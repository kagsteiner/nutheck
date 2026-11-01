"""Assemble the three canids' actual front/profile eye review renders."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
board=Image.new('RGB',(1140,890),'#202a31');draw=ImageDraw.Draw(board)
font='C:/Windows/Fonts/segoeui.ttf'
heading=ImageFont.truetype(font,26);small=ImageFont.truetype(font,20)
draw.text((20,15),'Dog family | Fitted eyes, front and profile',font=heading,fill='#e9d9bd')
for col,key in enumerate(['dog','large_dog','dingo']):
    x=20+col*374
    draw.text((x,60),key.replace('_',' ').title(),font=heading,fill='#e9d9bd')
    for row,view in enumerate(['front','profile']):
        im=Image.open(out/(key+'-head-'+view+'.png')).convert('RGBA').resize((352,352),Image.Resampling.LANCZOS)
        board.paste(im,(x,98+row*375),im)
draw.text((20,855),'Actual saved-mesh renders; isolated head views hide the tails. Amber eyes, dark pupils and coat-coloured lids.',font=small,fill='#b6c6ce')
board.save(out/'Batch6-EyeReview.png')
print('CREATURE_BATCH6_EYE_BOARD_READY')
