"""Boards from actual Blender renders and actual Unreal capture pixels."""
import json,re
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Art/FurStudy'
FONT='C:/Windows/Fonts/segoeui.ttf'
title=ImageFont.truetype(FONT,32);heading=ImageFont.truetype(FONT,26);small=ImageFont.truetype(FONT,19)
variants=['smooth','painted','tufted'];species=['little_dog','housecat']
manifest={row['key']:row for row in json.loads((OUT/'study-manifest.json').read_text())}

def board(label):
    im=Image.new('RGB',(2100,1650),'#253139');d=ImageDraw.Draw(im)
    d.text((35,20),'nUthEck | Restrained fur study | '+label,font=title,fill='#eddfc3')
    d.text((35,67),'Same base geometry and coat palette. No hair strands, fur shells or alpha cards.',font=small,fill='#bac6c9')
    for col,text in enumerate(['Current smooth paint','Painted fur texture','Painted fur + sparse clumps']):
        d.text((65+680*col,115),text,font=heading,fill='#dfc59b')
    return im,d

def put_image(board,im,box,nearest=False):
    im=im.convert('RGBA');im.thumbnail((box[2],box[3]),Image.Resampling.NEAREST if nearest else Image.Resampling.LANCZOS)
    board.paste(im,(box[0]+(box[2]-im.width)//2,box[1]+(box[3]-im.height)//2),im)

im,d=board('actual Blender renders')
for row,name in enumerate(species):
    y=172+row*710;d.text((35,y),name.replace('_',' ').title(),font=heading,fill='#eddfc3')
    photos=[Image.open(OUT/(name+'_'+v+'-close.png')).convert('RGBA') for v in variants]
    boxes=[p.getchannel('A').getbbox() for p in photos]
    bounds=(min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes))
    for col,v in enumerate(variants):
        x=35+col*680;key=name+'_'+v
        put_image(im,photos[col].crop(bounds),(x,y+40,620,445))
        d.text((x+35,y+500),'64 x 64 gameplay sample',font=small,fill='#bac6c9')
        d.text((x+330,y+500),'16 x 16 level sample',font=small,fill='#bac6c9')
        for suffix,at in [('gameplay',x+110),('level',x+385)]:
            p=Image.open(OUT/(key+'-'+suffix+'.png')).convert('RGBA').resize((128,128),Image.Resampling.NEAREST)
            im.paste(p,(at,y+530),p)
        extra=manifest[key]['added_triangles']
        d.text((x+40,y+665),f'Extra triangles: {extra}',font=small,fill='#dfc59b')
d.text((35,1615),'Low-resolution samples are actual renders, enlarged with nearest-neighbour. Existing draft meshes still need final LOD work.',font=small,fill='#bac6c9')
im.save(OUT/'FurComparison-Blender.png')

paths=[OUT/('Unreal-'+v+'.png') for v in ['close','gameplay','level']]
if all(p.exists() for p in paths):
    anchors={}
    for view in ['close','gameplay','level']:
        log=(ROOT/('build-fur-'+view+'.log')).read_text(encoding='utf-8',errors='replace')
        anchors[view]={m[0]:(float(m[1]),float(m[2])) for m in re.findall(r'FUR_STUDY_MESH (\w+).*?anchor_x=([\d.]+) anchor_y=([\d.]+)',log)}
        assert len(anchors[view])==6
    sources={view:Image.open(OUT/('Unreal-'+view+'.png')).convert('RGB') for view in anchors}
    im,d=board('actual Unreal renders')
    for row,name in enumerate(species):
        y=172+row*710;d.text((35,y),name.replace('_',' ').title(),font=heading,fill='#eddfc3')
        for col,v in enumerate(variants):
            x=35+col*680;key=name+'_'+v;ax,ay=anchors['close'][key]
            crop=sources['close'].crop((round(ax-205),round(ay-195),round(ax+205),round(ay+165)))
            put_image(im,crop,(x,y+40,620,445))
            for view,offset,size in [('gameplay',110,90),('level',385,15)]:
                ax,ay=anchors[view][key]
                crop=sources[view].crop((round(ax-size),round(ay-size),round(ax+size),round(ay+size)))
                crop=crop.resize((128,128),Image.Resampling.NEAREST)
                im.paste(crop,(x+offset,y+530))
            d.text((x+35,y+500),'Gameplay camera scale',font=small,fill='#bac6c9')
            d.text((x+330,y+500),'Whole-level camera scale',font=small,fill='#bac6c9')
            d.text((x+40,y+665),'Extra triangles: '+str(manifest[key]['added_triangles']),font=small,fill='#dfc59b')
    d.text((35,1615),'Crops of real staged engine captures at 680 / 1211 / 9700 cm camera widths. Small-scale samples enlarged nearest-neighbour.',font=small,fill='#bac6c9')
    im.save(OUT/'FurComparison-Unreal.png')
print('FUR_COMPARISONS_READY')
