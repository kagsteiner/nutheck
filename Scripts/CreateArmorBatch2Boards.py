from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
from ArmorBatch2Config import GROUPS,OUT
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',22)
for title,keys,cols in [('Plate',GROUPS[:3],3),('Dragons',GROUPS[3:],5)]:
    for view in ['three-quarter','rear','front','underside']:
        rows=(len(keys)+cols-1)//cols;b=Image.new('RGB',(cols*360,rows*460),'#27333b');d=ImageDraw.Draw(b)
        for i,k in enumerate(keys):
            x=i%cols*360;y=i//cols*460;d.text((x+10,y+10),k.replace('_dragon_scale_mail',' dragon mail').replace('_',' '),font=font,fill='#e9d9bd')
            im=Image.open(OUT/(k+'-'+view+'.png')).convert('RGBA');im.thumbnail((350,405));b.paste(im,(x+5,y+45),im)
        b.save(OUT/('ArmorBatch2-'+title+'-'+view+'.png'))
report=json.loads((OUT/'projection-report-armor-batch2.json').read_text());b=Image.new('RGB',(1320,len(report)*200),'#27333b');d=ImageDraw.Draw(b)
for i,r in enumerate(report):
    y=i*200;d.text((10,y+4),r['key'].replace('_',' '),font=font,fill='white')
    for j,c in enumerate(r['candidates']):
        im=Image.open(OUT/c['file']).convert('RGBA').resize((150,150),Image.Resampling.NEAREST);b.paste(im,(j*210+10,y+40),im)
b.save(OUT/'ArmorBatch2-Projections.png');print('ARMOR_BATCH2_BOARDS_READY')
