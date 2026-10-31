#!/usr/bin/env python3
"""Resource-limited process launcher only; performs no mathematical evaluation."""
import argparse,json,os,signal,sys,time,hashlib,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TASKS=['X2','Y2','Y2_star','I','L','crossing']
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--backend',choices=['python','c','all'],default='all');ap.add_argument('--results',default='results');args=ap.parse_args()
    backends=['python','c'] if args.backend=='all' else [args.backend]
    dirs={b:ROOT/f'audits/{b}/a2_spectral'/args.results for b in backends}
    for d in dirs.values():d.mkdir(exist_ok=False)
    begin=time.monotonic();deadline=begin+300; all_passed=True
    for backend in backends:
        rows=[]
        for task in TASKS:
            start=time.monotonic();limit=min(60,deadline-start);out=dirs[backend]/(task+'.stdout.json');err=dirs[backend]/(task+'.stderr.txt')
            if limit<=0:
                rows.append({'task':task,'status':'TIMEOUT','reason':'batch budget exhausted before launch','attempted':False});all_passed=False;continue
            command=[sys.executable,str(ROOT/'audits/python/a2_spectral/verify.py'),task] if backend=='python' else [str(ROOT/'audits/c/a2_spectral/verify'),task]
            pid=os.fork()
            if pid==0:
                os.setsid();os.chdir(ROOT)
                with out.open('w') as a,err.open('w') as b:os.dup2(a.fileno(),1);os.dup2(b.fileno(),2)
                os.execv(command[0],command)
            expired=False
            while True:
                found,status,usage=os.wait4(pid,os.WNOHANG)
                if found:break
                if time.monotonic()-start>=limit:
                    expired=True
                    try:os.killpg(pid,signal.SIGKILL)
                    except ProcessLookupError:pass
                    found,status,usage=os.wait4(pid,0);break
                time.sleep(.005)
            try:result=json.loads(out.read_text())
            except (ValueError,OSError):result={'task':task,'status':'ERROR','diagnostic':err.read_text() if err.exists() else 'no diagnostic'}
            if expired:result={'task':task,'status':'TIMEOUT','limit_seconds':limit}
            elif os.waitstatus_to_exitcode(status)!=0 and result.get('status')!='FAIL':result['status']='ERROR'
            result.update(wall_seconds=time.monotonic()-start,peak_rss_kib=usage.ru_maxrss,limit_seconds=limit)
            rows.append(result);all_passed = all_passed and result['status']=='PASS';print(backend,task,result['status'],flush=True)
        version=subprocess.check_output(['cc','--version'],text=True).splitlines()[0] if backend=='c' else sys.version
        saved={'backend':backend,'version':version,'limits_seconds':{'per_worker':60,'combined_batch':300},'elapsed_from_combined_start':time.monotonic()-begin,'results':rows,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/f'audits/{backend}/a2_spectral').iterdir() if p.suffix in ('.py','.c','.h')}}
        (dirs[backend]/'results.json').write_text(json.dumps(saved,indent=2)+'\n')
    print('Combined seconds:',time.monotonic()-begin)
    return 0 if all_passed else 1
if __name__=='__main__':sys.exit(main())
