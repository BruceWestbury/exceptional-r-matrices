#!/usr/bin/env python3
"""Run candidate checks; orchestration only, with deadlines and access tracing.
No research repository or Git-history input is used. Requires fresh output paths.
"""
import argparse,collections,hashlib,importlib.metadata,json,os,platform,re,shutil,signal,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'verification'
def read(p):return json.loads((ROOT/p).read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')

def main():
    global OUT
    ap=argparse.ArgumentParser();ap.add_argument('--run-name',default='verification');args=ap.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+',args.run_name):ap.error('run-name must be a simple directory name')
    run_name=args.run_name; OUT=ROOT/run_name
    os.chdir(ROOT);OUT.mkdir(exist_ok=False)
    stages=[];access=[];start=time.monotonic();success=True
    # Traces are scratch only. They can contain software-install paths and are not published.
    with tempfile.TemporaryDirectory(prefix='exceptional-audit-traces-') as scratch:
        def run(name,command,limit):
            t=time.monotonic();trace=Path(scratch)/(name+'.trace')
            invoked=['strace','-f','-qq','-e','trace=%file','-o',str(trace)]+command if shutil.which('strace') else command
            with (OUT/(name+'.stdout.txt')).open('w') as out,(OUT/(name+'.stderr.txt')).open('w') as err:
                child=subprocess.Popen(invoked,stdout=out,stderr=err,start_new_session=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PWD':str(ROOT),'OLDPWD':str(ROOT)})
                timeout=False
                try:code=child.wait(timeout=limit)
                except subprocess.TimeoutExpired:
                    timeout=True;os.killpg(child.pid,signal.SIGKILL);child.wait();code=-9
            paths=re.findall(r'"([^"\n]*)"',trace.read_text(errors='replace')) if trace.exists() else []
            forbidden=[p for p in paths if 'Dropbox' in p or '/E8Series/' in p or '/Zenodo/' in p] if os.environ.get('PUBLIC_ISOLATED')=='1' else []
            entry={'stage':name,'command':command,'wall_seconds':time.monotonic()-t,'limit_seconds':limit,'exit_code':code,'status':'TIMEOUT' if timeout else 'PASS' if code==0 else 'ERROR'}
            stages.append(entry);access.append({'stage':name,'traced':trace.exists(),'file_path_events':len(paths),'candidate_path_events':sum(p.startswith(str(ROOT)) for p in paths),'forbidden_research_path_attempts':len(forbidden)})
            print(name,entry['status'],f"{entry['wall_seconds']:.3f}s",flush=True)
            if code or forbidden:raise RuntimeError(name+' failed or attempted research access')
        try:
            run('structural',[sys.executable,'tools/validate_publication.py','--self-test','--output',f'{run_name}/structural.json'],60)
            for path,name in [('audits/c/a3_relations','ordinary'),('audits/c/a2_spectral','a2'),('benchmarks/flint_ybe','ybe')]:run('build_'+name,['make','-C',path],60)
            run('ordinary_a3',['audits/c/a3_relations/runner',f'{run_name}/ordinary_a3'],300)
            assert all(r['status']=='PASS' for r in read(f'{run_name}/ordinary_a3/results.json')['results'])
            run('a2_spectral',[sys.executable,'audits/run_a2_spectral.py','--results',run_name+'_results'],300)
            for lang in ('c','python'):assert all(r['status']=='PASS' for r in read(f'audits/{lang}/a2_spectral/{run_name}_results/results.json')['results'])
            run('c_ybe',['benchmarks/flint_ybe/runner',f'benchmarks/flint_ybe/{run_name}_results'],300)
            c=read(f'benchmarks/flint_ybe/{run_name}_results/results.json');assert c['all_eleven_pass']
            # Required reporting input for the unchanged Python runner.
            dest=ROOT/'benchmarks/flint_ybe/results.json'; prior=dest.read_bytes() if dest.exists() else None;shutil.copyfile(ROOT/f'benchmarks/flint_ybe/{run_name}_results/results.json',dest)
            try:
                run('python_ybe',[sys.executable,'audits/python/run.py','--output',f'{run_name}/python_ybe'],300)
                py=read(f'{run_name}/python_ybe/results.json');assert all(r['status']=='PASS' for r in py['results'])
            finally:
                if prior is not None:dest.write_bytes(prior)
            if shutil.which('sage'):run('sage',['sage','-python','examples/import_spectral.py'],60)
            else:stages.append({'stage':'sage','status':'NOT AVAILABLE','wall_seconds':0,'limit_seconds':60})
        except Exception as exc:
            success=False;stages.append({'stage':'suite','status':'ERROR','diagnostic':str(exc)})
        finally:
            # Remove only executables produced by the builds in this fresh candidate.
            for rel in ('audits/c/a2_spectral/verify','audits/c/a3_relations/verify','audits/c/a3_relations/runner','benchmarks/flint_ybe/verifier','benchmarks/flint_ybe/runner'):
                p=ROOT/rel
                if p.exists():p.unlink()
        counts=collections.Counter()
        for p in (OUT/'ordinary_a3').glob('rep_*.jsonl'):
            for line in p.read_text().splitlines():
                x=json.loads(line)
                if 'id' in x and 'status' in x:counts[x['status']]+=1
        versions={'python':platform.python_version(),'compiler':subprocess.check_output(['cc','--version'],text=True).splitlines()[0]}
        for p in ('python-flint','jsonschema','sympy'):
            try:versions[p]=importlib.metadata.version(p)
            except importlib.metadata.PackageNotFoundError:pass
        summary={'status':'PASS' if success else 'FAIL','suite_wall_seconds':time.monotonic()-start,'stages':stages,'ordinary_relation_counts':dict(counts),'versions':versions,'access_traces':access,'isolation':{'research_tree_hidden':os.environ.get('PUBLIC_ISOLATED')=='1','network_disabled':os.environ.get('PUBLIC_ISOLATED')=='1','candidate_mount':'/tmp/release' if os.environ.get('PUBLIC_ISOLATED')=='1' else 'not namespace-isolated','method':'bubblewrap mount namespace; research tree hidden; dynamic strace file-access monitoring' if os.environ.get('PUBLIC_ISOLATED')=='1' else 'tracing only; no namespace isolation claimed'},'generated_executables_removed':True}
        dump(OUT/'summary.json',summary)
        lines=['# Clean-checkout verification report','','Overall status: **'+summary['status']+'**. This is a clean curated directory, not yet a Git checkout.','', '| Stage | Status | Wall s | Hard limit s |','|---|---|---:|---:|']
        for s in stages:lines.append(f"| {s['stage']} | {s['status']} | {s.get('wall_seconds',0):.3f} | {s.get('limit_seconds','—')} |")
        lines+=['',f"Ordinary manifest results: {dict(counts)}.",'','All runners retain their 60-second per-representation/crossing limits and 300-second batch limits. Build times are separate. No timeout was extended. A runner status alone is insufficient: result JSON is checked for every representation. Failed stages stop the suite; missing stages are not counted as passing.','',f"Isolation: {summary['isolation']}",f"Forbidden research-path attempts found in access traces: {sum(a['forbidden_research_path_attempts'] for a in access)}.",'',('The namespace-isolated run hid the research tree and disabled networking. Software dependencies were visible read-only.' if os.environ.get('PUBLIC_ISOLATED')=='1' else 'This run used file tracing only; research-directory masking and networking isolation are not claimed.')+' Raw traces are ephemeral; generated executables are removed after testing.','',f"Dependency versions: {versions}",'','Exact per-representation time, peak RSS and residuals are retained in the worker JSON logs. No arithmetic is performed by this orchestrator. Source-provenance citations are not filesystem accesses. Historical source-comparison evidence is not described as rerun.','', 'The historical Python ordinary wrapper is excluded; C/FLINT covers the complete encoded ordinary manifest. See AUDIT_COVERAGE.md and PUBLICATION_DECISIONS.md for unresolved presentation/assembly and release questions.','', 'No Git history, licence grant, publication or deposit has been created.']
        (ROOT/'CLEAN_CHECKOUT_REPORT.md').write_text('\n'.join(lines)+'\n')
    return 0 if success else 1
if __name__=='__main__':sys.exit(main())
