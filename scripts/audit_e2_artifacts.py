"""Recompute evidence claims from two completed E2 output folders."""
import argparse,json
from pathlib import Path
import numpy as np


def check(condition,message):
    if not condition:raise RuntimeError(message)


def main():
    p=argparse.ArgumentParser();p.add_argument('reference',type=Path);p.add_argument('repeat',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    left=json.loads((a.reference/'selection_checks.json').read_text());right=json.loads((a.repeat/'selection_checks.json').read_text())
    check(left==right,'configuration records differ between executions')
    check(len(left)==2480 and all(r['exact'] and r['digest']==r['reference_digest'] for r in left),'invalid exactness records')
    compared=0
    for f in sorted((a.reference/'selections').glob('*.npz')):
        with np.load(f,allow_pickle=False) as x,np.load(a.repeat/'selections'/f.name,allow_pickle=False) as y:
            check(set(x.files)==set(y.files),'selected field names differ')
            for k in x.files:
                check(x[k].dtype==y[k].dtype and x[k].shape==y[k].shape and np.array_equal(x[k],y[k]),f.name+':'+k)
                compared+=1
    check(compared==155,'missing selection arrays')
    stages={};stage_array_comparisons=0
    for directory in [a.reference,a.repeat]:
        rows=json.loads((directory/'stage/stage_results.json').read_text())
        check(len(rows)==4,'missing stage volumes')
        for row in rows:
            scroll=row['scroll']
            with np.load(directory/'stage'/f'{scroll}_upstream.npz',allow_pickle=False) as ref:
                for arm in ['sparse','block','stream']:
                    with np.load(directory/'stage'/f'{scroll}_{arm}.npz',allow_pickle=False) as z:
                        for key in ['position_zyx','nx','ny','presence']:
                            check(z[key].shape==ref[key].shape and z[key].dtype==ref[key].dtype and np.array_equal(z[key],ref[key]),f'{scroll}:{arm}:{key}')
                            stage_array_comparisons+=1
                        check(json.loads(str(z['metadata_json']))==json.loads(str(ref['metadata_json'])),'within-run metadata differs')
            if directory==a.reference:stages[scroll]=row['output']
            else:
                old=stages[scroll]
                check(old['arrays']==row['output']['arrays'] and old['count']==row['output']['count'],'cross-run output hashes differ')
                metadata_old={k:v for k,v in old['metadata'].items() if k!='manifest_url'}
                metadata_new={k:v for k,v in row['output']['metadata'].items() if k!='manifest_url'}
                check(metadata_old==metadata_new,'nontransport metadata changed')
    writer_left=json.loads((a.reference/'writer_stress.json').read_text());writer_right=json.loads((a.repeat/'writer_stress.json').read_text())
    check(len(writer_left)==len(writer_right)==3,'writer workloads missing')
    for l,r in zip(writer_left,writer_right):
        check(l['repeat']==r['repeat'],'writer workload differs')
        for arm in ['concatenate','stream']:
            check(l['methods'][arm]['array_hashes']==r['methods'][arm]['array_hashes'],'writer output differs across runs')
        check(r['methods']['concatenate']['array_hashes']==r['methods']['stream']['array_hashes'],'writer method output differs')
    timing=json.loads((a.repeat/'selection_timing.json').read_text());sc=sorted({r['scroll'] for r in timing});performance={}
    for base in ['upstream','sparse']:
        ratios=[r['methods'][base]['median_seconds']/r['methods']['block']['median_seconds'] for r in timing]
        logmeans=[float(np.mean([np.log(v) for r,v in zip(timing,ratios) if r['scroll']==scroll])) for scroll in sc]
        performance[base]={'equal_scroll_geomean_speedup':float(np.exp(np.mean(logmeans))),'wins':sum(v>1 for v in ratios),'cases':len(ratios),'minimum_speedup':min(ratios),'maximum_speedup':max(ratios)}
    result={'configuration_records_exact':len(left),'saved_selection_arrays_exact':compared,'stage_array_comparisons_exact':stage_array_comparisons,'stage_volumes_cross_run_exact':len(stages),'writer_workloads_exact':len(writer_right),'performance_repeat':performance,'interpretation':'Exact preprocessing evidence, not a reconstruction/human-cost improvement.'}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
