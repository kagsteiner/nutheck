"""Deterministic comparison of official pixels and actual Blender renders."""
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'Art/SpecialBatch2'
text=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text()
palette={m[0]:tuple(map(int,m[1:])) for m in re.findall(r'^(\S)\s*=\s*\(\s*(\d+),\s*(\d+),\s*(\d+)\s*\)',text,re.M)}
tiles={}
for category in ['monsters','objects','other']:
    raw=(ROOT/f'upstream/NetHack/win/share/{category}.txt').read_text(encoding='utf-8')
    for number,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)[^{]*\{([^}]+)\}',raw,re.M):
        tiles[name]=[r.strip() for r in rows.strip().splitlines()]
report=json.loads((OUT/'projection-report-special2.json').read_text())
board=Image.new('RGB',(1600,2575),'#1c252b'); draw=ImageDraw.Draw(board)
font='C:/Windows/Fonts/segoeui.ttf'
title=ImageFont.truetype(font,32); heading=ImageFont.truetype(font,24); small=ImageFont.truetype(font,18)
draw.text((32,20),'nUthEck | Six interpretations of the default tiles',font=title,fill='#e9d9bd')
draw.text((32,67),'Actual Blender geometry and renders. First anatomical drafts; shared-sex shopkeeper and five native altar appearances; unrigged static candidates.',font=small,fill='#abbcc3')
for x,label in [(32,'Official tile'),(294,'3D rendered at 16 x 16'),(574,'Three-quarter model'),(1110,'Rear model')]:
    draw.text((x,110),label,font=heading,fill='#c9b28a')
for row,entry in enumerate(report):
    y=157+row*395; key=entry['key']; name=key.replace('_',' ')
    draw.rounded_rectangle((20,y,1580,y+375),radius=12,fill='#27333b')
    draw.text((36,y+15),name.title(),font=heading,fill='#e9d9bd')
    lines=tiles['shopkeeper,male' if key=='shopkeeper' else key[6:]+' altar']; source=Image.new('RGB',(len(lines[0]),len(lines)))
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
    notes={key:('One shared official male/female icon; black hat, blue/cyan jacket, green trousers.' if key=='shopkeeper' else 'Native displayed '+key[6:]+' altar; static stone, no hidden deity or allegiance lookup.')}
    draw.text((36,y+341),notes[key],font=small,fill='#abbcc3')
draw.text((32,2540),'Six camera poses per creature tested for silhouette overlap. These are comparisons, not exact pixel reconstructions.',font=small,fill='#abbcc3')
board.save(OUT/'SpecialBatch2-Comparison.png')

# Compact actual models, all true 16x16 candidates and paired head views.
models=Image.new('RGB',(1500,1240),'#27333b');md=ImageDraw.Draw(models)
projections=Image.new('RGB',(1500,1370),'#27333b');pd=ImageDraw.Draw(projections)
heads=Image.new('RGB',(1500,1990),'#27333b');hd=ImageDraw.Draw(heads)
pd.text((20,12),'Official tile and all six actual 16 x 16 camera candidates (nearest-neighbour enlargement)',font=heading,fill='#e9d9bd')
hd.text((20,12),'Actual saved geometry | close detail views',font=heading,fill='#e9d9bd')
for row,entry in enumerate(report):
    key=entry['key'];md.text(((row%3)*500+20,(row//3)*620+15),key.replace('_',' ').title(),font=heading,fill='#e9d9bd')
    image=Image.open(OUT/(key+'-three-quarter.png')).convert('RGBA');image.thumbnail((490,560))
    models.paste(image,((row%3)*500+(500-image.width)//2,(row//3)*620+55),image)
    y=62+row*210
    source=Image.open(OUT/(key+'-official.png')).resize((160,160),Image.Resampling.NEAREST)
    projections.paste(source,(20,y));pd.text((20,y+166),key.replace('_',' '),font=small,fill='#e9d9bd')
    for col,candidate in enumerate(entry['candidates']):
        x=220+col*210;image=Image.open(OUT/candidate['file']).convert('RGBA').resize((160,160),Image.Resampling.NEAREST)
        projections.paste(image,(x,y),image)
        pd.text((x,y+166),f"{candidate['yaw']} / {candidate['elevation']}",font=small,fill='#abbcc3')
    for col,view in enumerate(['front','profile']):
        image=Image.open(OUT/(key+'-head-'+view+'.png')).convert('RGBA');image.thumbnail((450,300))
        heads.paste(image,(420+col*500,55+row*320),image)
    hd.text((20,160+row*320),key.replace('_',' ').title(),font=heading,fill='#e9d9bd')
models.save(OUT/'SpecialBatch2-Models.png');projections.save(OUT/'SpecialBatch2-Projections.png');heads.save(OUT/'SpecialBatch2-EyeReview.png')
print('CREATURE_COMPARISON_READY')

