"""User reference beside actual saved-model side/back/head views."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
board=Image.new('RGB',(1560,1230),'#202a31');draw=ImageDraw.Draw(board)
font='C:/Windows/Fonts/segoeui.ttf';title=ImageFont.truetype(font,30);small=ImageFont.truetype(font,21)
draw.text((24,18),'Jaguar | Reference-led coat revision',font=title,fill='#e9d9bd')
draw.text((24,62),'User photograph',font=small,fill='#b6c6ce')
ref=Image.open(out/'References/Jaguar-user-reference.jpg').convert('RGB');ref.thumbnail((700,485),Image.Resampling.LANCZOS)
board.paste(ref,(24,102))
draw.text((800,62),'Actual Blender mesh: flank',font=small,fill='#b6c6ce')
for filename,box in [('jaguar-reference-side.png',(780,95,750,500)),('jaguar-reference-back.png',(15,655,760,510)),('jaguar-head-front.png',(950,645,460,510))]:
    im=Image.open(out/filename).convert('RGBA');im.thumbnail((box[2],box[3]),Image.Resampling.LANCZOS)
    board.paste(im,(box[0]+(box[2]-im.width)//2,box[1]),im)
draw.text((24,610),'Actual Blender mesh: pattern wraps over the back',font=small,fill='#b6c6ce')
draw.text((950,610),'Head and leg spots',font=small,fill='#b6c6ce')
draw.text((24,1185),'Dense irregular rosettes, smaller head/leg spots, pale underside and banded tail. Geometry and other cats retained.',font=small,fill='#b6c6ce')
board.save(out/'Jaguar-ReferenceRevision.png');print('JAGUAR_REFERENCE_COMPARISON_READY')
