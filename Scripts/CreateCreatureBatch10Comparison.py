"""Deterministic comparison of official pixels and actual Blender renders."""
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'Art/CreatureInterpretations'
text=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text()
palette={m[0]:tuple(map(int,m[1:])) for m in re.findall(r'^(\S)\s*=\s*\(\s*(\d+),\s*(\d+),\s*(\d+)\s*\)',text,re.M)}
tiles={name:[r.strip() for r in rows.strip().splitlines()] for number,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',text,re.M)}
report=json.loads((OUT/'projection-report-batch10.json').read_text())
board=Image.new('RGB',(1600,1390),'#1c252b'); draw=ImageDraw.Draw(board)
font='C:/Windows/Fonts/segoeui.ttf'
title=ImageFont.truetype(font,32); heading=ImageFont.truetype(font,24); small=ImageFont.truetype(font,18)
draw.text((32,20),'nUthEck | Three interpretations of the default tiles',font=title,fill='#e9d9bd')
draw.text((32,67),'Actual Blender geometry and renders. First anatomical drafts; tiger and hell hounds; unrigged static candidates.',font=small,fill='#abbcc3')
for x,label in [(32,'Official tile'),(294,'3D rendered at 16 x 16'),(574,'Three-quarter model'),(1110,'Rear model')]:
    draw.text((x,110),label,font=heading,fill='#c9b28a')
for row,entry in enumerate(report):
    y=157+row*395; key=entry['key']; name=key.replace('_',' ')
    draw.rounded_rectangle((20,y,1580,y+375),radius=12,fill='#27333b')
    draw.text((36,y+15),name.title(),font=heading,fill='#e9d9bd')
    lines=tiles[name+',male']; source=Image.new('RGB',(len(lines[0]),len(lines)))
    source.putdata([palette[ch] for line in lines for ch in line])
    source.save(OUT/(key+'-official.png'))
    board.paste(source.resize((224,224),Image.Resampling.NEAREST),(36,y+65))
    pixel=Image.open(OUT/entry['best_projection']['file']).convert('RGBA')
    board.paste(pixel.resize((224,224),Image.Resampling.NEAREST),(300,y+65),pixel.resize((224,224),Image.Resampling.NEAREST))
    for suffix,x,width in [('three-quarter',570,500),('rear',1110,360)]:
        image=Image.open(OUT/(key+'-'+suffix+'.png')).convert('RGBA')
        image.thumbnail((width,320),Image.Resampling.LANCZOS)
        board.paste(image,(x+(width-image.width)//2,y+43),image)
    camera=entry['best_projection']
    draw.text((300,y+306),f"Pose: {camera['yaw']} deg / {camera['elevation']} deg",font=small,fill='#abbcc3')
    notes={
        'tiger':'Interpretation: powerful feline frame, wrapping tapered stripes, pale belly/cheeks and ringed tail.',
        'hell_hound_pup':'Interpretation: large juvenile head/paws, short muzzle/legs, orange-red coat, fitted red eyes and warm mouth.',
        'hell_hound':'Interpretation: taller strong adult canid, longer muzzle, orange-red coat, raised tail and fitted red eyes.',
    }
    draw.text((36,y+341),notes[key],font=small,fill='#abbcc3')
draw.text((32,1356),'Six camera poses per creature tested for silhouette overlap. These are comparisons, not exact pixel reconstructions.',font=small,fill='#abbcc3')
board.save(OUT/'MeshComparison-batch10.png')
print('CREATURE_COMPARISON_READY')
