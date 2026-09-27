"""Synthetic software smoke test, not satellite data or model evidence."""
from pathlib import Path
import numpy as np
from PIL import Image
from baseline import run
root=Path(__file__).resolve().parents[1]
p=root/'outputs'/'synthetic_demo'; p.mkdir(parents=True,exist_ok=True)
a=np.full((256,256,3),70,dtype=np.uint8); a[30:90,25:90]=150
b=a.copy(); b[130:195,140:220]=230
truth=np.zeros((256,256),dtype=np.uint8); truth[130:195,140:220]=255
for name,arr in [('before',a),('after',b),('label',truth)]: Image.fromarray(arr).save(p/f'{name}.png')
r=run(p/'before.png',p/'after.png',p,0.2,p/'label.png')
assert r['metrics']['iou']==1.0
print('PASS: synthetic sanity check only; not a real-world performance result.')
print(f'View {p / "before_after_overlay.png"}')
