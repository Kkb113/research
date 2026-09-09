"""Post-hoc diagnostics: longest spans and random queries matched to IVAR span deciles."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import argparse,json
import numpy as np
from winding_replay import make_design,block_update,metrics
from pair_replay import pair_candidates

def experiment(task):
    root,frozen,repeats=task;seed=frozen['rows'][0]['seed'];split=frozen['rows'][0]['split']
    rel,rd,pool,test,C0,mu0,M,meta=make_design(Path(root),seed,split=split);var=.09
    for i in pool[:8]:C0,mu0=block_update(C0,mu0,*rd[i],var)
    A,y,candidates=pair_candidates(rel,rd,list(pool[8:]),mode='spanning');index={c['id']:i for i,c in enumerate(candidates)}
    distance=np.array([np.linalg.norm(np.diff(c['xyz'],axis=0)) for c in candidates]);bins=np.digitize(distance,np.quantile(distance,np.arange(1,10)/10))
    active=next(x for x in frozen['rows'] if x['policy']=='ivar');target=[bins[index[c]] for c in active['selected_ids']];rows=[]
    for policy in ['longest']+['span_matched_random']*repeats:
        repeat=len(rows)-1;C=C0.copy();mu=mu0.copy();remaining=list(range(len(A)));selected=[]
        rng=np.random.default_rng(seed*1000+max(repeat,0)+777);row=dict(policy=policy,repeat=repeat,metrics={'0':metrics(rd,test,mu)})
        for b in range(1,65):
            if policy=='longest':i=max(remaining,key=lambda j:distance[j])
            else:i=int(rng.choice([j for j in remaining if bins[j]==target[b-1]]))
            remaining.remove(i);selected.append(i);u=C@A[i];den=var+A[i]@u;mu+=u*(y[i]-A[i]@mu)/den;C-=np.outer(u,u)/den;C=(C+C.T)/2
            if b in [8,16,32,64]:row['metrics'][str(b)]=metrics(rd,test,mu)
        row['selected_ids']=[candidates[i]['id'] for i in selected];row['total_endpoint_distance']=float(distance[selected].sum());rows.append(row)
    return dict(seed=seed,split=split,metadata=meta,rows=rows)

def main():
    p=argparse.ArgumentParser();p.add_argument('--data',required=True);p.add_argument('--frozen',required=True);p.add_argument('--out',required=True);p.add_argument('--repeats',type=int,default=20);a=p.parse_args()
    frozen=json.loads(Path(a.frozen).read_text())['results'];tasks=[(a.data,f,a.repeats) for f in frozen]
    with ProcessPoolExecutor(max_workers=4) as ex:results=list(ex.map(experiment,tasks))
    Path(a.out).write_text(json.dumps(dict(args=vars(a),results=results),indent=2))
if __name__=='__main__':main()
