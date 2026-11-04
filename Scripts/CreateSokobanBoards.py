"""Labelled review boards from real saved-model renders, never concept images."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
out=Path(__file__).resolve().parents[1]/'Art/Sokoban';font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',20)
keys=['soko_wall','soko_floor','soko_boulder','soko_pit','soko_hole','soko_frame','soko_trim','soko_lamp']
for title,suffix in [('Models','three-quarter'),('Rear','rear'),('Front','front'),('Underside','underside')]:
    b=Image.new('RGB',(1400,740),'#27333b');d=ImageDraw.Draw(b)
    for i,k in enumerate(keys):
        x=(i%4)*350;y=(i//4)*370;d.text((x+12,y+10),k.replace('soko_','').replace('_',' '),font=font,fill='#e9d9bd')
        im=Image.open(out/(k+'-'+suffix+'.png')).convert('RGBA');im=im.crop(im.getbbox());im.thumbnail((325,320));b.paste(im,(x+(350-im.width)//2,y+42+(320-im.height)//2),im)
    b.save(out/('Sokoban-'+title+'.png'))
b=Image.new('RGB',(1150,8*170),'#27333b');d=ImageDraw.Draw(b)
for i,r in enumerate(json.loads((out/'projection-report.json').read_text())):
    y=i*170;d.text((10,y+4),r['key'],font=font,fill='white')
    for j,c in enumerate(r['candidates']):
        im=Image.open(out/c['file']).convert('RGBA');assert im.size==(16,16);im=im.resize((128,128),Image.Resampling.NEAREST);b.paste(im,(j*185+10,y+32),im)
b.save(out/'Sokoban-Projections.png');print('SOKOBAN_BOARDS_READY')
