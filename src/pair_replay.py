"""Cost-fair two-point relative queries; whole original collections held out."""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from scipy.linalg import helmert
from scipy.spatial.distance import cdist
from winding_replay import make_design,block_update,metrics

POLICIES=['random','chronological','coverage','information','ivar']
def pair_candidates(rel,rd,available,mode='adjacent'):
    candidates=[];A=[];y=[]
    for i in available:
        D,z=rd[i];n=len(z)+1;H=helmert(n);P=H.T@D;v=H.T@z
        indices=np.unique(np.round(np.linspace(0,len(rel[i]['xyz'])-1,min(16,len(rel[i]['xyz'])))).astype(int))
        pairs=[(j,j+1) for j in range(0,n-1,2)] if mode=='adjacent' else [(j,n-1-j) for j in range(n//2)]
        for number,(j,k) in enumerate(pairs):
            A.append((P[j]-P[k])/np.sqrt(2));y.append((v[j]-v[k])/np.sqrt(2))
            candidates.append(dict(id=rel[i]['id']+f':pair:{number}',collection_id=rel[i]['id'],point_indices=[int(indices[j]),int(indices[k])],xyz=rel[i]['xyz'][indices[[j,k]]].tolist(),time=rel[i]['time']))
    return np.array(A),np.array(y),candidates

def select(C,A,remaining,policy,M,locations,known,rng,variance):
    if policy=='random':return int(rng.choice(remaining))
    if policy=='coverage':return int(remaining[np.argmax(cdist(locations[remaining],known).min(axis=1))])
    U=C@A[remaining].T;den=variance+np.sum(A[remaining].T*U,axis=0)
    score=den if policy=='information' else np.sum(U*(M@U),axis=0)/den
    return int(remaining[np.argmax(score)])

def experiment(args):
    root,seed,split,budgets,mode=args;t=time.time()
    rel,rd,pool,test,C0,mu0,M,meta=make_design(Path(root),seed,split=split)
    initial=list(pool[:8]);available=list(pool[8:]);variance=.3**2
    for i in initial:C0,mu0=block_update(C0,mu0,*rd[i],variance)
    A,y,candidates=pair_candidates(rel,rd,available,mode);meta['n_pair_candidates']=len(candidates);meta['pair_mode']=mode
    locations=np.array([np.mean(c['xyz'],axis=0)/np.array([700,700,2500]) for c in candidates])
    initial_locations=np.array([rel[i]['xyz'].mean(0)/np.array([700,700,2500]) for i in initial]);rows=[]
    for policy in POLICIES:
        C=C0.copy();mu=mu0.copy();remaining=list(range(len(A)));chosen=[];rng=np.random.default_rng(seed+900000)
        row=dict(seed=seed,split=split,policy=policy,metrics={'0':metrics(rd,test,mu)})
        for budget in range(1,max(budgets)+1):
            if policy=='chronological':i=min(remaining,key=lambda j:(candidates[j]['time'],candidates[j]['id']))
            else:
                known=np.concatenate([initial_locations,locations[chosen]]) if chosen else initial_locations
                i=select(C,A,np.array(remaining),policy,M,locations,known,rng,variance)
            remaining.remove(i);chosen.append(i)
            u=C@A[i];den=variance+A[i]@u;mu+=u*((y[i]-A[i]@mu)/den);C-=np.outer(u,u)/den;C=(C+C.T)/2
            if budget in budgets:row['metrics'][str(budget)]=metrics(rd,test,mu)
        row['selected_ids']=[candidates[j]['id'] for j in chosen];row['selected_pairs']=[candidates[j] for j in chosen];rows.append(row)
    return dict(metadata=meta,rows=rows,seconds=time.time()-t)

def main():
    p=argparse.ArgumentParser();p.add_argument('--data',required=True);p.add_argument('--out',required=True)
    p.add_argument('--pair-mode',choices=['adjacent','spanning'],default='adjacent');p.add_argument('--seeds',default='0,1,2');p.add_argument('--split',default='random');p.add_argument('--budgets',default='8,16,32,64');p.add_argument('--workers',type=int,default=4)
    a=p.parse_args();tasks=[(a.data,int(s),a.split,list(map(int,a.budgets.split(','))),a.pair_mode) for s in a.seeds.split(',')];results=[]
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        for r in ex.map(experiment,tasks):
            results.append(r);print('FINISHED',r['rows'][0]['seed'],flush=True)
    Path(a.out).write_text(json.dumps(dict(args=vars(a),results=results),indent=2))
if __name__=='__main__':main()
