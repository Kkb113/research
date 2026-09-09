# E2 correctness argument and resource contract

This is known reduction/serialization mathematics applied to one pinned implementation, not a new learning theory.

## Selection identity

Let the accepted voxels in global integer cell k be those inside the same half-open ROI with uint8 presence at least the threshold. The original code lexicographically sorts by cell (z,y,x), then descending presence, then original C-order flat index, and takes the first voxel per cell. Thus its answer is the unique maximum of the ordered pair `(presence, -flat_index)` in each accepted cell.

E2 aligns blocks to the GLOBAL cell lattice, not the chunk origin. The within-cell array order is z-major, then y, then x. For any fixed cell, that order agrees with increasing original C-order flat index, including when the cell intersects a clipped chunk/ROI boundary. NumPy argmax chooses the first maximum in this order. Invalid padded values are -1 in int16, strictly below every uint8 value and every allowed threshold. Therefore padding cannot win an accepted cell, even at threshold zero. The selected local offsets map back to the original integer coordinates and flat indices.

Tiles enumerate cells lexicographically. When x is tiled, y and z each span one cell; when y is tiled, z spans one. Only complete x/y planes may span multiple z cells. Concatenating tile outputs therefore preserves original output order. c=1 uses the same threshold and C-order traversal. The sparse fallback directly implements the original total ordering after thresholding.

Consequently, for supported inputs, both methods select the same indices and coordinates in the same order. Gathering the unchanged nx, ny and presence arrays at those indices yields the same bytes. The original extractor still performs the identical float32 scale conversion. The finite oracle/configuration tests check the implementation of this argument, not just the resulting sample count.

This does not certify physical correctness of the prediction field. Identical inputs also do not prove bitwise-identical outcomes from an unexecuted nondeterministic GPU optimizer.

## Dense selection working memory

A regular tile contains at most the configured voxel budget, provided cell_size cubed fits it. The int16 padding/rearrangement arrays scale with this tile, rather than voxel-wide int64 coordinate grids. Large cells use the explicitly documented sparse fallback. Required selected output coordinates still scale with sample count. This is a bound on dense reduction tiles, not a total RSS cap.

## Output accumulation

For S records, the four raw output arrays contain 15*S bytes: three float32 coordinates and three uint8 values. The streaming writer spools these to disk and writes NPY headers plus bounded raw-file transfers into a compressed ZIP. It does not build a full concatenated output array in RAM. Output order and values are unchanged. Header version/ZIP timestamps may differ while parsed arrays and metadata agree.

The ordered producer keeps at most max_pending outstanding futures, including ready-but-unconsumed results; integration sets this to twice the worker count. Total memory still includes chunk decoding, output batches, interpreter/libraries, source key sets and work lists. Disk grows with output, and the existing downstream loader is not out-of-core. Atomic publication of a completed temporary file is not a guarantee against filesystem/power-loss durability failures.

The intentional empty-work behavior differs: original concatenation raises; the optional streaming variant writes a valid empty format-2 artifact. Unsupported input shapes/dtypes/parameters and upstream source drift fail explicitly.
