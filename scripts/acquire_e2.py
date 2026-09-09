"""Acquire immutable E2 inputs; reject hash changes instead of replacing cases."""
import argparse,base64,gzip,hashlib,json,os,tempfile,time,urllib.request
from pathlib import Path

UPSTREAM='4accc199a55695ebbefaab4fb6a99faa800fcabf'
SOURCE_HASH='48d0c7d3ea057e4d8fb7e2b8abece75906fca3067fbcc6e8cda963c13f8a5065'
MANIFEST_HASH='b4683eb73b8b5756935696c1382edcfba42bb813ab4d0ad56f983aa63ad8bb9f'

def fetch(url,path,expected):
    path=Path(path)
    if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==expected:return
    last=None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url,timeout=60) as response:data=response.read(64*1024*1024+1)
            if len(data)>64*1024*1024:raise ValueError('source exceeds per-file safety bound')
            if hashlib.sha256(data).hexdigest()!=expected:raise ValueError('SHA256 mismatch: '+url)
            path.parent.mkdir(parents=True,exist_ok=True)
            fd,tmp=tempfile.mkstemp(dir=path.parent,prefix='.download-')
            try:
                with os.fdopen(fd,'wb') as f:f.write(data)
                os.replace(tmp,path)
            finally:
                if os.path.exists(tmp):os.unlink(tmp)
            return
        except (OSError,TimeoutError) as e:last=e;time.sleep(attempt+1)
    raise last

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path('.'));p.add_argument('--data',type=Path,default=Path('e2_data'));args=p.parse_args()
    manifest_path=args.root/'provenance/fiber_manifest.json'
    if manifest_path.exists():raw=manifest_path.read_bytes()
    else:
        transport=args.root/'provenance/fiber_manifest.json.gz.b64'
        encoded=transport.read_text() if transport.exists() else ''.join(p.read_text().strip() for p in sorted((args.root/'provenance/manifest.parts').glob('*.b64')))
        raw=gzip.decompress(base64.b64decode(encoded))
    assert hashlib.sha256(raw).hexdigest()==MANIFEST_HASH
    args.data.mkdir(parents=True,exist_ok=True);(args.data/'manifest.json').write_bytes(raw)
    m=json.loads(raw)
    for v in m:
        for f in v['files']:fetch(f['url'],args.data/f['path'],f['sha256'])
    url=f'https://raw.githubusercontent.com/ScrollPrize/villa/{UPSTREAM}/spiral-fitting/fiber_direction_samples.py'
    fetch(url,args.data/'upstream_fiber_direction_samples.py',SOURCE_HASH)
    print('Verified',sum(len(v['files']) for v in m),'source files and upstream code')
if __name__=='__main__':main()
