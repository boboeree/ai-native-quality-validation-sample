from pathlib import Path
import ast,json,hashlib
D=Path(__file__).resolve().parent
p=D/'python/test.py';r=ast.parse(p.read_text());calls=[x for x in ast.walk(r) if isinstance(x,ast.Call)]
print('Original export TC-6: Python and JavaScript, both Playwright with TestMu bindings')
print('Python entry: python test.py -> testmu.run(test)')
print('Python dependencies:\n'+(D/'python/requirements.txt').read_text())
j=json.load(open(D/'javascript/package.json'));print('JavaScript entry:',j['scripts']['start']);print('JavaScript dependencies:',json.dumps(j['dependencies']))
print('Business code preserved; Python SHA256:',hashlib.sha256(p.read_bytes()).hexdigest())
print('Recorded calls: steps=',sum(ast.unparse(x.func)=='testmu.step' for x in calls),'vision_query=',sum(ast.unparse(x.func)=='testmu.vision_query' for x in calls),'assertions=',sum(ast.unparse(x.func)=='testmu.verify_assertion' for x in calls))
print('Required execution settings: TESTMU_RUN_TARGET=cloud, TESTMU_SMART=1, LT_USERNAME, LT_ACCESS_KEY')
print('No credential values are inspected or printed. .env.example contains blanks only.')
print('Scope: one Python cloud execution. JavaScript is syntax/dependency audited, not executed.')
