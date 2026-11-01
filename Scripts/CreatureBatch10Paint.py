"""Continuous tiger stripes and restrained hell-hound coat shading, vertex paint only."""
import math

def blend(a,b,t):return tuple(x*(1-t)+y*t for x,y in zip(a,b))
def smooth(a,b,x):
    t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)

def batch10_pigment(obj,p,pigment,colors):
    key=obj.get('creature');tag=obj.get('pigment','')
    if key=='tiger' and tag in {'tiger_coat','tiger_pale'}:
        dark=colors['tiger_stripe'];cream=colors['tiger_pale'];gold=colors['tiger_coat']
        x,y,z=p;side=1 if y>=0 else -1
        if obj.get('coat_marking')=='tiger_stripes':
            hx=obj['head_x'];hz=obj['head_z'];head=obj['head_length']
            center=obj['body_center_z'];depth=obj['body_depth'];width=obj['body_width']
            if x<hx+head*.52 and z>hz-head*.80:
                # White lower cheeks/chin; black tear tracks and cheek bars.
                pale=1-smooth(hz-head*.23,hz+head*.03,z)
                base=blend(gold,cream,pale*.95)
                q=(z-hz)/head
                cheek=abs(math.sin(q*12.5+(x-hx)*19+side*.30))
                brow=abs(math.sin((x-hx)*72+y*8))
                marked=(abs(y)>head*.57 and -.55<q<.42 and cheek>.90)
                marked|=(q>.32 and brow>.91)
                # Fine dark lines beside the inner eye corners, never extra eyes.
                marked|=(-.22<q<.12 and abs(abs(y)-head*.35)<head*.042 and x<hx-head*.60)
                return dark if marked else base
            if z<center-depth*.58:
                # Upper legs carry staggered horizontal stripes; toes stay pale.
                pale=1-smooth(.055,.20,z)
                base=blend(gold,cream,pale*.93)
                band=abs(math.sin(z*48+x*8+side*.51))
                return dark if band>.935 and z>.060 else base
            angle=math.atan2(y/width,(z-center)/depth)
            pale=smooth(1.55,2.28,abs(angle))
            base=blend(gold,cream,pale*.98)
            mark=False
            for i in range(11):
                root=-.315+i*.060+ .007*math.sin(i*2.7+side)
                a=abs(angle)
                curve=root+.022*math.sin(a*2.3+i*1.7+side*.3)+.012*a*math.cos(i*2.0)
                taper=.010+.008*(.5+.5*math.sin(i*1.9+a*1.2))
                taper*=1-.48*smooth(1.9,2.8,a)
                if abs(x-curve)<taper and a<2.70:mark=True
                # Short fork on selected shoulder/flank bands.
                if i%3==1 and .6<a<1.9 and abs(x-(curve+.035*(a-.6)))<taper*.52:mark=True
            return dark if mark else base
        if obj.get('tail_form'):
            band=abs(math.sin((z-obj['tail_root_z'])*41+x*5))
            return dark if band>.77 or z>obj['tail_root_z']+.46 else gold
        if 'rounded_ear' in obj.name:
            if x>obj.location.x:return cream if (y-obj.location.y)**2+(z-obj.location.z)**2<.00020 else dark
        if 'muzzle_pad' in obj.name:
            freckle=abs(math.sin(y*225+z*170)*math.sin(x*200-z*67))>.94
            return dark if freckle else cream
    if key in {'hell_hound_pup','hell_hound'} and tag=='hell_coat':
        body_z=obj.get('body_center_z',.42)
        # Orange-red continuous coat, darker spine; no black shadow feet.
        weight=.21+.20*smooth(body_z-.03,body_z+.12,p.z)
        return blend(colors['hell_coat'],colors['hell_rust'],weight)
    return pigment
