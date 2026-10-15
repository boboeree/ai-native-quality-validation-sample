from pathlib import Path
import os,sys,subprocess,time,json,base64,urllib.parse,signal,select,hashlib,re
D=Path(__file__).resolve().parent;O=D/'artifacts';O.mkdir(exist_ok=True)
secrets=[os.environ.get(x,'') for x in ['LT_USERNAME','LT_ACCESS_KEY']]
if not all(secrets):
 print('Missing required credential environment variables; no session launched.');sys.exit(2)
variants=[*secrets,base64.b64encode(':'.join(secrets).encode()).decode()]
variants += [urllib.parse.quote(x,safe='') for x in variants]
def redact(s):
 for v in sorted(set(variants),key=len,reverse=True):
  if v:s=s.replace(v,'[REDACTED]')
 return s
for n in ['TESTMU_RUN_TARGET','TESTMU_SMART','BUILD','TESTMU_HEADLESS']:print(n+'='+os.environ.get(n,''),flush=True)
print('Credentials: present (values hidden). Exactly one Python execution; no retry.',flush=True)
start=time.time();cmd=[sys.executable,'test.py'];p=subprocess.Popen(cmd,cwd=D/'python',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=os.environ.copy(),start_new_session=True);output=[];deadline=180
while True:
 if time.time()-start>deadline:
  os.killpg(p.pid,signal.SIGTERM);output.append('WALL_TIMEOUT_180_SECONDS\n');break
 if select.select([p.stdout],[],[],.5)[0]:
  b=os.read(p.stdout.fileno(),65536)
  if not b:break
  s=redact(b.decode('utf8','replace'));output.append(s);print(s,end='',flush=True)
 if p.poll() is not None:break
try:code=p.wait(timeout=20)
except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);code=p.wait()
rest=redact(p.stdout.read().decode('utf8','replace'));output.append(rest);print(rest,end='',flush=True)
log=''.join(output);(O/'runtime-sanitized.log').write_text(log)
result={'command':'python test.py','exit_code':code,'elapsed_s':round(time.time()-start,3),'build':os.environ['BUILD'],'run_target':os.environ['TESTMU_RUN_TARGET'],'smart':os.environ['TESTMU_SMART'],'python_test_sha256':hashlib.sha256((D/'python/test.py').read_bytes()).hexdigest(),'test_pass': '[TEST PASS]' in log,'test_fail':'[TEST FAIL]' in log,'vision_results':re.findall(r'\[vision_query\] result=(.*)',log),'no_retry':True,'cloud_session_budget':0,'local_execution_budget':1,'javascript_executed':False}
(O/'result.json').write_text(json.dumps(result,indent=2));print('EXPORT_RUNTIME_RESULT',json.dumps(result),flush=True)
if os.environ.get('GITHUB_STEP_SUMMARY'):
 with open(os.environ['GITHUB_STEP_SUMMARY'],'a') as f:f.write('## Original Kane export runtime\n\n```json\n'+json.dumps(result,indent=2)+'\n```\n')
sys.exit(code)
