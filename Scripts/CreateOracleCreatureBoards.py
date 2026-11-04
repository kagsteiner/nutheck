"""Boards contain only unchanged official tiles and actual saved-mesh renders."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
O=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
def panel(board,name,label,box,tiny=False):
 x,y,w,h=box;im=Image.open(O/name).convert('RGBA')
 im.thumbnail((w,h-38),Image.Resampling.NEAREST if tiny else Image.Resampling.LANCZOS)
 if tiny:im=Image.open(O/name).convert('RGBA').resize((min(w,h-38),)*2,Image.Resampling.NEAREST)
 board.paste(im,(x+(w-im.width)//2,y+38+(h-38-im.height)//2),im)
 ImageDraw.Draw(board).text((x+10,y+8),label,font=small,fill='white')
b=Image.new('RGB',(1440,1040),(27,30,34));d=ImageDraw.Draw(b);d.text((20,12),'Oracle — actual static sculpt / source tile interpretation',font=font,fill='white')
for name,label,box in [('oracle-three-quarter.png','Three-quarter',(0,50,480,500)),('oracle-rear.png','Rear',(480,50,480,500)),('oracle-front.png','Front',(960,50,480,500)),('oracle-face.png','Fitted eyes / chanting face',(0,550,480,470)),('oracle-profile.png','Complete profile',(480,550,480,470)),('oracle-underside.png','Crossed legs / underside',(960,550,480,470))]:panel(b,name,label,box)
b.save(O/'Oracle-Review.png')
r=json.loads((O/'projection-report-oracle.json').read_text())[0]
b=Image.new('RGB',(1440,800),(27,30,34));d=ImageDraw.Draw(b);d.text((20,12),'Unchanged official source and true 16 × 16 geometry projections',font=font,fill='white')
entries=[('oracle-female-official.png','Official female (identical male)')]+[(c['file'],f"yaw {c['yaw']} / elevation {c['elevation']} / IoU {c['silhouette_iou']}") for c in r['candidates']]
for i,(name,label) in enumerate(entries):panel(b,name,label,((i%4)*360,55+(i//4)*360,360,350),True)
d.text((20,780),'Black mouth retained; offset cast shadow excluded by reviewed spatial mask. Shape scores are diagnostic only.',font=small,fill='white');b.save(O/'Oracle-Projections.png')
print('ORACLE_REVIEW_BOARDS_READY')
