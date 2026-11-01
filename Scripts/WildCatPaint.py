"""Continuous vertex-painted coats: broad jaguar rosettes, lynx flank and dark panther."""
import math
from JaguarCoat import jaguar_pigment

def blend(a,b,t):return tuple(x*(1-t)+y*t for x,y in zip(a,b))
def band(lo,hi,value):
    t=max(0,min(1,(value-lo)/(hi-lo)));return t*t*(3-2*t)

def wild_cat_pigment(obj,p,base,colors):
    mark=obj.get('coat_marking')
    if obj.get('creature')=='jaguar' and (mark in {'jaguar_rosettes','jaguar_tail'} or obj.get('pigment') in {'jaguar_gold','jaguar_muzzle'}):
        return jaguar_pigment(obj,p)
    if mark=='lynx_flank':
        z=obj['body_center_z'];width=obj['body_width'];length=obj['body_length']
        weight=.65*band(width*.28,width*.80,abs(p.y))*(1-band(z+.015,z+.075,p.z))
        weight*=band(-length*.8,-length*.4,p.x)*(1-band(length*.55,length*.95,p.x))
        weight*=band(obj['leg_height']*.86,obj['leg_height']*1.22,p.z)
        hx=obj['head_x'];hz=obj['head_z'];head=obj['head_length']
        cheek=.88*(1-band(.45,1,abs(p.x-hx)/(head*.85)))
        cheek*=1-band(.45,1,abs(p.z-(hz-head*.20))/(head*.50))
        cheek*=band(width*.50,width*.84,abs(p.y))
        weight=max(weight,cheek)
        return blend(base,colors['lynx_pale'],weight)
    if mark=='lynx_tail_tip':
        return blend(base,colors['wild_cat_dark'],band(obj['tail_tip_x']-.043,obj['tail_tip_x']-.010,p.x))
    return base
