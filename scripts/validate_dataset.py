"""Check paired filenames, image dimensions and binary mask encodings."""
import argparse
from pathlib import Path
import numpy as np
from PIL import Image
p=argparse.ArgumentParser(); p.add_argument('root',type=Path); args=p.parse_args()
for split in ['train','val','test']:
    dirs=[args.root/split/x for x in ['A','B','label']]
    sets=[{f.name for f in d.glob('*.png')} for d in dirs]
    if not sets[0] or not sets[0]==sets[1]==sets[2]:
        raise ValueError(f'{split}: missing PNG files or mismatched A/B/label filenames')
    for name in sorted(sets[0]):
        with Image.open(dirs[0]/name) as a, Image.open(dirs[1]/name) as b, Image.open(dirs[2]/name) as m:
            if not a.size==b.size==m.size: raise ValueError(f'{split}/{name}: dimensions differ')
            if not set(np.unique(np.asarray(m.convert("L")))).issubset({0,1,255}):
                raise ValueError(f'{split}/{name}: nonbinary mask')
    print(f'{split}: {len(sets[0])} pairs passed structural checks')
print('These checks do not verify alignment, duplicates, label accuracy or geographic independence.')
