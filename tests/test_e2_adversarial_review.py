"""Post-confirmation adversarial review; no algorithm tuning or new efficacy claim."""
import itertools
from pathlib import Path
import tempfile
import unittest
import numpy as np
from evidence_pipeline.select import cell_argmax, sparse_argmax
from evidence_pipeline.stream import write_batches


def scalar(a, origin, c, threshold, begin, end):
    best = {}
    zsize, ysize, xsize = a.shape
    for z in range(zsize):
        for y in range(ysize):
            for x in range(xsize):
                p = tuple(int(origin[k]) + v for k, v in enumerate((z,y,x)))
                v = int(a[z,y,x])
                if v < threshold or not all(int(begin[k]) <= p[k] < int(end[k]) for k in range(3)):
                    continue
                key = tuple(vv // c for vv in p)
                index = (z * ysize + y) * xsize + x
                if key not in best or v > best[key][0]:
                    best[key] = (v, index, p)
    order = [best[k] for k in sorted(best)]
    return np.asarray([v[1] for v in order], dtype=np.int64), np.asarray([v[2] for v in order], dtype=np.int64).reshape(-1,3)


class ExhaustiveReview(unittest.TestCase):
    def test_exhaustive_6561_volumes(self):
        o = np.asarray([-1,2,1]); hi = o + 2
        for vals in itertools.product((0,1,255), repeat=8):
            a = np.asarray(vals,dtype=np.uint8).reshape(2,2,2)
            for c, threshold, lo in [(2,0,o),(3,1,o),(2,255,o+[1,0,0])]:
                expected = scalar(a,o,c,threshold,lo,hi)
                for method in (cell_argmax,sparse_argmax):
                    actual = method(a,o,c,threshold,lo,hi)
                    if not all(np.array_equal(x,y) for x,y in zip(expected,actual)):
                        self.fail(str((vals,c,threshold,lo.tolist(),method.__name__)))

    def test_no_clobber_race(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d)/'out.npz'
            def batches():
                target.write_bytes(b'competing writer')
                yield (np.zeros((1,3),np.float32), *[np.zeros(1,np.uint8) for _ in range(3)])
            with self.assertRaises(FileExistsError):
                write_batches(target,batches(),{})
            self.assertEqual(target.read_bytes(), b'competing writer')
            self.assertEqual([p.name for p in Path(d).iterdir()], ['out.npz'])

    def test_failure_in_metadata_serialization_is_atomic(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'out.npz';target.write_bytes(b'original')
            with self.assertRaises(TypeError):
                write_batches(target,[],{'not_serializable':object()},overwrite=True)
            self.assertEqual(target.read_bytes(),b'original')
            self.assertEqual(len(list(Path(d).iterdir())),1)

    def test_noncontiguous_batches_roundtrip(self):
        raw=np.arange(90,dtype=np.float32).reshape(30,3)
        b=(raw[::-2],np.arange(30,dtype=np.uint8)[::-2],np.arange(30,dtype=np.uint8)[::-2],np.arange(30,dtype=np.uint8)[::-2])
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'out.npz';write_batches(target,[b],{'format_version':2})
            with np.load(target,allow_pickle=False) as z:
                for key,arr in zip(('position_zyx','nx','ny','presence'),b):
                    np.testing.assert_array_equal(z[key],arr)
                    self.assertEqual(z[key].dtype,arr.dtype)

if __name__=='__main__': unittest.main()
