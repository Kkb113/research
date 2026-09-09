"""Generate a minimal patch to a hash-verified production extractor."""
import argparse
import ast
import difflib
import hashlib
from pathlib import Path

UPSTREAM_SHA256='48d0c7d3ea057e4d8fb7e2b8abece75906fca3067fbcc6e8cda963c13f8a5065'
UPSTREAM_COMMIT='4accc199a55695ebbefaab4fb6a99faa800fcabf'


def patched_source(source,method='block',stream=False):
    if hashlib.sha256(source.encode()).hexdigest()!=UPSTREAM_SHA256:
        raise ValueError('upstream source differs from the pinned audited version; refusing patch')
    if method not in ('upstream','sparse','block'):raise ValueError(method)
    if method!='upstream':
        function='cell_argmax' if method=='block' else 'sparse_argmax'
        source=source.replace('\ndef extract(',f'\nfrom evidence_pipeline.select import {function} as _cell_argmax\n\ndef extract(',1)
    if stream:
        start=source.index('        positions, nxs, nys, presences = [], [], [], []')
        end=source.index('\n\ndef load_fiber_direction_samples',start)
        source=source[:start]+'''        from evidence_pipeline.stream import ordered_bounded_map, write_batches
        with ThreadPoolExecutor(max_workers=workers) as executor:
            batches = ordered_bounded_map(executor, process, work, 2 * workers)
            sample_count = write_batches(output, batches, extraction_identity,
                                         overwrite=overwrite)
    print(f"wrote {sample_count:,} samples from {len(work):,} chunks to {output}")
'''+source[end:]
    ast.parse(source)
    return source


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--method',choices=['block','sparse','upstream'],default='block');p.add_argument('--stream',action='store_true');p.add_argument('--diff',action='store_true');args=p.parse_args()
    source=args.source.read_text();patched=patched_source(source,args.method,args.stream)
    if args.diff:
        args.output.write_text(''.join(difflib.unified_diff(source.splitlines(True),patched.splitlines(True),fromfile='a/spiral-fitting/fiber_direction_samples.py',tofile='b/spiral-fitting/fiber_direction_samples.py')))
    else:
        if args.output.exists():raise FileExistsError(args.output)
        args.output.write_text(patched)
if __name__=='__main__':main()
