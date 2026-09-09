"""Reconstruct real patch XYZ samples on GIVEN UV/mask; not unknown-sheet unwrapping."""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import tifffile
from scipy.spatial.distance import cdist

def kernel(x,y,ell=.3):
    r=np.sqrt(5)*cdist(x,y)/ell
    return 100*(1+x@y.T)+(1+r+r*r/3)*np.exp(-r)

def initial_points(uv):
    selected=[]
    for corner in np.array([[0,0],[1,1],[0,1],[1,0]]):
        ds=np.sum((uv-corner)**2,axis=1);ds[selected]=np.inf;selected.append(int(np.argmin(ds)))
    return selected

def choose(C,uv,selected,policy,rng,noise):
    mask=np.ones(len(uv),bool);mask[selected]=False;ids=np.flatnonzero(mask)
    if policy=='random':return int(rng.choice(ids))
    if policy=='coverage':score=cdist(uv[ids],uv[selected]).min(axis=1)
    elif policy=='variance':score=np.diag(C)[ids]
    elif policy=='ivar':score=np.sum(C[:,ids]**2,axis=0)/(np.diag(C)[ids]+noise)
    else:raise ValueError(policy)
    return int(ids[np.argmax(score)])

def replay(uv,truth,testuv,testtruth,policy,seed,ell=.3,budgets=(4,8,16,32)):
    C=kernel(uv,uv,ell);Ct=kernel(testuv,uv,ell);noise=1e-6
    init=initial_points(uv);origin=truth[init[0]].copy();Y=truth-origin;T=testtruth-origin
    mu=np.zeros_like(Y);mt=np.zeros_like(T);selected=[];rng=np.random.default_rng(seed)
    def acquire(j):
        nonlocal C,Ct,mu,mt
        c=C[:,j].copy();ct=Ct[:,j].copy();den=C[j,j]+noise;res=Y[j]-mu[j]
        mu+=np.outer(c/den,res);mt+=np.outer(ct/den,res)
        C-=np.outer(c,c)/den;Ct-=np.outer(ct,c)/den;selected.append(j)
    def score():
        e=np.linalg.norm(mt-T,axis=1)
        return dict(rmse_voxels=float(np.sqrt(np.mean(e**2))),mae_voxels=float(e.mean()),p95_voxels=float(np.quantile(e,.95)))
    for j in init:acquire(j)
    out={'0':score()}
    for b in range(1,max(budgets)+1):
        j=choose(C,uv,selected,policy,rng,noise);acquire(j)
        if b in budgets:out[str(b)]=score()
    return dict(policy=policy,seed=seed,metrics=out,selected=selected)

def load_patch(path):
    arr=np.stack([tifffile.imread(path/(s+'.tif')) for s in 'xyz'],axis=-1).astype(float)
    valid=np.isfinite(arr).all(-1)&(arr>=0).all(-1);ij=np.argwhere(valid)
    if len(ij)<96:raise ValueError('fewer than 96 valid vertices')
    uv=ij/np.maximum(1,np.array(valid.shape)-1)
    return uv,arr[valid],dict(shape=list(valid.shape),valid_vertices=int(valid.sum()),centroid_xyz=arr[valid].mean(0).tolist())

def experiment(args):
    root,name,split_seed,ell,repeats=args;t=time.time();uv,y,meta=load_patch(Path(root)/name)
    rng=np.random.default_rng(split_seed);order=rng.permutation(len(uv));npool=min(256,len(uv)//2)
    pool=order[:npool];test=order[npool:npool+512];rows=[]
    for policy in ['coverage','variance','ivar']:
        rows.append(replay(uv[pool],y[pool],uv[test],y[test],policy,split_seed,ell))
    for repeat in range(repeats):
        rows.append(replay(uv[pool],y[pool],uv[test],y[test],'random',split_seed*1000+repeat+100000,ell))
    return dict(patch=name,split_seed=split_seed,ell=ell,metadata=meta,pool_indices=pool.tolist(),test_indices=test.tolist(),rows=rows,seconds=time.time()-t)

def main():
    p=argparse.ArgumentParser();p.add_argument('--data',required=True);p.add_argument('--out',required=True)
    p.add_argument('--partition',choices=['dev','test','all'],default='dev');p.add_argument('--ell',type=float,default=.3)
    p.add_argument('--splits',default='0,1');p.add_argument('--repeats',type=int,default=10);p.add_argument('--workers',type=int,default=4)
    a=p.parse_args();names=json.loads((Path(a.data)/'manifest.json').read_text())['selected']
    names=names[:8] if a.partition=='dev' else names[8:] if a.partition=='test' else names
    tasks=[(a.data,n,s,a.ell,a.repeats) for n in names for s in map(int,a.splits.split(','))];results=[];excluded=[];validtasks=[]
    for task in tasks:
        try:load_patch(Path(task[0])/task[1]);validtasks.append(task)
        except Exception as exc:excluded.append(dict(patch=task[1],error=repr(exc)))
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        for r in ex.map(experiment,validtasks):
            results.append(r);print('FINISHED',r['patch'],r['split_seed'],round(r['seconds'],3),flush=True)
    Path(a.out).write_text(json.dumps(dict(args=vars(a),excluded=excluded,results=results),indent=2))
if __name__=='__main__':main()
