"""Explicit local test-asset patch. Does not modify CLI, .context or result statuses."""
from pathlib import Path
import difflib, json, shutil, sys

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
internal = root/'.testmuai/tests/output-budget-category-shows-exactly-the-two-eligible-preview-2/.internal'
out.mkdir(parents=True, exist_ok=True)
code = "Array.from(el(0).querySelectorAll('.cursor-pointer.group')).filter(e => e.getClientRects().length > 0).length"
wrapped = "(els) => { const el = (i) => els[i]; return " + code + "; }"
query = "count all currently visible listing cards from a fresh DOM query rooted at the listings grid"
locator = 'div.grid.grid-cols-1'
changed=[]

def save(path, text):
    before=path.read_text()
    backup=out/'before-local-patch'/path.relative_to(internal)
    backup.parent.mkdir(parents=True,exist_ok=True)
    assert not backup.exists(), 'Refuse overwriting pre-patch evidence'
    backup.write_text(before)
    path.write_text(text)
    diff=''.join(difflib.unified_diff(before.splitlines(True),text.splitlines(True),fromfile='before/'+str(path.relative_to(internal)),tofile='after/'+str(path.relative_to(internal))))
    changed.append(diff)

files=list((internal/'steps').rglob('actions.ndjson'))
count=0
for path in files:
    rows=[json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    touched=False
    for row in rows:
        p=row.get('action_params',{})
        if row.get('action_type')!='analyze' or p.get('key')!='visible_listing_cards_count':continue
        assert p['expected_value']=='2'
        assert 'total properties' in str(p['locators']), 'Only patch the audited summary-based counter'
        p.update(code_js=code,wrapped_js=wrapped,locators=[locator],query=query)
        row['action_instruction']='Count all visible listing cards using a dynamic DOM collection'
        row['intent']=query
        touched=True;count+=1
    if touched:save(path,'\n'.join(json.dumps(x,ensure_ascii=False) for x in rows)+'\n')
assert count==1,count

path=internal/'execution.json'
doc=json.loads(path.read_text());count=0
for ins in doc['instructions']:
    for child in ins.get('children',[]):
        for op in child.get('operations',[]):
            if op.get('query_variable_name')!='visible_listing_cards_count' or op.get('command')!='TEXTUAL_ANALYZER':continue
            source=json.loads(op['sub_instruction_obj'])
            assert source['expected_value']=='2'
            source.update(code_js=code,wrapped_js=wrapped,locators=[locator],query=query,reasoning=query)
            source['operation']='Count all visible listing cards using a dynamic DOM collection'
            op['sub_instruction_obj']=json.dumps(source,ensure_ascii=False,separators=(',',':'))
            op['instruction']=source['operation'];op['intent']=query;op['reasoning']=query
            count+=1
assert count==1,count
save(path,json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
(out/'local-oracle-patch.diff').write_text('\n'.join(changed))
(out/'patched-count-oracle.json').write_text(json.dumps({'code_js':code,'wrapped_js':wrapped,'locators':[locator],'expected':'2','patch_kind':'Codex local generated test-asset repair; not vendor native AI output'},indent=2))
print('Patched only one count extraction in runtime recording and matching execution asset')
print('Selector:',locator)
print('JavaScript:',code)
print('Expected count remains 2; no assertion/result status/.context/global CLI modified')
print('Originals and exact diff:',out)
