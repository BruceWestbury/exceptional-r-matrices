#!/usr/bin/env python3
"""Run repository checks with deadlines and optional file-access tracing.
Use a fresh output directory for each run.
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
            entry={'stage':name,'command':command,'wall_seconds':time.monotonic()-t,'limit_seconds':limit,'exit_code':code,'status':'TIMEOUT' if timeout else 'PASS' if code==0 else 'ERROR'}
            stages.append(entry);access.append({'stage':name,'traced':trace.exists(),'file_path_events':len(paths),'repository_path_events':sum(p.startswith(str(ROOT)) for p in paths)})
            print(name,entry['status'],f"{entry['wall_seconds']:.3f}s",flush=True)
            if code:raise RuntimeError(name+' failed')
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
            # Remove executables produced by the builds.
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
        summary={'status':'PASS' if success else 'FAIL','suite_wall_seconds':time.monotonic()-start,'stages':stages,'ordinary_relation_counts':dict(counts),'versions':versions,'access_traces':access,'environment':{'filesystem':'isolated mount namespace' if os.environ.get('PUBLIC_ISOLATED')=='1' else 'local checkout','isolation_supplied':os.environ.get('PUBLIC_ISOLATED')=='1','file_access_tracing':shutil.which('strace') is not None},'generated_executables_removed':True}
        dump(OUT/'summary.json',summary)
        lines=['# Verification results', '',
               'Overall status: **'+summary['status']+'**. This report summarizes the C/Python suite.', '',
               '| Stage | Status | Wall s | Limit s |', '|---|---|---:|---:|']
        for stage in stages:
            lines.append(f"| {stage['stage']} | {stage['status']} | {stage.get('wall_seconds',0):.3f} | {stage.get('limit_seconds','—')} |")
        lines += ['', f"Ordinary relation results: {dict(counts)}.", '',
                  'The suite checks structural validity, ordinary A(3) relations, A(2) unitarity and crossing, '
                  'and generic Yang–Baxter identities. SageMath import is included when available. '
                  'Per-representation result records determine the reported mathematical status.', '',
                  'Workers have 60-second limits and batches have 300-second limits. '
                  'Build times are recorded separately. A failed stage stops the suite.', '',
                  ('Environment: isolated filesystem with local software dependencies.'
                   if os.environ.get('PUBLIC_ISOLATED')=='1' else
                   'Environment: the local checkout and installed software dependencies.'),
                  f"Stages with file-access tracing: {sum(a['traced'] for a in access)}.", '',
                  f"Dependency versions: {versions}", '',
                  f"[Full run summary]({run_name}/summary.json) records the environment and stage results. "
                  'Worker logs retain exact residuals, wall times and peak resident memory.', '',
                  'See [AUDIT_COVERAGE.md](AUDIT_COVERAGE.md) for the mathematical scope and '
                  '[macaulay2/README.md](macaulay2/README.md) for the separate package checks.', '',
                  'The repository uses [CC BY 4.0](LICENSE).']
        (ROOT/'CLEAN_CHECKOUT_REPORT.md').write_text('\n'.join(lines)+'\n')
    return 0 if success else 1
if __name__=='__main__':sys.exit(main())
