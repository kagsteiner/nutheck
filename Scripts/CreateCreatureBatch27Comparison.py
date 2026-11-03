"""Actual front/rear meshes, original sex tiles and eighteen true tiny renders."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
report=json.loads((out/'projection-report-batch27.json').read_text())
font='C:/Windows/Fonts/segoeui.ttf';title=ImageFont.truetype(font,28);small=ImageFont.truetype(font,18)
board=Image.new('RGB',(1600,1320),'#27333b');d=ImageDraw.Draw(board)
d.text((25,16),'Batch 27 | actual geometry, original sex tiles and 16 x 16 reverse projections',font=title,fill='#e9d9bd')
for x,t in [(25,'Official sex tile'),(270,'Best actual 16 x 16'),(540,'Front quarter'),(1090,'Rear')]:d.text((x,65),t,font=small,fill='white')
models=Image.new('RGB',(1500,620),'#27333b');md=ImageDraw.Draw(models)
proj=Image.new('RGB',(1500,710),'#27333b');pd=ImageDraw.Draw(proj)
heads=Image.new('RGB',(1200,960),'#27333b');hd=ImageDraw.Draw(heads)
for row,e in enumerate(report):
    key=e['key'];base=key.removesuffix('_female');sex='female' if key.endswith('_female') else 'male';y=110+row*400
    d.text((25,y),key.replace('_',' '),font=title,fill='#e9d9bd')
    im=Image.open(out/(base+'-'+sex+'-official.png'));board.paste(im.resize((210,210),Image.Resampling.NEAREST),(25,y+50))
    im=Image.open(out/e['best_projection']['file']).convert('RGBA').resize((210,210),Image.Resampling.NEAREST);board.paste(im,(280,y+50),im)
    for suffix,x in [('three-quarter',540),('rear',1080)]:
        im=Image.open(out/(key+'-'+suffix+'.png')).convert('RGBA');im.thumbnail((500,330));board.paste(im,(x,y+35),im)
    mx=(row%3)*500;my=(row//3)*500;md.text((mx+12,my+12),key.replace('_',' '),font=small,fill='white')
    im=Image.open(out/(key+'-three-quarter.png')).convert('RGBA');im.thumbnail((490,450));models.paste(im,(mx,my+40),im)
    py=15+row*225;pd.text((12,py),key.replace('_',' '),font=small,fill='white')
    im=Image.open(out/(base+'-'+sex+'-official.png'));proj.paste(im.resize((160,160),Image.Resampling.NEAREST),(12,py+28))
    for col,c in enumerate(e['candidates']):
        x=210+col*210;im=Image.open(out/c['file']).convert('RGBA').resize((160,160),Image.Resampling.NEAREST);proj.paste(im,(x,py+28),im)
        pd.text((x,py+190),str(c['yaw'])+' / '+str(c['elevation']),font=small,fill='white')
    hd.text((12,row*310+12),key.replace('_',' '),font=small,fill='white')
    for col,view in enumerate(['front','profile']):
        im=Image.open(out/(key+'-head-'+view+'.png')).convert('RGBA');im.thumbnail((400,285));heads.paste(im,(300+col*440,row*310+20),im)
board.save(out/'MeshComparison-batch27.png');models.save(out/'Batch27-Models.png');proj.save(out/'Batch27-Projections.png');heads.save(out/'Batch27-HeadReview.png')
underside=Image.new('RGB',(1500,550),'#27333b');ud=ImageDraw.Draw(underside)
for i,e in enumerate(report):
    key=e['key'];ud.text((i*500+15,15),key.replace('_',' ')+' | underside',font=small,fill='white')
    im=Image.open(out/(key+'-head-underside.png')).convert('RGBA');im.thumbnail((490,490));underside.paste(im,(i*500+5,55),im)
underside.save(out/'Batch27-UndersideReview.png')
print('CREATURE_BATCH27_COMPARISON_READY')

