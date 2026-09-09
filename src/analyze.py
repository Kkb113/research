"""Conditional paired spatial bootstrap. Same scroll and fixed fitted models, not independent trials."""
from pathlib import Path
from collections import defaultdict
import json,argparse,zipfile
import numpy as np
from winding_replay import load_groups

def group_labels(xyz):
    return [str(tuple(np.floor(np.array(x)/[1500,1500,3000]).astype(int))) for x in xyz]

def surface_analysis(root):
    data=json.loads((root/'results/surface_confirm.json').read_text())['results'];per=defaultdict(lambda:defaultdict(list));centres={}
    for x in data:
        centres[x['patch']]=x['metadata']['centroid_xyz']
        for policy in ['random','coverage','variance','ivar']:
            per[x['patch']][policy].append(np.mean([r['metrics']['16']['rmse_voxels'] for r in x['rows'] if r['policy']==policy]))
    names=sorted(per);labels=group_labels([centres[n] for n in names]);unique=list(dict.fromkeys(labels));groups=[np.where(np.array(labels)==g)[0] for g in unique]
    v={p:np.array([np.mean(per[n][p]) for n in names]) for p in ['random','coverage','variance','ivar']};out={}
    for base in ['random','coverage','variance']:
        a=v[base];b=v['ivar'];totals=np.array([[a[ix].sum(),b[ix].sum()] for ix in groups]);rng=np.random.default_rng(988)
        draw=rng.integers(len(groups),size=(10000,len(groups)));s=totals[draw].sum(1);ratios=100*(1-s[:,1]/s[:,0])
        out['ivar_vs_'+base]=dict(baseline_mean=float(a.mean()),ivar_mean=float(b.mean()),reduction_percent=float(100*(1-b.mean()/a.mean())),spatial_bootstrap_95=np.quantile(ratios,[.025,.975]).tolist(),patch_wins=int((b<a).sum()),n_patches=len(names),n_clusters=len(groups))
    return out

def compare_mse(B,A,labels):
    mask=np.isfinite(B)&np.isfinite(A);B=np.where(mask,B,0);A=np.where(mask,A,0)
    base=float(np.sqrt(B.sum(1)/mask.sum(1)).mean());method=float(np.sqrt(A.sum(1)/mask.sum(1)).mean())
    unique=sorted(set(labels));assignment=np.array([unique.index(x) for x in labels]);G=len(unique)
    b=np.column_stack([B[:,assignment==g].sum(1) for g in range(G)]);a=np.column_stack([A[:,assignment==g].sum(1) for g in range(G)]);m=np.column_stack([mask[:,assignment==g].sum(1) for g in range(G)])
    rng=np.random.default_rng(699);ratios=[]
    for _ in range(100):
        draws=rng.integers(G,size=(100,G));weights=np.stack([np.bincount(x,minlength=G) for x in draws],1);den=m@weights;valid=(den>0).all(0)
        bb=np.sqrt((b@weights)[:,valid]/den[:,valid]).mean(0);aa=np.sqrt((a@weights)[:,valid]/den[:,valid]).mean(0);ratios.extend((100*(1-aa/bb)).tolist())
    return dict(baseline_mean_split_rmse=base,ivar_mean_split_rmse=method,reduction_percent=100*(1-method/base),conditional_spatial_bootstrap_95=np.quantile(ratios,[.025,.975]).tolist(),valid_resamples=len(ratios),n_clusters=G,n_splits=len(B))

def pair_analysis(root,name):
    data=json.loads((root/'results'/f'pair_spanning_{name}.json').read_text())['results'];extra=json.loads((root/'results'/f'pair_extra_{name}.json').read_text())['results'];extra={x['seed']:x['rows'] for x in extra}
    g,_=load_groups(root/'audit/data');xyz={c['id']:c['xyz'].mean(0) for c in g['relative']};ids=sorted(xyz);index={c:i for i,c in enumerate(ids)};labels=group_labels([xyz[c] for c in ids])
    policies=['random','chronological','coverage','information','ivar','longest','span_matched_random'];matrices={p:np.full((len(data),len(ids)),np.nan) for p in policies}
    curves=defaultdict(list)
    for si,x in enumerate(data):
        rows=x['rows']+extra[x['rows'][0]['seed']]
        for p in policies:
            chosen=[r for r in rows if r['policy']==p];curves[p].append(np.mean([r['metrics']['64']['rmse_windings'] for r in chosen]))
            matrices[p][si,[index[c] for c in x['metadata']['test_ids']]]=np.mean([r['metrics']['64']['test_collection_mse'] for r in chosen],axis=0)
    return dict(mean_split_rmse={p:float(np.mean(curves[p])) for p in policies},comparisons={'ivar_vs_'+p:compare_mse(matrices[p],matrices['ivar'],labels) for p in policies if p!='ivar'},note='For repeated span-matched random controls, the bootstrap pools MSE before RMSE; mean_split_rmse averages individual RMSE. These estimands differ slightly.')

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',default='.');a=p.parse_args();root=Path(a.root)
    if not (root/'results/surface_confirm.json').exists():
        with zipfile.ZipFile(root/'external_results.zip') as archive:
            for info in archive.infolist():
                if not (root/info.filename).resolve().is_relative_to(root.resolve()):raise ValueError('Unsafe archive path')
            archive.extractall(root)
    result={'surface':surface_analysis(root),'spanning_pairs':pair_analysis(root,'confirm'),'spatial_pairs':pair_analysis(root,'spatial'),'warning':'One scroll; fixed fitted models; correlated replay splits; no independent-scroll or human-time generalization is established.'}
    (root/'results/analysis_summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
