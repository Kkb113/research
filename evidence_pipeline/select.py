"""Exact uint8 per-cell selection for Vesuvius fiber_direction_samples.

Known block reduction, not a new sampling rule. Global cells, half-open ROI,
C-order tie breaking, lexicographic cell order, and returned dtype are retained.
Only uint8 3D inputs are supported; the upstream extractor uses that format.
"""
from __future__ import annotations
import operator
import numpy as np


def _validate(presence, global_begin, cell_size, threshold, valid_begin, valid_end):
    a = np.asarray(presence)
    if a.ndim != 3 or a.dtype != np.uint8:
        raise ValueError('presence must be a 3D uint8 array')
    c = operator.index(cell_size)
    t = operator.index(threshold)
    if c <= 0 or not 0 <= t <= 255:
        raise ValueError('positive integer cell_size and threshold in [0,255] required')
    vectors = []
    for value in (global_begin, valid_begin, valid_end):
        v = np.asarray(value)
        if v.shape != (3,) or v.dtype.kind not in 'iu':
            raise ValueError('origins and ROI bounds must be three integer coordinates')
        if any(int(x) < -(2**62) or int(x) >= 2**62 for x in v):
            raise ValueError('coordinate magnitude must be below 2**62')
        vectors.append(v.astype(np.int64))
    origin, begin, end = vectors
    lo = np.maximum(begin, origin)
    hi = np.minimum(end, origin + np.array(a.shape, dtype=np.int64))
    return a, origin, c, t, lo, hi


def _empty():
    return np.empty(0, dtype=np.int64), np.empty((0, 3), dtype=np.int64)


def sparse_argmax(presence, global_begin, cell_size, threshold, valid_begin, valid_end):
    """Strong simple baseline: threshold BEFORE materializing coordinates."""
    a, origin, c, t, lo, hi = _validate(presence, global_begin, cell_size, threshold, valid_begin, valid_end)
    if np.any(hi <= lo):
        return _empty()
    start = lo - origin
    crop = a[tuple(slice(int(l), int(h)) for l, h in zip(start, hi - origin))]
    loc = np.array(np.nonzero(crop >= t), dtype=np.int64).T
    if not len(loc):
        return _empty()
    xyz = loc + lo
    flat = np.ravel_multi_index((xyz - origin).T, a.shape).astype(np.int64)
    cells = xyz // c
    values = crop[tuple(loc.T)]
    order = np.lexsort((flat, -values.astype(np.int64), cells[:, 2], cells[:, 1], cells[:, 0]))
    cell_order = cells[order]
    first = np.r_[True, np.any(cell_order[1:] != cell_order[:-1], axis=1)]
    chosen = order[first]
    return flat[chosen], xyz[chosen]


def cell_argmax(presence, global_begin, cell_size, threshold, valid_begin, valid_end,
                *, tile_voxels=1_048_576):
    """Drop-in _cell_argmax replacement with bounded dense reduction tiles.

    Each dense tile contains <= tile_voxels values (unless the sparse fallback is
    used). Total memory also includes required result arrays; this is not an RSS
    cap. At c=1 or c>32 we use sparse selection, avoiding huge padded cells.
    No density- or scroll-specific dispatch is used.
    """
    a, origin, c, t, lo, hi = _validate(presence, global_begin, cell_size, threshold, valid_begin, valid_end)
    budget = operator.index(tile_voxels)
    if budget <= 0:
        raise ValueError('tile_voxels must be a positive integer')
    if np.any(hi <= lo):
        return _empty()
    if c == 1:
        start = lo - origin
        crop = a[tuple(slice(int(l), int(h)) for l, h in zip(start, hi - origin))]
        loc = np.array(np.nonzero(crop >= t), dtype=np.int64).T
        xyz = loc + lo
        return np.ravel_multi_index((xyz-origin).T, a.shape).astype(np.int64), xyz
    if c > 32 or c**3 > budget:
        return sparse_argmax(a, origin, c, t, lo, hi)
    cell_lo = lo // c
    cell_hi = (hi - 1) // c + 1
    n = cell_hi - cell_lo
    # Rectangular tiles in lexicographic order: when x is split, y and z must
    # each span only one cell. When y is split, z spans only one cell.
    cell_budget = budget // c**3
    tx = min(int(n[2]), cell_budget)
    ty = min(int(n[1]), cell_budget // tx) if tx == n[2] else 1
    tz = min(int(n[0]), cell_budget // (tx*ty)) if tx == n[2] and ty == n[1] else 1
    out_flat, out_xyz = [], []
    for z in range(0, int(n[0]), tz):
        for y in range(0, int(n[1]), ty):
            for x in range(0, int(n[2]), tx):
                count = np.minimum(n - [z,y,x], [tz,ty,tx])
                base = (cell_lo + [z,y,x])*c
                shape = tuple(int(v*c) for v in count)
                block = np.full(shape, -1, dtype=np.int16)
                b_lo = np.maximum(base, lo)
                b_hi = np.minimum(base + np.array(shape), hi)
                dst = tuple(slice(int(l), int(h)) for l,h in zip(b_lo-base,b_hi-base))
                src = tuple(slice(int(l), int(h)) for l,h in zip(b_lo-origin,b_hi-origin))
                block[dst] = a[src]
                bz,by,bx = map(int,count)
                cells = block.reshape(bz,c,by,c,bx,c).transpose(0,2,4,1,3,5).reshape(-1,c**3)
                best = cells.argmax(axis=1)
                good = np.flatnonzero(cells[np.arange(len(cells)), best] >= t)
                if not len(good):
                    continue
                cell_pos = np.array(np.unravel_index(good,(bz,by,bx)),dtype=np.int64).T
                offsets = np.array(np.unravel_index(best[good],(c,c,c)),dtype=np.int64).T
                xyz = base + c*cell_pos + offsets
                flat = np.ravel_multi_index((xyz-origin).T,a.shape).astype(np.int64)
                out_flat.append(flat);out_xyz.append(xyz)
    if not out_flat:
        return _empty()
    return np.concatenate(out_flat), np.concatenate(out_xyz)
