"""Bounded ordered processing and atomic, streamed format-2 NPZ output.

The NPZ arrays and metadata are loader-compatible with the original Vesuvius
extractor. Uses temporary disk proportional to total uncompressed output.
"""
from __future__ import annotations
from collections import deque
import json
import os
from pathlib import Path
import shutil
import tempfile
import zipfile
import numpy as np


def ordered_bounded_map(executor, fn, work, max_pending):
    """Preserve input order with at most max_pending unfinished/ready futures."""
    if max_pending < 1:
        raise ValueError('max_pending must be positive')
    work=iter(work);queue=deque()
    try:
        for _ in range(max_pending):
            try:item=next(work)
            except StopIteration:break
            queue.append(executor.submit(fn,item))
        while queue:
            result=queue.popleft().result()
            yield result
            try:item=next(work)
            except StopIteration:continue
            queue.append(executor.submit(fn,item))
    finally:
        for future in queue:future.cancel()


def write_batches(output,batches,metadata,*,overwrite=False):
    """Write (position_zyx,nx,ny,presence) batches and return sample_count.

    Empty streams are supported. Failure leaves an existing destination intact.
    Unlike np.savez_compressed(concatenate(...)), no full output-sized RAM copy
    is needed. The arrays themselves and ZIP compression retain original types.
    """
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    if output.exists() and not overwrite:raise FileExistsError(output)
    names=('position_zyx','nx','ny','presence')
    dtypes=(np.dtype('<f4'),np.dtype('u1'),np.dtype('u1'),np.dtype('u1'))
    count=0
    with tempfile.TemporaryDirectory(prefix='.fiber-spool-',dir=output.parent) as directory:
        root=Path(directory)
        handles=[open(root/(name+'.raw'),'wb') for name in names]
        try:
            for batch in batches:
                if len(batch)!=4:raise ValueError('each batch must have four arrays')
                arrays=[np.asarray(a) for a in batch];n=len(arrays[0])
                if arrays[0].shape!=(n,3) or any(a.shape!=(n,) for a in arrays[1:]):
                    raise ValueError('batch shapes must be (N,3), (N,), (N,), (N,)')
                if arrays[0].dtype!=np.float32 or any(a.dtype!=np.uint8 for a in arrays[1:]):
                    raise ValueError('batch dtypes must be float32, uint8, uint8, uint8')
                for h,a,dtype in zip(handles,arrays,dtypes):
                    if n:h.write(np.ascontiguousarray(a,dtype=dtype).tobytes())
                count+=n
        finally:
            for h in handles:h.close()
        meta=dict(metadata);meta['sample_count']=count
        temporary=root/'complete.npz'
        with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED,allowZip64=True) as archive:
            for name,dtype in zip(names,dtypes):
                shape=(count,3) if name=='position_zyx' else (count,)
                with archive.open(name+'.npy','w',force_zip64=True) as member:
                    np.lib.format.write_array_header_2_0(member,{
                        'descr':np.lib.format.dtype_to_descr(dtype),'fortran_order':False,'shape':shape})
                    with open(root/(name+'.raw'),'rb') as source:
                        shutil.copyfileobj(source,member,length=1024*1024)
            with archive.open('metadata_json.npy','w',force_zip64=True) as member:
                np.lib.format.write_array(member,np.asarray(json.dumps(meta)),allow_pickle=False)
        if overwrite:
            os.replace(temporary,output)
        else:
            # Same-filesystem hard link provides atomic no-clobber publication.
            os.link(temporary,output)
    return count
