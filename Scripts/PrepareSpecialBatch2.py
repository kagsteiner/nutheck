"""Review unmodified official tiles and protect all preceding canonical exports."""
import sys,json,hashlib,re
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from SpecialBatch2Config import *
tiles={};palettes={}
for category in ['monsters','other']:
    raw=(ROOT/f'upstream/NetHack/win/share/{category}.txt').read_text()
    palettes[category]={m[0]:tuple(map(int,m[1:])) for m in re.findall(r'^(\S)\s*=\s*\(\s*(\d+),\s*(\d+),\s*(\d+)\s*\)',raw,re.M)}
    for number,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)[^{]*\{([^}]+)\}',raw,re.M):tiles[name]=(category,int(number),[r.strip() for r in rows.strip().splitlines()])
board=Image.new('RGB',(1500,850),'#27333b');d=ImageDraw.Draw(board);font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',23)
labels=['shopkeeper,male','shopkeeper,female']+[k+' altar' for k in ALTARS]
for i,label in enumerate(labels):
    x=20+(i%4)*370;y=20+(i//4)*400;cat,num,rows=tiles[label]
    d.text((x,y),label,font=font,fill='white');d.text((x,y+30),cat+' tile '+str(num),font=font,fill='#cdb48c')
    im=Image.new('RGB',(16,16));im.putdata([palettes[cat][c] for row in rows for c in row]);im.save(OUT/(label.replace(',','-').replace(' ','_')+'-official.png'));board.paste(im.resize((288,288),Image.Resampling.NEAREST),(x,y+70))
board.save(OUT/'SpecialBatch2-SourceReview.png')
manifest=OUT/'protected-assets.json'
if not manifest.exists():
    files=[p for folder in ['CreatureInterpretations','ObjectInterpretations','EnvironmentInterpretations','TileFallback'] for p in (ROOT/'Art'/folder).glob('*.fbx') if p not in EXPORT_PATHS.values()]
    manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
print('SPECIAL_BATCH2_SOURCE_READY protected='+str(len(json.loads(manifest.read_text()))))
