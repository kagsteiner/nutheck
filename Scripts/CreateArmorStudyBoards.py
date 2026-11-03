from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
out=Path(__file__).resolve().parents[1]/'Art/ObjectInterpretations'
keys=['leather_armor','studded_leather_armor','chain_mail','banded_mail','elven_mithril_coat','dwarvish_mithril_coat','dwarvish_cloak']
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',24)
for title,suffixes in [('Models',['three-quarter']),('Rear',['rear']),('Details',['front','underside'])]:
    b=Image.new('RGB',(1600,1000 if title!='Details' else 1800),'#27333b');d=ImageDraw.Draw(b)
    for i,key in enumerate(keys):
        x=(i%4)*400;y=(i//4)*(490 if title!='Details' else 890)
        d.text((x+12,y+12),key.replace('_',' '),font=font,fill='#e9d9bd')
        for j,suffix in enumerate(suffixes):
            im=Image.open(out/(key+'-'+suffix+'.png')).convert('RGBA');im.thumbnail((390,410));b.paste(im,(x+5,y+55+j*420),im)
    b.save(out/('ArmorStudy-'+title+'.png'))
reports=json.loads((out/'projection-report-armor-study.json').read_text())+json.loads((out/'projection-report-dwarvish-cloak.json').read_text())
b=Image.new('RGB',(1400,1600),'#27333b');d=ImageDraw.Draw(b)
for i,r in enumerate(reports):
    y=i*225;d.text((12,y+4),r['key'].replace('_',' '),font=font,fill='white')
    for j,c in enumerate(r['candidates']):
        im=Image.open(out/c['file']).convert('RGBA').resize((160,160),Image.Resampling.NEAREST);b.paste(im,(j*210+12,y+42),im)
b.save(out/'ArmorStudy-Projections.png');print('ARMOR_STUDY_BOARDS_READY')
