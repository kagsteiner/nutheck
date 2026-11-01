"""Small, tileable brush-stroke modulation/normal maps, not photographic hair."""
from pathlib import Path
import math,random
import numpy as np
from PIL import Image,ImageDraw,ImageFilter

OUT=Path(__file__).resolve().parents[1]/'Art/FurStudy/Textures'
OUT.mkdir(parents=True,exist_ok=True)
size=512;rng=random.Random(417)
height=Image.new('L',(size,size),128);draw=ImageDraw.Draw(height)
# Strokes run along U. Wrapped copies keep the repeat seam quiet.
for i in range(1850):
    x=rng.randrange(size);y=rng.randrange(size)
    length=rng.randrange(9,29);slope=rng.uniform(-.16,.16)
    value=rng.choice([108,114,120,137,143,149]);width=rng.choice([1,1,2,3])
    for dx in [-size,0,size]:
        for dy in [-size,0,size]:
            draw.line([(x+dx,y+dy),(x+dx+length*.55,y+dy+slope*length*.45),
                       (x+dx+length,y+dy+slope*length)],fill=value,width=width)
height=height.filter(ImageFilter.GaussianBlur(.65))
h=np.asarray(height,dtype=np.float32)/255
# Mean 0.5, multiplied by two in both renderers; preserve broad coat colours.
modulation=np.clip(.5+(h-h.mean())*.95,.43,.57)
Image.fromarray(np.uint8(np.rint(modulation*255))).convert('RGB').save(OUT/'FurBrush.png')
dx=(np.roll(h,-1,axis=1)-np.roll(h,1,axis=1))*.5
dy=(np.roll(h,-1,axis=0)-np.roll(h,1,axis=0))*.5
normal=np.stack([-dx*2,dy*2,np.ones_like(h)],axis=-1)
normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
Image.fromarray(np.uint8(np.rint((normal*.5+.5)*255))).save(OUT/'FurBrushNormal.png')
print('FUR_TEXTURES_READY size=512 two_shared_maps=True')
