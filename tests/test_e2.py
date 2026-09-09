from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import tempfile
import time
import unittest
import numpy as np
from evidence_pipeline.select import cell_argmax, sparse_argmax
from evidence_pipeline.stream import write_batches, ordered_bounded_map


def oracle(a, origin, c, threshold, begin, end):
    chosen = {}
    for local in np.ndindex(a.shape):
        point=tuple(int(origin[k])+local[k] for k in range(3))
        if not all(begin[k]<=point[k]<end[k] for k in range(3)) or a[local]<threshold:continue
        key=tuple(x//c for x in point)
        flat=int(np.ravel_multi_index(local,a.shape));v=int(a[local])
        if key not in chosen or v>chosen[key][0]:chosen[key]=(v,flat,point)
    records=[chosen[k] for k in sorted(chosen)]
    return (np.array([r[1] for r in records],dtype=np.int64),
            np.array([r[2] for r in records],dtype=np.int64).reshape(-1,3))


class SelectionTests(unittest.TestCase):
    def test_scalar_oracle_480_cases(self):
        rng=np.random.default_rng(20260909)
        for trial in range(480):
            shape=tuple(rng.integers(1,12,3));a=rng.integers(0,256,shape,dtype=np.uint8)
            if trial%7==0:a.fill(trial%256)
            if trial%5==0:a=np.asfortranarray(a)
            if trial%3==0:a=a[::-1,::2,::-1]
            o=rng.integers(-50,50,3);lo=o+rng.integers(-2,4,3);hi=o+np.array(a.shape)-rng.integers(-2,4,3)
            c=int(rng.choice([1,2,3,4,8,33]));t=int(rng.choice([0,80,160,240,255]));copy=a.copy()
            expected=oracle(a,o,c,t,lo,hi)
            for f in (cell_argmax,sparse_argmax):
                actual=f(a,o,c,t,lo,hi)
                for x,y in zip(expected,actual):np.testing.assert_array_equal(x,y)
            actual=cell_argmax(a,o,c,t,lo,hi,tile_voxels=max(c**3,8))
            for x,y in zip(expected,actual):np.testing.assert_array_equal(x,y)
            np.testing.assert_array_equal(a,copy)

    def test_large_origins(self):
        a=np.ones((5,6,7),dtype=np.uint8);o=np.array([2**50,-2**50,2**40])
        for c in [2,3,4]:
            x=cell_argmax(a,o,c,0,o,o+list(a.shape));y=oracle(a,o,c,0,o,o+list(a.shape))
            for u,v in zip(x,y):np.testing.assert_array_equal(u,v)

    def test_empty_shapes(self):
        for s in [(0,3,4),(1,0,3),(4,3,0)]:
            for f in (cell_argmax,sparse_argmax):
                i,p=f(np.zeros(s,dtype=np.uint8),[0,0,0],2,0,[0,0,0],[4,4,4])
                self.assertEqual(i.shape,(0,));self.assertEqual(p.shape,(0,3))

    def test_invalid_inputs(self):
        a=np.zeros((2,3,4),dtype=np.uint8)
        for c,t in [(0,0),(-1,0),(2,-1),(2,256)]:
            with self.assertRaises(ValueError):cell_argmax(a,[0]*3,c,t,[0]*3,[5]*3)
        with self.assertRaises(ValueError):cell_argmax(a.astype(float),[0]*3,2,0,[0]*3,[5]*3)
        with self.assertRaises(ValueError):cell_argmax(a,[0]*3,2,0,[0]*3,[5]*3,tile_voxels=0)
        with self.assertRaises(TypeError):cell_argmax(a,[0]*3,2.5,0,[0]*3,[5]*3)


def batch(n):
    return (np.arange(n*3,dtype=np.float32).reshape(n,3),*(np.arange(n,dtype=np.uint8) for _ in range(3)))

class StreamTests(unittest.TestCase):
    def test_exact_arrays_and_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'out.npz';b=[batch(0),batch(3),batch(1),batch(0),batch(7)]
            self.assertEqual(write_batches(p,iter(b),{'format_version':2}),11)
            with np.load(p,allow_pickle=False) as z:
                for i,name in enumerate(['position_zyx','nx','ny','presence']):
                    np.testing.assert_array_equal(z[name],np.concatenate([v[i] for v in b]))
                self.assertEqual(json.loads(str(z['metadata_json'])),{'format_version':2,'sample_count':11})
            self.assertEqual([x.name for x in Path(d).iterdir()],['out.npz'])

    def test_empty(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'empty.npz';write_batches(p,[],{})
            with np.load(p) as z:self.assertEqual(z['position_zyx'].shape,(0,3))

    def test_failure_preserves_destination_and_cleans_spools(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'out.npz';p.write_bytes(b'original')
            with self.assertRaises(FileExistsError):write_batches(p,[batch(1)],{})
            def broken():
                yield batch(1)
                raise OSError('injected I/O failure')
            with self.assertRaises(OSError):write_batches(p,broken(),{},overwrite=True)
            self.assertEqual(p.read_bytes(),b'original')
            self.assertEqual(len(list(Path(d).iterdir())),1)

    def test_invalid_batch(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):write_batches(Path(d)/'x',[batch(2)[:3]],{})
            self.assertEqual(list(Path(d).iterdir()),[])

    def test_bounded_order(self):
        consumed=[]
        def source():
            for i in range(20):consumed.append(i);yield i
        def fn(i):time.sleep((3-i%4)*.0001);return i*i
        with ThreadPoolExecutor(3) as pool:
            it=ordered_bounded_map(pool,fn,source(),4)
            self.assertEqual(next(it),0);self.assertEqual(len(consumed),4)
            self.assertEqual([0]+list(it),[i*i for i in range(20)])

if __name__=='__main__':unittest.main()
