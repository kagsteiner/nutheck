"""Assemble the three equines' actual front/profile eye review renders."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
board=Image.new('RGB',(1140,890),'#202a31');draw=ImageDraw.Draw(board)
font='C:/Windows/Fonts/segoeui.ttf'
heading=ImageFont.truetype(font,26);small=ImageFont.truetype(font,20)
draw.text((20,15),'Kobold states | Actual saved head views',font=heading,fill='#e9d9bd')
for col,key in enumerate(['kobold_shaman','kobold_mummy','kobold_zombie']):
    x=20+col*374
    draw.text((x,60),key.replace('_',' ').title(),font=heading,fill='#e9d9bd')
    for row,view in enumerate(['front','profile']):
        im=Image.open(out/(key+'-head-'+view+'.png')).convert('RGBA').resize((352,352),Image.Resampling.LANCZOS)
        board.paste(im,(x,98+row*375),im)
draw.text((20,855),'Actual saved meshes; yellow caster cloth, fitted linen wraps and blue/green undead skin.',font=small,fill='#b6c6ce')
board.save(out/'Batch14-EyeReview.png')
print('CREATURE_BATCH14_EYE_BOARD_READY')
