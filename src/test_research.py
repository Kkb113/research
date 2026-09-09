"""Numerical and leakage audits. No network needed when data are present."""
from __future__ import annotations
import unittest,hashlib,json,tempfile,shutil
from pathlib import Path
import numpy as np
from numpy.testing import assert_allclose
from scipy.linalg import helmert
from winding_replay import block_update,block_scores,make_design,load_groups
from surface_replay import kernel,initial_points,choose,replay
ROOT=Path(__file__).resolve().parents[1]

class AlgebraTests(unittest.TestCase):
    def setUp(self):
        self.rng=np.random.default_rng(713);F=self.rng.normal(size=(11,11));self.Q=F.T@F+.1*np.eye(11)
        self.C=np.linalg.inv(self.Q);self.mu=self.rng.normal(size=11);self.A=self.rng.normal(size=(4,11));self.y=self.rng.normal(size=4);self.var=.27
    def test_block_update_direct_inverse(self):
        C,m=block_update(self.C,self.mu,self.A,self.y,self.var);Q=self.Q+self.A.T@self.A/self.var;h=self.Q@self.mu+self.A.T@self.y/self.var
        assert_allclose(C,np.linalg.inv(Q),rtol=1e-10,atol=1e-10);assert_allclose(m,np.linalg.solve(Q,h),rtol=1e-10,atol=1e-10)
    def test_weighted_risk_gain_direct(self):
        B=self.rng.normal(size=(7,11));M=B.T@B;C,_=block_update(self.C,self.mu,self.A,self.y,self.var)
        self.assertAlmostEqual(block_scores(self.C,[self.A],self.var,M)[0],np.trace(M@(self.C-C)),places=9)
    def test_covariance_decrease_psd(self):
        C,_=block_update(self.C,self.mu,self.A,self.y,self.var)
        self.assertGreater(np.linalg.eigvalsh(C).min(),0);self.assertGreater(np.linalg.eigvalsh(self.C-C).min(),-1e-10)
    def test_information_gain_direct_logdet(self):
        C,_=block_update(self.C,self.mu,self.A,self.y,self.var)
        self.assertAlmostEqual(block_scores(self.C,[self.A],self.var)[0],np.linalg.slogdet(self.C)[1]-np.linalg.slogdet(C)[1],places=9)
    def test_helmert_centering_per_point_error(self):
        x=self.rng.normal(size=15);H=helmert(15);assert_allclose(H.T@H@x,x-x.mean(),atol=1e-13)
        self.assertAlmostEqual(np.mean((H.T@H@x)**2),np.sum((H@x)**2)/15,places=13)
    def test_risk_theory_not_realized_error_guarantee(self):
        C=np.diag([100.,1.]);A=[np.array([[1.,0.]]),np.array([[0.,1.]])]
        self.assertEqual(int(np.argmax(block_scores(C,A,1e-9,np.eye(2)))),0)
        truth=np.array([0.,1.]);mu=np.zeros(2)
        _,m0=block_update(C,mu,A[0],A[0]@truth,1e-9);_,m1=block_update(C,mu,A[1],A[1]@truth,1e-9)
        self.assertGreater(np.sum((m0-truth)**2),np.sum((m1-truth)**2))

class SurfaceTests(unittest.TestCase):
    def setUp(self):
        rng=np.random.default_rng(4);self.uv=rng.uniform(size=(50,2));self.tv=rng.uniform(size=(20,2))
        self.y=np.column_stack([self.uv[:,0]*100,self.uv[:,1]*80,np.sin(self.uv[:,0]*3)*20])+1000
        self.ty=np.column_stack([self.tv[:,0]*100,self.tv[:,1]*80,np.sin(self.tv[:,0]*3)*20])+1000
    def test_sequential_prediction_matches_cholesky(self):
        r=replay(self.uv,self.y,self.tv,self.ty,'ivar',0,budgets=(8,));ids=r['selected'];origin=self.y[ids[0]]
        K=kernel(self.uv[ids],self.uv[ids])+1e-6*np.eye(len(ids))
        predicted=kernel(self.tv,self.uv[ids])@np.linalg.solve(K,self.y[ids]-origin)+origin
        rmse=np.sqrt(np.mean(np.sum((predicted-self.ty)**2,axis=1)));self.assertAlmostEqual(rmse,r['metrics']['8']['rmse_voxels'],places=6)
    def test_selection_label_blind(self):
        rng=np.random.default_rng(25)
        for policy in ['ivar','variance','coverage','random']:
            a=replay(self.uv,self.y,self.tv,self.ty,policy,9,budgets=(8,))
            b=replay(self.uv,rng.normal(size=self.y.shape),self.tv,rng.normal(size=self.ty.shape),policy,9,budgets=(8,))
            self.assertEqual(a['selected'],b['selected'])
    def test_selection_independent_of_test_locations(self):
        a=replay(self.uv,self.y,self.tv,self.ty,'ivar',0,budgets=(8,));b=replay(self.uv,self.y,self.tv+3,self.ty,'ivar',0,budgets=(8,))
        self.assertEqual(a['selected'],b['selected'])
    def test_ivar_maximizes_one_step_trace_decrease(self):
        C=kernel(self.uv,self.uv);noise=1e-6;init=initial_points(self.uv)
        for j in init:
            c=C[:,j].copy();C-=np.outer(c,c)/(C[j,j]+noise)
        j=choose(C,self.uv,init,'ivar',np.random.default_rng(1),noise);ids=[i for i in range(len(C)) if i not in init]
        reductions=[np.trace(C)-np.trace(C-np.outer(C[:,i],C[:,i])/(C[i,i]+noise)) for i in ids]
        self.assertEqual(j,ids[int(np.argmax(reductions))])

