"""Run E2 fixed-corpus verification, never treating repeated timings as scrolls."""
import argparse,hashlib,json,os,resource,subprocess,sys,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from evidence_pipeline.fixtures import verify,decode,load_upstream
from evidence_pipeline.select import cell_argmax,sparse_argmax

def digest(arrays):
 h=hashlib.sha256()
 for a in arrays:
  a=np.ascontiguousarray(a);h.update(str(a.dtype).encode());h.update(str(a.shape).encode());h.update(a.tobytes())
 return h.hexdigest()

def main():
 p=argparse.ArgumentParser();p.add_argument('--fixtures',type=Path,required=True);p.add_argument('--upstream',type=Path,required=True);p.add_argument('--out',type=Path,default=ROOT/'results');p.add_argument('--memory-case');p.add_argument('--method');args=p.parse_args()
 u=load_upstream(args.upstream);funcs={'upstream':u._cell_argmax,'sparse':sparse_argmax,'block':cell_argmax}
 manifest=json.loads((args.fixtures/'manifest.json').read_text())
 if args.memory_case:
  v,c=next((v,c) for v in manifest for c in v['cases'] if c['id']==args.memory_case);a=decode(args.fixtures,v,c);o=np.array(c['index'])*v['metadata']['presence']['chunks']
  out=funcs[args.method](a,o,2,160,o,o+a.shape)
  print(json.dumps({'rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'digest':digest(out)}));return
 _,n=verify(args.fixtures);args.out.mkdir(parents=True,exist_ok=True);(args.out/'selections').mkdir(exist_ok=True)
 checks=[];timings=[];rng=np.random.default_rng(20260909)
 for v in manifest:
  for case in v['cases']:
   if case['role']=='development':continue
   a=decode(args.fixtures,v,case);origin=np.array(case['index'])*v['metadata']['presence']['chunks'];nx=decode(args.fixtures,v,case,'nx');ny=decode(args.fixtures,v,case,'ny')
   for c in [1,2,4,8]:
    for threshold in [0,80,160,240,255]:
     for roi in ['full','clipped']:
      lo=origin+(np.array([1,3,5]) if roi=='clipped' else 0);hi=origin+np.array(a.shape)-(np.array([2,4,6]) if roi=='clipped' else 0);inp=(a,origin,c,threshold,lo,hi)
      ref=funcs['upstream'](*inp);refhash=digest(ref)
      for method in ['sparse','block']:
       res=funcs[method](*inp);exact=all(np.array_equal(x,y) for x,y in zip(ref,res));checks.append({'case':case['id'],'cell_size':c,'threshold':threshold,'roi':roi,'method':method,'exact':exact,'count':len(res[0]),'digest':digest(res),'reference_digest':refhash})
       if not exact:raise AssertionError(checks[-1])
   inp=(a,origin,2,160,origin,origin+np.array(a.shape));ref=funcs['upstream'](*inp);flat,coords=ref
   np.savez_compressed(args.out/'selections'/(case['id']+'.npz'),flat=flat,coordinates=coords,nx=nx.ravel()[flat],ny=ny.ravel()[flat],presence=a.ravel()[flat])
   row={'case':case['id'],'scroll':v['scroll'],'count':len(flat),'foreground_fraction':float(np.mean(a>=160)),'methods':{}}
   for method in funcs:funcs[method](*inp);row['methods'][method]={'seconds':[]}
   for repeat in range(5):
    for method in rng.permutation(list(funcs)):
     start=time.perf_counter();res=funcs[method](*inp);dt=time.perf_counter()-start;assert digest(res)==digest(ref);row['methods'][method]['seconds'].append(dt)
   for method in funcs:
    row['methods'][method]['median_seconds']=float(np.median(row['methods'][method]['seconds']))
    command=[sys.executable,__file__,'--fixtures',str(args.fixtures),'--upstream',str(args.upstream),'--memory-case',case['id'],'--method',method]
    memory=json.loads(subprocess.check_output(command,text=True,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}));assert memory['digest']==digest(ref);row['methods'][method].update(memory)
   timings.append(row);(args.out/'selection_timing.json').write_text(json.dumps(timings,indent=2));print(case['id'],len(flat),'speedup',round(row['methods']['upstream']['median_seconds']/row['methods']['block']['median_seconds'],2),flush=True)
 (args.out/'selection_checks.json').write_text(json.dumps(checks,indent=2))
 summary={'source_files_verified':n,'cases':len(timings),'comparisons':len(checks),'all_exact':all(x['exact'] for x in checks),'volumes':{}}
 for v in manifest:
  rows=[r for r in timings if r['scroll']==v['scroll']];summary['volumes'][v['scroll']]={m:{'median_seconds':float(np.median([r['methods'][m]['median_seconds'] for r in rows])),'median_rss_mib':float(np.median([r['methods'][m]['rss_mib'] for r in rows]))} for m in funcs}
  for other in ['upstream','sparse']:summary['volumes'][v['scroll']]['block_speedup_vs_'+other]=float(np.median([r['methods'][other]['median_seconds']/r['methods']['block']['median_seconds'] for r in rows]))
 (args.out/'selection_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
