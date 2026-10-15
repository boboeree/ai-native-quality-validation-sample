import fs from 'node:fs';
import assert from 'node:assert/strict';

const payload=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const run=Function('return ('+payload.wrapped_js+')')();
for(const [visible,hidden] of [[0,0],[1,0],[2,0],[3,0],[2,2]]) {
  let queries=0;
  const cards=Array.from({length:visible+hidden},(_,i)=>({getClientRects:()=>i<visible?[{}]:[]}));
  const grid={querySelectorAll(selector){assert.equal(selector,'.cursor-pointer.group');queries++;return cards;}};
  const actual=run([grid]);
  assert.equal(actual,visible);
  assert.equal(queries,1);
  const passes=String(actual)===payload.expected;
  assert.equal(passes,visible===2);
  console.log(`visible=${visible}, hidden=${hidden}: actual=${actual}, assertion=${passes?'PASS':'FAIL (expected rejection)'}`);
}
console.log('PASS: the actual patched extraction rejects 0/1/3 visible cards and counts a dynamic collection. Offline operator regression, not a browser session.');
