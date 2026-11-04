"""Review boards from untouched official tiles and actual centaur mesh renders."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import re,json
R=Path(__file__).resolve().parents[1];O=R/'Art/CreatureInterpretations';keys=['plains_centaur','forest_centaur','mountain_centaur']
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
def panel(b,name,label,x,y,w,h,tiny=False):
 im=Image.open(O/name).convert('RGBA');im.thumbnail((w,h-40),Image.Resampling.LANCZOS)
 if tiny:im=Image.open(O/name).convert('RGBA').resize((min(w,h-40),)*2,Image.Resampling.NEAREST)
 b.paste(im,(x+(w-im.width)//2,y+40+(h-40-im.height)//2),im);ImageDraw.Draw(b).text((x+8,y+8),label,font=small,fill='white')
b=Image.new('RGB',(1500,1050),(27,30,34));ImageDraw.Draw(b).text((20,12),'Centaur creatures and pure white marble statues — actual geometry',font=font,fill='white')
for i,k in enumerate(keys):
 panel(b,k+'-three-quarter.png',k.replace('_',' ')+' / living',i*500,50,500,500)
 panel(b,k+'-marble.png','Same geometry / uniform marble',i*500,550,500,500)
b.save(O/'Centaurs-Models.png')
b=Image.new('RGB',(1500,2050),(27,30,34));ImageDraw.Draw(b).text((20,12),'Saved sculpt inspection: front, face, rear and underside',font=font,fill='white')
for i,k in enumerate(keys):
 for j,view in enumerate(['front','face','rear','underside']):panel(b,k+'-'+view+'.png',k.replace('_',' ')+' / '+view,i*500,50+j*500,500,500)
b.save(O/'Centaurs-Details.png')
raw=(R/'upstream/NetHack/win/share/monsters.txt').read_text();palette={m[0]:tuple(map(int,m[1:])) for m in re.findall(r'^(\S)\s*=\s*\(\s*(\d+),\s*(\d+),\s*(\d+)\s*\)',raw,re.M)};tiles={n:[x.strip() for x in rows.strip().splitlines()] for _,n,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',raw,re.M)}
reports=json.loads((O/'projection-report-centaurs.json').read_text());b=Image.new('RGB',(1960,970),(27,30,34));ImageDraw.Draw(b).text((20,12),'Official source versus actual 16 × 16 projections / spatial shadow masks',font=font,fill='white')
for i,k in enumerate(keys):
 rows=tiles[k.replace('_',' ')+',male'];assert rows==tiles[k.replace('_',' ')+',female']
 im=Image.new('RGBA',(16,16));im.putdata([(*palette[c],0 if c=='.' else 255) for row in rows for c in row]);im.save(O/(k+'-official.png'))
 panel(b,k+'-official.png',k.replace('_',' ')+' / official',0,50+i*300,280,300,True)
 for j,c in enumerate(reports[i]['candidates']):panel(b,c['file'],f"{c['yaw']}° / {c['elevation']}° IoU {c['silhouette_iou']}",(j+1)*280,50+i*300,280,300,True)
ImageDraw.Draw(b).text((20,950),'Black upper anatomy retained; offset right/lower cast shadows excluded. Identical male/female source art shares each sculpt.',font=small,fill='white');b.save(O/'Centaurs-Projections.png')
print('CENTAUR_BOARDS_READY')
