"""Download only pinned public files; reject changed bytes, oversized responses and unsafe paths."""
import argparse,hashlib,json,urllib.request,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
BASE='https://dl.ash2txt.org/datasets/spiral_datasets/PHercParis4/'
def safe_path(root,relative):
    p=(root/relative).resolve()
    if not p.is_relative_to(root.resolve()):raise ValueError('Unsafe path')
    return p

def retrieve(task):
    entry,path=task;url=entry['url']
    if not url.startswith(BASE):raise ValueError('Unexpected source domain or path')
    if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256']:return
    error=None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url,timeout=60) as response:raw=response.read(10_000_001)
            if len(raw)>10_000_000:raise ValueError('File exceeds size bound')
            if hashlib.sha256(raw).hexdigest()!=entry['sha256']:raise ValueError('Source has changed: '+url)
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw);return
        except Exception as exc:error=exc;time.sleep(attempt+1)
    raise RuntimeError(f'Acquisition failed for {url}: {error}')

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',default='.');a=p.parse_args();root=Path(a.root)
    ann=json.loads((root/'provenance/annotations_manifest.json').read_text());patch=json.loads((root/'provenance/patches_manifest.json').read_text())
    tasks=[(f,safe_path(root/'audit/data',f['name'])) for f in ann['files'] if 'sha256' in f]
    tasks += [(f,safe_path(root/'patches',f['path'])) for f in patch['files'] if 'sha256' in f]
    with ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(retrieve,tasks))
    (root/'audit').mkdir(exist_ok=True);(root/'patches').mkdir(exist_ok=True)
    (root/'audit/manifest.json').write_text(json.dumps(ann,indent=2));(root/'patches/manifest.json').write_text(json.dumps(patch,indent=2))
    print('Verified files:',len(tasks))
if __name__=='__main__':main()
