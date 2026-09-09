"""Real-data whole-collection replay; reduced winding field, NOT production fitter."""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from scipy.linalg import helmert,cho_factor,cho_solve
from scipy.interpolate import interp1d
from scipy.spatial.distance import cdist

def load_groups(root):
    groups={}
    for kind,fn in [('absolute','abs_winding.json'),('relative','relative_windings.json'),('same','same_windings.json')]:
        out=[]
        for cid,c in json.loads((root/fn).read_text())['collections'].items():
            # JSON insertion order is lexicographic, NOT annotation path order.
            ps=[v for _,v in sorted(c['points'].items(),key=lambda t:int(t[0]))]
            ps=[p for p in ps if np.isfinite(p['p']).all() and (kind=='same' or p.get('wind_a') is not None)]
            if len(ps)<(1 if kind=='absolute' else 2):continue
            out.append(dict(id=kind+':'+str(cid),xyz=np.array([p['p'] for p in ps],float),values=np.array([0 if kind=='same' else p['wind_a'] for p in ps],float),time=min(p.get('creation_time',0) for p in ps)))
        groups[kind]=out
    cp=json.loads((root/'umbilicus.json').read_text())['control_points']
    u=np.array(sorted([[p['z'],p['x'],p['y']] for p in cp]))
    return groups,interp1d(u[:,0],u[:,1:],axis=0,bounds_error=False,fill_value='extrapolate')

def farthest_centres(x,n):
    j=int(np.argmin(np.sum((x-x.mean(0))**2,axis=1)));selected=[j];ds=np.sum((x-x[j])**2,axis=1)
    for _ in range(min(n,len(x))-1):
        j=int(np.argmax(ds));selected.append(j);ds=np.minimum(ds,np.sum((x-x[j])**2,axis=1))
    return x[selected]

