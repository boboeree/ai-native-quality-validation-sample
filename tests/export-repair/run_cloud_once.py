from pathlib import Path
import os,sys,subprocess,time,json,base64,urllib.parse,signal,select,hashlib,re,pty,fcntl,termios,struct
D=Path(__file__).resolve().parent;O=D/'artifacts';O.mkdir(exist_ok=True)
secrets=[os.environ.get(x,'') for x in ['LT_USERNAME','LT_ACCESS_KEY']]
if not all(secrets):print('Missing LT credential environment; no browser launched.');sys.exit(2)
variants=[*secrets,base64.b64encode(':'.join(secrets).encode()).decode()]
variants += [urllib.parse.quote(x,safe='') for x in variants]
def redact(s):
 for v in sorted(set(variants),key=len,reverse=True):
  if v:s=s.replace(v,'[REDACTED]')
 return s
results=[]
for lang,cmd in [('python',[sys.executable,'test-cloud.py'])]:
 out=O/lang;out.mkdir(exist_ok=True);events=[];chunks=[];start=time.time()
 header={'version':2,'width':132,'height':38,'timestamp':int(start),'title':f'Actual GitHub Runner {lang} repaired export execution','env':{'TERM':'xterm-256color'}}
 def emit(s):
  s=redact(s);events.append([round(time.time()-start,3),'o',s]);chunks.append(s);print(s,end='',flush=True)
 emit(f'RUNNER COMMAND: {" ".join(cmd)}\r\nMODE: Windows 10 cloud browser + smart AI; original assertions unchanged\r\n')
 master,slave=pty.openpty();fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',38,132,0,0))
 env=os.environ.copy();env['TERM']='xterm-256color'
 child=subprocess.Popen(cmd,cwd=D/lang,stdin=subprocess.DEVNULL,stdout=slave,stderr=slave,env=env,start_new_session=True);os.close(slave)
 deadline=180;timedout=False
 while True:
  if time.time()-start>deadline:
   os.killpg(child.pid,signal.SIGTERM);emit('WALL_TIMEOUT_180_SECONDS\r\n');timedout=True;break
  if select.select([master],[],[],.25)[0]:
   try:b=os.read(master,65536)
   except OSError:break
   if not b:break
   emit(b.decode('utf8','replace'))
  if child.poll() is not None:break
 try:code=child.wait(timeout=10)
 except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);code=child.wait()
 while select.select([master],[],[],.1)[0]:
  try:b=os.read(master,65536)
  except OSError:break
  if not b:break
  emit(b.decode('utf8','replace'))
 os.close(master);emit(f'\r\nCHILD_EXIT_CODE={code}\r\n')
 log=''.join(chunks);(out/'runtime.log').write_text(log);(out/'runtime.cast').write_text('\n'.join(json.dumps(e) for e in [header]+events)+'\n')
 result={'language':lang,'command':cmd,'exit_code':code,'duration_s':round(time.time()-start,3),'timed_out':timedout,'run_id':os.environ.get('GITHUB_RUN_ID'),'sha':os.environ.get('GITHUB_SHA'),'run_target':os.environ.get('TESTMU_RUN_TARGET'),'smart':os.environ.get('TESTMU_SMART'),'repaired_file_sha256':hashlib.sha256((D/lang/cmd[-1]).read_bytes()).hexdigest(),'vision_results':re.findall(r'\[vision_query\] result=(.*)',log),'test_pass':'[TEST PASS]' in log,'test_fail':'[TEST FAIL]' in log,'no_auto_retry':True,'cloud_browser_session_budget':1}
 (out/'result.json').write_text(json.dumps(result,indent=2));print('REPAIR_RESULT',json.dumps(result),flush=True);results.append(result)
(O/'pair-result.json').write_text(json.dumps(results,indent=2))
if os.environ.get('GITHUB_STEP_SUMMARY'):
 with open(os.environ['GITHUB_STEP_SUMMARY'],'a') as f:f.write('## Repaired exported code runtime\n\n```json\n'+json.dumps(results,indent=2)+'\n```\n')
sys.exit(0 if all(r['exit_code']==0 and r['test_pass'] for r in results) else 1)
