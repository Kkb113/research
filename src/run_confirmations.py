"""Bounded CPU reproduction; all errors and failures propagate, no best-only filtering."""
import os,subprocess,sys,json
from pathlib import Path
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
Path('results').mkdir(exist_ok=True)
def run(script,*args):
    subprocess.run([sys.executable,'src/'+script,*args],check=True)
def seeds(start,end):return ','.join(map(str,range(start,end)))
run('winding_replay.py','--data','audit/data','--out','results/winding_confirm.json','--seeds',seeds(100,140),'--workers','4')
run('surface_replay.py','--data','patches','--out','results/surface_confirm.json','--partition','test','--splits','0,1','--repeats','20','--workers','4')
run('cost_replay.py','--data','audit/data','--out','results/winding_cost.json')
for name,start,end,split in [('confirm',600,640,'random'),('spatial',700,720,'spatial_z')]:
    path='results/pair_spanning_'+name+'.json'
    run('pair_replay.py','--data','audit/data','--out',path,'--seeds',seeds(start,end),'--split',split,'--pair-mode','spanning')
    run('extra_pair_baselines.py','--data','audit/data','--frozen',path,'--out','results/pair_extra_'+name+'.json','--repeats','20' if name=='confirm' else '10')
import numpy as np
summary={}
for name,budget,metric in [('surface_confirm','16','rmse_voxels'),('winding_confirm','32','rmse_windings'),('pair_spanning_confirm','64','rmse_windings'),('pair_spanning_spatial','64','rmse_windings'),('pair_extra_confirm','64','rmse_windings'),('pair_extra_spatial','64','rmse_windings')]:
    data=json.loads(Path('results/'+name+'.json').read_text())['results'];policies=sorted({r['policy'] for x in data for r in x['rows']})
    summary[name]={p:float(np.mean([r['metrics'][budget][metric] for x in data for r in x['rows'] if r['policy']==p])) for p in policies}
Path('results/reproduction_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