def make_design(root,seed=0,ell=1.,noise=.3,dimension=96,split='random'):
    g,umb=load_groups(root);rel=g['relative'];rng=np.random.default_rng(seed);ids=np.arange(len(rel));order=rng.permutation(ids)
    if split=='random':test=order[:len(ids)//5];pool=order[len(ids)//5:]
    elif split=='spatial_z':
        z=np.array([v['xyz'][:,2].mean() for v in rel]);bins=np.quantile(z,[.2,.4,.6,.8]);block=np.digitize(z,bins)
        test=ids[block==seed%5];pool=rng.permutation(ids[block!=seed%5])
    else:raise ValueError(split)
    # Test geometry and labels are excluded from acquisition and basis construction.
    geom=np.concatenate([c['xyz'] for c in g['same']+g['absolute']+[rel[i] for i in pool]])
    origin=np.array([4500.,4000.,12000.]);scale=np.array([700.,700.,2500.])*ell
    centres=farthest_centres((geom-origin)/scale,dimension)
    def phi(x):
        xx=(x-origin)/scale;r=np.linalg.norm(x[:,:2]-umb(x[:,2]),axis=1)
        return np.column_stack([np.ones(len(x))*20.,(x-origin)/np.array([1000.,1000.,4000.])*20.,r/1000.*20.,20.*np.exp(-.5*cdist(xx,centres,'sqeuclidean'))/np.sqrt(dimension)])
    def design(c):
        k=8 if c['id'].startswith('same') else 16
        ix=np.unique(np.round(np.linspace(0,len(c['xyz'])-1,min(k,len(c['xyz'])))).astype(int))
        x=c['xyz'][ix];val=c['values'][ix];xy=c['xyz'][:,:2]-umb(c['xyz'][:,2])
        theta=np.unwrap(np.arctan2(xy[:,1],xy[:,0]) % (2*np.pi));radius=np.linalg.norm(xy,axis=1)
        prior=radius/25.-theta/(2*np.pi);A=phi(x);y=val-prior[ix]
        if not c['id'].startswith('absolute'):H=helmert(len(ix));A=H@A;y=H@y
        return A,y
    base=[design(c) for c in g['absolute']+g['same']];rd=[design(c) for c in rel]
    d=rd[0][0].shape[1];Q=np.eye(d);h=np.zeros(d)
    for A,y in base:Q+=A.T@A/noise**2;h+=A.T@y/noise**2
    C=np.linalg.inv(Q);mu=C@h
    M=sum(rd[i][0].T@rd[i][0]/(len(rd[i][1])+1) for i in pool)/len(pool)
    meta=dict(test_ids=[rel[i]['id'] for i in test],pool_ids=[rel[i]['id'] for i in pool],base_same=len(g['same']),base_absolute=len(g['absolute']),n_relative=len(rel),dimension=d)
    return rel,rd,pool,test,C,mu,M,meta

def block_update(C,mu,A,y,variance):
    U=C@A.T;S=variance*np.eye(len(A))+A@U;cf=cho_factor(S,lower=True,check_finite=False)
    K=cho_solve(cf,U.T,check_finite=False).T;new=C-K@U.T
    return (new+new.T)/2,mu+K@(y-A@mu)

def block_scores(C,matrices,variance,M=None):
    scores=[]
    for A in matrices:
        U=C@A.T;S=variance*np.eye(len(A))+A@U;cf=cho_factor(S,lower=True,check_finite=False)
        score=2*np.log(np.diag(cf[0])).sum()-len(A)*np.log(variance) if M is None else np.trace(cho_solve(cf,U.T@M@U,check_finite=False))
        scores.append(float(score))
    return np.array(scores)

def metrics(rd,test,mu):
    mse=[];mae=[];bad=[]
    for i in test:
        A,y=rd[i];e=A@mu-y;n=len(e)+1;pe=helmert(n).T@e
        mse.append(float(np.mean(pe**2)));mae.append(float(np.mean(abs(pe))));bad.append(float(np.mean(abs(pe)>.5)))
    return dict(rmse_windings=float(np.sqrt(np.mean(mse))),mae_windings=float(np.mean(mae)),fraction_over_half_winding=float(np.mean(bad)),test_collection_mse=mse)

def experiment(args):
    root,seed,ell,noise,dim,split,budgets,policies=args;t=time.time()
    rel,rd,pool,test,C0,mu0,M,meta=make_design(Path(root),seed,ell,noise,dim,split)
    initial=list(pool[:8]);available=list(pool[8:]);var=noise**2
    for i in initial:C0,mu0=block_update(C0,mu0,*rd[i],var)
    rows=[]
    for policy in policies:
        C=C0.copy();mu=mu0.copy();remaining=available.copy();chosen=[];rng=np.random.default_rng(seed+900000)
        loc=np.array([c['xyz'].mean(0)/np.array([700,700,2500]) for c in rel])
        row=dict(seed=seed,split=split,ell=ell,noise=noise,policy=policy,metrics={'0':metrics(rd,test,mu)})
        for b in range(1,max(budgets)+1):
            if policy=='random':j=int(rng.integers(len(remaining)))
            elif policy=='chronological':j=int(np.argmin([rel[i]['time'] for i in remaining]))
            elif policy=='coverage':j=int(np.argmax(cdist(loc[remaining],loc[initial+chosen]).min(axis=1)))
            else:j=int(np.argmax(block_scores(C,[rd[i][0] for i in remaining],var,M if policy=='ivar' else None)))
            i=remaining.pop(j);chosen.append(i);C,mu=block_update(C,mu,*rd[i],var)
            if b in budgets:row['metrics'][str(b)]=metrics(rd,test,mu)
        row['selected_ids']=[rel[i]['id'] for i in chosen];rows.append(row)
    return dict(metadata=meta,rows=rows,seconds=time.time()-t)

def main():
    p=argparse.ArgumentParser();p.add_argument('--data',required=True);p.add_argument('--out',required=True)
    p.add_argument('--seeds',default='0,1,2');p.add_argument('--ell',type=float,default=1);p.add_argument('--noise',type=float,default=.3)
    p.add_argument('--dimension',type=int,default=96);p.add_argument('--split',default='random');p.add_argument('--budgets',default='8,16,32')
    p.add_argument('--workers',type=int,default=3);p.add_argument('--policies',default='random,chronological,coverage,information,ivar')
    a=p.parse_args();seeds=list(map(int,a.seeds.split(',')));budgets=list(map(int,a.budgets.split(',')))
    tasks=[(a.data,s,a.ell,a.noise,a.dimension,a.split,budgets,a.policies.split(',')) for s in seeds];results=[]
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        for result in ex.map(experiment,tasks):
            results.append(result);print('FINISHED',result['rows'][0]['seed'],round(result['seconds'],2),flush=True)
            Path(a.out).write_text(json.dumps(dict(args=vars(a),results=results),indent=2))
if __name__=='__main__':main()