@unittest.skipUnless((ROOT/'audit/data/relative_windings.json').exists(),'public data not present')
class DataTests(unittest.TestCase):
    def test_source_hashes(self):
        manifest=json.loads((ROOT/'audit/manifest.json').read_text())
        for f in manifest['files']:
            if 'sha256' in f:self.assertEqual(hashlib.sha256((ROOT/'audit/data'/f['name']).read_bytes()).hexdigest(),f['sha256'])
    def test_group_counts_and_nonempty(self):
        g,_=load_groups(ROOT/'audit/data');self.assertEqual([len(g[x]) for x in ['relative','same','absolute']],[254,125,5])
    def test_test_values_and_geometry_do_not_change_selection_design(self):
        root=ROOT/'audit/data';a=make_design(root,100);test_ids={x.split(':')[1] for x in a[-1]['test_ids']}
        with tempfile.TemporaryDirectory() as temp:
            temp=Path(temp)
            for f in root.glob('*.json'):shutil.copy(f,temp/f.name)
            p=temp/'relative_windings.json';data=json.loads(p.read_text())
            for key in test_ids:
                for point in data['collections'][key]['points'].values():
                    if point.get('wind_a') is not None:point['wind_a']+=123
                    point['p']=[v+111 for v in point['p']]
            p.write_text(json.dumps(data));b=make_design(temp,100)
        for ix in [4,5,6]:assert_allclose(a[ix],b[ix],rtol=0,atol=0)
        for i in a[2]:assert_allclose(a[1][i][0],b[1][i][0],rtol=0,atol=0)
    def test_saved_splits_disjoint_and_acquisitions_legal(self):
        for fn in ['winding_confirm.json','winding_spatial.json']:
            p=ROOT/'results'/fn
            if not p.exists():continue
            for r in json.loads(p.read_text())['results']:
                pool=set(r['metadata']['pool_ids']);test=set(r['metadata']['test_ids']);self.assertFalse(pool&test)
                for row in r['rows']:
                    self.assertTrue(set(row['selected_ids'])<=pool);self.assertEqual(len(row['selected_ids']),len(set(row['selected_ids'])))
        p=ROOT/'results/surface_confirm.json'
        if p.exists():
            for r in json.loads(p.read_text())['results']:
                self.assertFalse(set(r['pool_indices'])&set(r['test_indices']))
                for row in r['rows']:self.assertEqual(len(row['selected']),len(set(row['selected'])))

@unittest.skipUnless((ROOT/'audit/data/relative_windings.json').exists(),'public data not present')
class PairTests(unittest.TestCase):
    def test_disjoint_pair_endpoints_and_no_test_queries(self):
        from pair_replay import pair_candidates
        rel,rd,pool,test,C,mu,M,meta=make_design(ROOT/'audit/data',600)
        for mode in ['adjacent','spanning']:
            A,y,candidates=pair_candidates(rel,rd,list(pool[8:]),mode);seen=set()
            for c in candidates:
                self.assertNotIn(c['collection_id'],meta['test_ids'])
                for i in c['point_indices']:
                    key=(c['collection_id'],i);self.assertNotIn(key,seen);seen.add(key)
            self.assertEqual(len(seen),2*len(candidates))
    def test_scalar_pair_update_matches_block(self):
        rng=np.random.default_rng(91);F=rng.normal(size=(10,10));C=np.linalg.inv(F.T@F+np.eye(10));mu=rng.normal(size=10);a=rng.normal(size=10);y=2.3
        expected,m=block_update(C,mu,a[None],np.array([y]),.09);u=C@a;den=.09+a@u
        assert_allclose(expected,C-np.outer(u,u)/den,atol=1e-12);assert_allclose(m,mu+u*(y-a@mu)/den,atol=1e-12)
    def test_acquisition_trajectory_label_blind(self):
        from pair_replay import pair_candidates,select
        rel,rd,pool,test,C,mu,M,meta=make_design(ROOT/'audit/data',600)
        for i in pool[:8]:C,mu=block_update(C,mu,*rd[i],.09)
        A,y,candidates=pair_candidates(rel,rd,list(pool[8:]),'spanning');locations=np.array([np.mean(c['xyz'],axis=0) for c in candidates]);known=np.zeros((1,3));sequences=[]
        for values in [y,np.random.default_rng(1).normal(size=y.shape)*100]:
            cc=C.copy();m=mu.copy();available=list(range(len(A)));chosen=[]
            for _ in range(16):
                i=select(cc,A,np.array(available),'ivar',M,locations,known,np.random.default_rng(0),.09)
                available.remove(i);chosen.append(i);cc,m=block_update(cc,m,A[i:i+1],values[i:i+1],.09)
            sequences.append(chosen)
        self.assertEqual(*sequences)
    def test_all_downloaded_patch_hashes(self):
        manifest_path=ROOT/'patches/manifest.json'
        if not manifest_path.exists():self.skipTest('patches not downloaded')
        manifest=json.loads(manifest_path.read_text());self.assertEqual(len(manifest['selected']),48)
        for f in manifest['files']:
            if 'sha256' in f:self.assertEqual(hashlib.sha256((ROOT/'patches'/f['path']).read_bytes()).hexdigest(),f['sha256'])

if __name__=='__main__':unittest.main(verbosity=2)
