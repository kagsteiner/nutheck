"""Deterministic comparison of official pixels and actual Blender renders."""
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'Art/CreatureInterpretations'
text=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text()
palette={m[0]:tuple(map(int,m[1:])) for m in re.findall(r'^(\S)\s*=\s*\(\s*(\d+),\s*(\d+),\s*(\d+)\s*\)',text,re.M)}
tiles={name:[r.strip() for r in rows.strip().splitlines()] for number,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',text,re.M)}
report=json.loads((OUT/'projection-report-batch21.json').read_text())
board=Image.new('RGB',(1600,995),'#1c252b'); draw=ImageDraw.Draw(board)
font='C:/Windows/Fonts/segoeui.ttf'
title=ImageFont.truetype(font,32); heading=ImageFont.truetype(font,24); small=ImageFont.truetype(font,18)
draw.text((32,20),'nUthEck | Two interpretations of the default tiles',font=title,fill='#e9d9bd')
draw.text((32,67),'Actual Blender geometry and renders. First anatomical drafts; orc mummy and orc zombie; unrigged static candidates.',font=small,fill='#abbcc3')
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
        'orc_mummy':'Exact saved orc anatomy, fitted pale linen, red eyes and interpreted orange cloth accent; no held weapon.',
        'orc_zombie':'Exact saved orc anatomy, orange/brown clothes, cyan arms, green facial accents and shared sex appearance.',
    }
    draw.text((36,y+341),notes[key],font=small,fill='#abbcc3')
draw.text((32,961),'Six camera poses per creature tested for silhouette overlap. These are comparisons, not exact pixel reconstructions.',font=small,fill='#abbcc3')
board.save(OUT/'MeshComparison-batch21.png')

# Compact actual models, all true 16x16 candidates and paired head views.
models=Image.new('RGB',(1000,620),'#27333b');md=ImageDraw.Draw(models)
projections=Image.new('RGB',(1500,500),'#27333b');pd=ImageDraw.Draw(projections)
heads=Image.new('RGB',(1500,710),'#27333b');hd=ImageDraw.Draw(heads)
pd.text((20,12),'Official tile and all six actual 16 x 16 camera candidates (nearest-neighbour enlargement)',font=heading,fill='#e9d9bd')
hd.text((20,12),'Actual saved upright orc geometry | front and profile head review',font=heading,fill='#e9d9bd')
for row,entry in enumerate(report):
    key=entry['key'];md.text((row*500+20,15),key.replace('_',' ').title(),font=heading,fill='#e9d9bd')
    image=Image.open(OUT/(key+'-three-quarter.png')).convert('RGBA');image.thumbnail((490,560))
    models.paste(image,(row*500+(500-image.width)//2,55),image)
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
models.save(OUT/'Batch21-Models.png');projections.save(OUT/'Batch21-Projections.png');heads.save(OUT/'Batch21-EyeReview.png')
print('CREATURE_COMPARISON_READY')
