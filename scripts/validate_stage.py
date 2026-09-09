"""Run the actual upstream extraction entry point against an immutable real-chunk HTTP mirror.

The mirror advertises only the sampled subset, not a complete production volume.
Local wall times include listing, read, decompression, selection and NPZ writing.
"""
import argparse,contextlib,hashlib,http.server,importlib.util,json,os,socket,sys,threading,time,types
from pathlib import Path
from urllib.parse import urlparse,parse_qs
import xml.etree.ElementTree as ET
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from evidence_pipeline.fixtures import verify
from evidence_pipeline.integrate import patched_source


def hashes(path):
    with np.load(path,allow_pickle=False) as z:
        arrays={name:hashlib.sha256(z[name].tobytes()).hexdigest() for name in ['position_zyx','nx','ny','presence']}
        meta=json.loads(str(z['metadata_json']))
        return {'arrays':arrays,'metadata':meta,'count':len(z['presence'])}


def main():
    p=argparse.ArgumentParser();p.add_argument('--fixtures',type=Path,required=True);p.add_argument('--upstream',type=Path,required=True);p.add_argument('--out',type=Path,default=ROOT/'results/stage');args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    manifest,_=verify(args.fixtures);routes={};presence_keys=[]
    for v in manifest:
        routes[urlparse(v['manifest_url']).path]=(args.fixtures/v['scroll']/'manifest.json').read_bytes()
        for name in ['presence','nx','ny']:
            routes[urlparse(v['urls'][name]).path+'/.zarray']=(args.fixtures/v['scroll']/name/'.zarray').read_bytes()
        for c in v['cases']:
            for name,path in c['fields'].items():
                key=urlparse(v['urls'][name]).path+'/'+v['metadata'][name].get('dimension_separator','.').join(map(str,c['index']))
                routes[key]=(args.fixtures/path).read_bytes()
                if name=='presence':presence_keys.append(key.lstrip('/'))
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_GET(self):
            parsed=urlparse(self.path);q=parse_qs(parsed.query)
            if q.get('list-type')==['2']:
                root=ET.Element('ListBucketResult');ET.SubElement(root,'IsTruncated').text='false'
                for key in presence_keys:
                    if key.startswith(q.get('prefix',[''])[0]):ET.SubElement(ET.SubElement(root,'Contents'),'Key').text=key
                b=ET.tostring(root)
            else:
                b=routes.get(parsed.path)
                if b is None:self.send_error(404);return
            self.send_response(200);self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    host='fixture.s3.localhost';prefix=f'http://{host}:{server.server_port}'
    old_dns=socket.getaddrinfo
    socket.getaddrinfo=lambda h,*a,**kw:old_dns('127.0.0.1' if h==host else h,*a,**kw)
    old_proxy=os.environ.get('NO_PROXY');os.environ['NO_PROXY']='*'
    source=args.upstream.read_text();arms={}
    for name,method,stream in [('upstream','upstream',False),('sparse','sparse',False),('block','block',False),('stream','block',True)]:
        module=types.ModuleType('fiber_'+name);module.__file__=str(args.upstream);exec(compile(patched_source(source,method,stream),str(args.upstream),'exec'),module.__dict__);arms[name]=module
    rows=[];rng=np.random.default_rng(20260909)
    try:
        for v in manifest:
            chunks=np.array(v['metadata']['presence']['chunks']);indices=np.array([c['index'] for c in v['cases']]);config=json.loads((args.fixtures/v['scroll']/'manifest.json').read_text());scale=float(config['source_to_base'])*2**int(config['groups']['presence']['scaledown'])
            zroi=(int(indices[:,0].min()*chunks[0]*scale),int((indices[:,0].max()+1)*chunks[0]*scale));url=prefix+urlparse(v['manifest_url']).path
            reference=None;row={'scroll':v['scroll'],'z_roi':zroi,'fixture_chunks':len(v['cases']),'arms':{k:{'seconds':[]} for k in arms}}
            for repeat in range(-1,3):
                for name in (list(arms) if repeat==-1 else rng.permutation(list(arms))):
                    output=args.out/(v['scroll']+'_'+name+'.npz')
                    if output.exists():output.unlink()
                    with contextlib.redirect_stdout(open(os.devnull,'w')):
                        start=time.perf_counter();arms[name].extract(url,zroi,output,workers=1);elapsed=time.perf_counter()-start
                    result=hashes(output)
                    if reference is None:reference=result
                    assert result==reference,(v['scroll'],name)
                    loaded=arms['upstream'].load_fiber_direction_samples(output,*zroi)
                    assert (loaded is None and result['count']==0) or len(loaded['presence'])==result['count']
                    if repeat>=0:row['arms'][name]['seconds'].append(elapsed)
                    row['arms'][name]['exact']=True;row['arms'][name]['output_bytes']=output.stat().st_size
            row['output']=reference
            for arm in row['arms'].values():arm['median_seconds']=float(np.median(arm['seconds']))
            rows.append(row);(args.out/'stage_results.json').write_text(json.dumps(rows,indent=2));print(v['scroll'],{n:round(a['median_seconds'],4) for n,a in row['arms'].items()},flush=True)
        # No stored fixture chunks in first slice: original raises, streamed output is valid empty.
        v=manifest[0];url=prefix+urlparse(v['manifest_url']).path;empty={}
        for name in ['upstream','stream']:
            output=args.out/(name+'_empty.npz')
            try:
                with contextlib.redirect_stdout(open(os.devnull,'w')):arms[name].extract(url,(0,1),output,overwrite=True)
                empty[name]={'status':'written','count':hashes(output)['count']}
            except Exception as e:empty[name]={'status':'error','type':type(e).__name__,'message':str(e)}
        (args.out/'empty_results.json').write_text(json.dumps(empty,indent=2));print('empty',empty)
    finally:
        server.shutdown();server.server_close();thread.join();socket.getaddrinfo=old_dns
        if old_proxy is None:os.environ.pop('NO_PROXY',None)
        else:os.environ['NO_PROXY']=old_proxy
if __name__=='__main__':main()
