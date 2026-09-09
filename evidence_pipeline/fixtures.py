"""Manifest-verified real prediction fixtures; no learned references are truth labels."""
import importlib.util
import json
import hashlib
from pathlib import Path
import numpy as np


def load_upstream(path):
    spec=importlib.util.spec_from_file_location('upstream_fiber_direction_samples',path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m


def verify(root):
    root=Path(root);manifest=json.loads((root/'manifest.json').read_text());count=0
    for volume in manifest:
        for f in volume['files']:
            p=root/f['path']
            if not p.exists():
                # Earlier artifact collection omitted hidden .zarray metadata.
                # Reconstitute exact source bytes separately, never invent hashes.
                raise FileNotFoundError(p)
            assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256'],p
            count+=1
    return manifest,count


def decode(root,volume,case,field='presence'):
    import numcodecs
    meta=volume['metadata'][field];b=(Path(root)/case['fields'][field]).read_bytes()
    raw=numcodecs.get_codec(meta['compressor']).decode(b) if meta.get('compressor') else b
    arr=np.frombuffer(raw,np.dtype(meta['dtype']))
    chunks=np.array(meta['chunks']);begin=np.array(case['index'])*chunks
    edge=np.minimum(chunks,np.array(meta['shape'])-begin)
    shape=tuple(chunks) if arr.size==int(np.prod(chunks)) else tuple(edge)
    return arr.reshape(shape,order=meta.get('order','C'))[tuple(slice(0,int(x)) for x in edge)]


def source_record(path,url):
    p=Path(path);return {'url':url,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
