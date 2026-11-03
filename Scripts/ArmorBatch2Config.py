from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Art/ObjectInterpretations'
DRAGON_COLORS=['gray','gold','silver','red','white','orange','black','blue','green','yellow']
GROUPS=['plate_mail','crystal_plate_mail','bronze_plate_mail']+[c+'_dragon_scale_mail' for c in DRAGON_COLORS]
