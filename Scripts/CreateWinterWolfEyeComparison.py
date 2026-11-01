"""Review board assembled exclusively from actual saved-mesh close renders."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
board=Image.new('RGB',(1280,1020),'#202a31');draw=ImageDraw.Draw(board)
font='C:/Windows/Fonts/segoeui.ttf'
title=ImageFont.truetype(font,28);small=ImageFont.truetype(font,20)
draw.text((24,18),'Winter wolves | Revised eye placement and pale coat',font=title,fill='#e9d9bd')
draw.text((24,58),'Actual Blender renders: frontal alignment, three-quarter placement and profile embedding.',font=small,fill='#b6c6ce')
for row,key in enumerate(['winter_wolf_cub','winter_wolf']):
    y=106+row*438
    draw.text((24,y),key.replace('_',' ').title(),font=title,fill='#e9d9bd')
    for col,label in enumerate(['front','quarter','profile']):
        x=24+col*416
        im=Image.open(out/(key+'-head-'+label+'.png')).convert('RGBA').resize((400,400),Image.Resampling.LANCZOS)
        board.paste(im,(x,y+35),im)
draw.text((24,995),'White coat; neutral ear lining; smaller skull-conforming red apertures, dark pupils and pale eyelids.',font=small,fill='#b6c6ce')
board.save(out/'WinterWolf-EyeReview.png')
print('WINTER_WOLF_EYE_BOARD_READY')
