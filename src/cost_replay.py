"""Equal ORIGINAL annotation-point budget, not measured human-time equivalence."""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from scipy.spatial.distance import cdist
from winding_replay import make_design,block_update,block_scores,metrics

def experiment(args):
    root,seed,budgets=args;t=time.time()
    rel,rd,pool,test,C0,mu0,M,meta=make_design(Path(root),seed)
    initial=list(pool[:8]);available=list(pool[8:]);var=.3**2
    for i in initial:C0,mu0=block_update(C0,mu0,*rd[i],var)
    loc=np.array([c['xyz'].mean(0)/np.array([700,700,2500]) for c in rel]);costs=np.array([len(c['xyz']) for c in rel]);rows=[]
    for budget in budgets:
        for policy in ['random','chronological','coverage','information','ivar']:
            C=C0.copy();mu=mu0.copy();remaining=available.copy();chosen=[];spent=0;rng=np.random.default_rng(seed+900000)
            while True:
                feasible=[i for i in remaining if costs[i]<=budget-spent]
                if not feasible:break
                if policy=='random':j=int(rng.integers(len(feasible)))
                elif policy=='chronological':j=int(np.argmin([rel[i]['time'] for i in feasible]))
                elif policy=='coverage':j=int(np.argmax(cdist(loc[feasible],loc[initial+chosen]).min(axis=1)))
                else:
                    scores=block_scores(C,[rd[i][0] for i in feasible],var,M if policy=='ivar' else None);j=int(np.argmax(scores/costs[feasible]))
                i=feasible[j];remaining.remove(i);chosen.append(i);spent+=int(costs[i]);C,mu=block_update(C,mu,*rd[i],var)
            rows.append(dict(seed=seed,policy=policy,budget_points=budget,spent_points=spent,queries=len(chosen),selected_ids=[rel[i]['id'] for i in chosen],metrics=metrics(rd,test,mu)))
    return dict(metadata=meta,rows=rows,seconds=time.time()-t)

def main():
    p=argparse.ArgumentParser();p.add_argument('--data',required=True);p.add_argument('--out',required=True)
    p.add_argument('--seeds',default=','.join(map(str,range(100,140))));p.add_argument('--budgets',default='64,128,256');p.add_argument('--workers',type=int,default=4)
    a=p.parse_args();tasks=[(a.data,int(s),list(map(int,a.budgets.split(',')))) for s in a.seeds.split(',')];results=[]
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        for r in ex.map(experiment,tasks):results.append(r)
    Path(a.out).write_text(json.dumps(dict(args=vars(a),results=results),indent=2))
if __name__=='__main__':main()
