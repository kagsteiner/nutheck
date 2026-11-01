"""Actual frontal, underside and face inspection renders, no concept artwork."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
board=Image.new('RGB',(1140,1320),'#202a31');draw=ImageDraw.Draw(board)
font='C:/Windows/Fonts/segoeui.ttf';heading=ImageFont.truetype(font,25);small=ImageFont.truetype(font,19)
draw.text((20,15),'Bat family | Wing construction and fitted eyes',font=heading,fill='#e9d9bd')
for col,key in enumerate(['bat','giant_bat','vampire_bat']):
    x=20+col*374;draw.text((x,60),key.replace('_',' ').title(),font=heading,fill='#e9d9bd')
    for row,label in enumerate(['front','underside','face']):
        y=102+row*390;draw.text((x,y),label.title(),font=small,fill='#b6c6ce')
        im=Image.open(out/(key+'-review-'+label+'.png')).convert('RGBA').resize((352,352),Image.Resampling.LANCZOS)
        board.paste(im,(x,y+25),im)
draw.text((20,1290),'Actual saved-mesh inspection renders with underside fill lighting; static spread-wing poses.',font=small,fill='#b6c6ce')
board.save(out/'Batch8-WingFaceReview.png');print('CREATURE_BATCH8_REVIEW_BOARD_READY')
