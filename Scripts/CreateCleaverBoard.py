from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
out=Path(__file__).resolve().parents[1]/'Art/ObjectInterpretations'
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',24)
b=Image.new('RGB',(1600,1400),'#27333b');d=ImageDraw.Draw(b)
for i,label in enumerate(['three-quarter','rear','underside','detail']):
    x=i%2*800;y=i//2*590;d.text((x+18,y+12),'Cleaver | '+label,font=font,fill='#e9d9bd')
    im=Image.open(out/('cleaver-'+label+'.png')).convert('RGBA');im.thumbnail((780,540));b.paste(im,(x+10,y+50),im)
report=json.loads((out/'projection-report-cleaver.json').read_text())[0]
for i,c in enumerate(report['candidates']):
    im=Image.open(out/c['file']).convert('RGBA').resize((150,150),Image.Resampling.NEAREST);b.paste(im,(i*240+20,1210),im)
b.save(out/'Cleaver-Review.png');print('CLEAVER_REVIEW_BOARD_READY')
