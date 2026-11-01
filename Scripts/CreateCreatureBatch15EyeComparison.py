"""Assemble the three equines' actual front/profile eye review renders."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
board=Image.new('RGB',(1900,890),'#202a31');draw=ImageDraw.Draw(board)
font='C:/Windows/Fonts/segoeui.ttf'
heading=ImageFont.truetype(font,26);small=ImageFont.truetype(font,20)
draw.text((20,15),'Gnome states | Actual saved head views',font=heading,fill='#e9d9bd')
for col,key in enumerate(['gnomish_wizard','gnome_mummy','gnome_zombie','gnomish_wizard_female','gnome_zombie_female']):
    x=20+col*374
    draw.text((x,60),key.replace('_',' ').title(),font=heading,fill='#e9d9bd')
    for row,view in enumerate(['front','profile']):
        im=Image.open(out/(key+'-head-'+view+'.png')).convert('RGBA').resize((352,352),Image.Resampling.LANCZOS)
        board.paste(im,(x,98+row*375),im)
draw.text((20,855),'Actual saved meshes; green caster clothing, fitted linen wraps, retained pointed caps and red undead eyes.',font=small,fill='#b6c6ce')
board.save(out/'Batch15-EyeReview.png')
print('CREATURE_BATCH15_EYE_BOARD_READY')
