"""Source-only review board and immutable pre-batch export signatures."""
from pathlib import Path
import hashlib,json,re
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1];out=root/'Art/CreatureInterpretations'
text=(root/'upstream/NetHack/win/share/monsters.txt').read_text()
palette={m[0]:tuple(map(int,m[1:])) for m in re.findall(r'^(\S)\s*=\s*\(\s*(\d+),\s*(\d+),\s*(\d+)\s*\)',text,re.M)}
tiles={name:[r.strip() for r in rows.strip().splitlines()] for _,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',text,re.M)}
board=Image.new('RGB',(1300,810),'#27333b');d=ImageDraw.Draw(board);font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',23)
d.text((20,15),'Batch 25 | original official sex tiles, nearest-neighbour enlargement',font=font,fill='white')
for row,name in enumerate(['gecko','iguana','lizard']):
    d.text((20,90+row*235),name,font=font,fill='white')
    for col,sex in enumerate(['male','female']):
        im=Image.new('RGB',(16,16));im.putdata([palette[ch] for line in tiles[name+','+sex] for ch in line]);im.save(out/(name.replace(' ','_')+'-'+sex+'-official.png'))
        board.paste(im.resize((192,192),Image.Resampling.NEAREST),(260+col*250,80+row*235))
        d.text((260+col*250,52+row*235),sex,font=font,fill='white')
    same=tiles[name+',male']==tiles[name+',female'];d.text((790,110+row*235),'Identical sexes' if same else 'Distinct female silhouette',font=font,fill='#dbc197')
board.save(out/'Batch25-SourceReview.png')
manifest=out/'batch25-protected-assets.json'
if not manifest.exists():
    files=[p for folder in ['CreatureInterpretations','ObjectInterpretations','EnvironmentInterpretations','TileFallback'] for p in (root/'Art'/folder).glob('*.fbx')]
    manifest.write_text(json.dumps({p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
print('BATCH25_SOURCE_REVIEW_READY protected='+str(len(json.loads(manifest.read_text()))))



