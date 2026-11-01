"""Extract labelled official tile references without guessing atlas positions."""
import csv
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Art/Studies/01-MiniatureDungeon'
OUT.mkdir(parents=True,exist_ok=True)
rows=[]
tiles={}
for category in ['monsters','objects','other']:
    source=ROOT/'upstream/NetHack/win/share'/f'{category}.txt'
    text=source.read_text()
    palette={m[0]:tuple(map(int,m[1:])) for m in re.findall(r'^(\S)\s*=\s*\(\s*(\d+),\s*(\d+),\s*(\d+)\s*\)',text,re.M)}
    for number,name,pixels in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',text,re.M):
        lines=[line.strip() for line in pixels.strip().splitlines()]
        if not lines or any(len(line)!=len(lines[0]) for line in lines):
            raise ValueError(f'Inconsistent tile: {category}/{number}')
        im=Image.new('RGB',(len(lines[0]),len(lines)))
        im.putdata([palette[ch] for line in lines for ch in line])
        key=f'{category}:{number}'
        tiles[(category,name)]=im
        rows.append(dict(reference_key=key,name=name,category=category,
            source=f'upstream/NetHack/win/share/{category}.txt',
            model_family='',asset='',status='reference only'))
with (OUT/'OfficialTileCatalogue.csv').open('w',newline='',encoding='utf-8') as stream:
    writer=csv.DictWriter(stream,fieldnames=rows[0]); writer.writeheader(); writer.writerows(rows)

selected=[('monsters',name) for name in ['giant ant,male','little dog,male','kitten,male','goblin,male','orc,male','blue jelly,male','floating eye,male','red dragon,male']]
sheet=Image.new('RGB',(1440,760),'#192329'); draw=ImageDraw.Draw(sheet)
font_path='C:/Windows/Fonts/segoeui.ttf'
title=ImageFont.truetype(font_path,30); font=ImageFont.truetype(font_path,20)
small=ImageFont.truetype(font_path,17)
draw.text((36,24),'nUthEck | Official NetHack 5.0 tile references',font=title,fill='#e4d3b7')
draw.text((36,72),'Original pixels, enlarged without smoothing. Names come from the source, not image recognition.',font=small,fill='#9fb2b7')
for i,key in enumerate(selected):
    x=36+(i%4)*350; y=125+(i//4)*295
    draw.rounded_rectangle((x,y,x+320,y+270),radius=12,fill='#263238')
    im=tiles[key].resize((160,160),Image.Resampling.NEAREST)
    sheet.paste(im,(x+80,y+16))
    draw.text((x+18,y+192),key[1].replace(',male',''),font=font,fill='#e4d3b7')
    family={'giant ant,male':'Insect / articulated legs','little dog,male':'Quadruped / fur','kitten,male':'Quadruped / fur','goblin,male':'Small humanoid','orc,male':'Humanoid / armour','blue jelly,male':'Amorphous / soft surface','floating eye,male':'Floating / organic','red dragon,male':'Winged reptile'}[key[1]]
    draw.text((x+18,y+226),family,font=small,fill='#9fb2b7')
draw.text((36,725),'Reference keys are file-local tile indices; runtime glyph mapping must use the compiled NetHack mapping.',font=small,fill='#9fb2b7')
sheet.save(OUT/'OfficialTileReferences.png')
(OUT/'catalogue-summary.json').write_text(json.dumps({'total_reference_tiles':len(rows),'counts':{c:sum(r['category']==c for r in rows) for c in ['monsters','objects','other']}},indent=2))
print(f'TILE_CATALOGUE_READY tiles={len(rows)}')
