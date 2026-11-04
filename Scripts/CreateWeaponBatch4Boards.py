from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
out=Path(__file__).resolve().parents[1]/'Art/ObjectInterpretations';keys=['silver_saber','broadsword','two_handed_sword'];font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',24)
for title,suffix in [('Models','three-quarter'),('Rear','rear'),('Front','front'),('Hilts','hilt'),('Underside','underside')]:
    b=Image.new('RGB',(1500,800),'#27333b');d=ImageDraw.Draw(b)
    for i,k in enumerate(keys):
        d.text((i*500+20,15),k.replace('_',' '),font=font,fill='#e9d9bd');im=Image.open(out/(k+'-'+suffix+'.png')).convert('RGBA');im=im.crop(im.getbbox());im.thumbnail((450,690));b.paste(im,(i*500+(500-im.width)//2,60+(690-im.height)//2),im)
    b.save(out/('WeaponBatch4-'+title+'.png'))
b=Image.new('RGB',(1300,690),'#27333b');d=ImageDraw.Draw(b);report=json.loads((out/'projection-report-weapon-batch4.json').read_text())
for i,r in enumerate(report):
    y=i*225;d.text((10,y+5),r['key'].replace('_',' '),font=font,fill='white')
    for j,c in enumerate(r['candidates']):
        im=Image.open(out/c['file']).convert('RGBA').resize((165,165),Image.Resampling.NEAREST);b.paste(im,(j*210+10,y+45),im)
b.save(out/'WeaponBatch4-Projections.png');print('WEAPON_BATCH4_BOARDS_READY')
