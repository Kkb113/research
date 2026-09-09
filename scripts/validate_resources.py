"""Correct Linux process-memory measurement and repeated-real-batch writer stress.

ru_maxrss can inherit the parent's pre-exec high-water mark. Use /proc/self/status
VmHWM, which describes this executed process's address space, and retain both.
"""
import argparse,json,os,resource,subprocess,sys,time,hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from evidence_pipeline.fixtures import decode,load_upstream
from evidence_pipeline.select import cell_argmax,sparse_argmax
from evidence_pipeline.stream import write_batches

def memory():
    values={s.split(':')[0]:s.split(':')[1].strip() for s in Path('/proc/self/status').read_text().splitlines() if ':' in s}
    return {'vmhwm_mib':int(values['VmHWM'].split()[0])/1024,'vmrss_mib':int(values['VmRSS'].split()[0])/1024,'ru_maxrss_mib_inheritance_caveat':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024}

def array_hashes(path):
    with np.load(path) as z:return {n:hashlib.sha256(z[n].tobytes()).hexdigest() for n in ['position_zyx','nx','ny','presence']}

def main():
 p=argparse.ArgumentParser();p.add_argument('--fixtures',type=Path,required=True);p.add_argument('--upstream',type=Path,required=True);p.add_argument('--results',type=Path,default=ROOT/'results');p.add_argument('--case');p.add_argument('--method');p.add_argument('--writer');p.add_argument('--repeat',type=int,default=1);args=p.parse_args()
 if args.case:
  manifest=json.loads((args.fixtures/'manifest.json').read_text());v,c=next((v,c) for v in manifest for c in v['cases'] if c['id']==args.case);a=decode(args.fixtures,v,c);o=np.array(c['index'])*v['metadata']['presence']['chunks'];up=load_upstream(args.upstream)
  fn={'upstream':up._cell_argmax,'sparse':sparse_argmax,'block':cell_argmax}[args.method];out=fn(a,o,2,160,o,o+a.shape)
  print(json.dumps({**memory(),'count':len(out[0])}));return
 if args.writer:
  batches=[]
  for path in sorted((args.results/'selections').glob('*.npz')):
   with np.load(path) as z:batches.append((z['coordinates'].astype(np.float32),z['nx'],z['ny'],z['presence']))
  count=sum(len(b[0]) for b in batches)*args.repeat
  metadata={'artifact_type':'fiber_direction_samples','format_version':2,'sample_count':count,'experiment':'repeated-real-selections-not-new-regions'}
  target=args.results/('stress_'+args.writer+'_'+str(args.repeat)+'.npz');start=time.perf_counter()
  if args.writer=='concatenate':
   arrays=[np.concatenate([b[i] for _ in range(args.repeat) for b in batches]) for i in range(4)]
   np.savez_compressed(target,**dict(zip(['position_zyx','nx','ny','presence'],arrays)),metadata_json=np.asarray(json.dumps(metadata)))
  else:write_batches(target,(b for _ in range(args.repeat) for b in batches),metadata,overwrite=True)
  elapsed=time.perf_counter()-start;record={'seconds':elapsed,'count':count,'output_bytes':target.stat().st_size,'raw_bytes':count*15,**memory()}
  # Memory sampled BEFORE full verification reads, otherwise verifier pollutes metric.
  record['array_hashes']=array_hashes(target);print(json.dumps(record));target.unlink();return
 env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}
 def run(*extra):
  cmd=[sys.executable,__file__,'--fixtures',str(args.fixtures),'--upstream',str(args.upstream),'--results',str(args.results),*extra]
  return json.loads(subprocess.check_output(cmd,env=env,text=True))
 timings=json.loads((args.results/'selection_timing.json').read_text());rows=[]
 for row in timings:
  record={'case':row['case'],'scroll':row['scroll'],'methods':{}}
  for method in ['upstream','sparse','block']:
   record['methods'][method]=run('--case',row['case'],'--method',method)
   assert record['methods'][method]['count']==row['count']
  rows.append(record)
 (args.results/'selection_memory_corrected.json').write_text(json.dumps(rows,indent=2));print('corrected memory complete',flush=True)
 stress=[]
 for repeat in [1,16,128]:
  results={method:run('--writer',method,'--repeat',str(repeat)) for method in ['concatenate','stream']}
  assert results['concatenate']['array_hashes']==results['stream']['array_hashes'];stress.append({'repeat':repeat,'methods':results})
  (args.results/'writer_stress.json').write_text(json.dumps(stress,indent=2));print('writer',repeat,{m:{k:v for k,v in r.items() if k in ['seconds','vmhwm_mib','count']} for m,r in results.items()},flush=True)
if __name__=='__main__':main()
