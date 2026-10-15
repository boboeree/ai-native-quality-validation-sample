"""Restore the exact audited replay assets. Refuses different existing files."""
from pathlib import Path
import hashlib,json,shutil
here=Path(__file__).resolve().parent
root=here.parents[1]
manifest=json.loads((here/'asset-sha256.json').read_text())
for rel,want in manifest.items():
    src=here/rel
    assert hashlib.sha256(src.read_bytes()).hexdigest()==want, rel
    dst=root/'.testmuai'/Path(rel).relative_to('assets')
    if dst.exists():
        assert dst.read_bytes()==src.read_bytes(), f'Refuse overwriting existing local asset: {dst}'
    else:
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,dst)
    print('verified',dst.relative_to(root))
print('Ready: 6 exact audited assets restored; no login/config/context altered')
