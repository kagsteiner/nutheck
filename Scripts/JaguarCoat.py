"""Reference-led jaguar paint: wrapping rosettes, spotted head/legs and banded tail."""
import math
from functools import lru_cache

def blend(a,b,t):return tuple(x*(1-t)+y*t for x,y in zip(a,b))
def smooth(a,b,x):
    t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def noise(i,j,s=0):
    q=math.sin(i*127.1+j*311.7+s*74.7)*43758.5453
    return q-math.floor(q)

def markings(u,v,spacing,rosettes):
    """Jittered surface cells, thick irregular rings and independent inner spots."""
    ci=math.floor(u/spacing);cj=math.floor(v/spacing);ink=0;warm=0
    for i in range(ci-1,ci+2):
        for j in range(cj-1,cj+2):
            # Offset successive rows and jitter both axes to avoid printed grids.
            cx=(i+.5+(j%2)*.33+(noise(i,j,1)-.5)*.40)*spacing
            cy=(j+.5+(noise(i,j,2)-.5)*.42)*spacing
            dx=u-cx;dy=v-cy
            angle=noise(i,j,3)*math.tau
            a=(dx*math.cos(angle)+dy*math.sin(angle))/(spacing*(.30+.09*noise(i,j,4)))
            b=(-dx*math.sin(angle)+dy*math.cos(angle))/(spacing*(.31+.10*noise(i,j,5)))
            r=math.hypot(a,b)
            if r>1.5:continue
            t=math.atan2(b,a);phase=noise(i,j,6)*math.tau
            edge=1+.13*math.sin(t*3+phase)+.075*math.sin(t*5-phase)+.045*math.cos(t*7+phase)
            if rosettes:
                thickness=.20+.09*noise(i,j,7)
                ring=1-smooth(thickness,thickness+.14,abs(r-edge))
                # Mostly complete rosettes, with a few short natural interruptions.
                if noise(i,j,8)>.57:
                    ring*=.25+.75*smooth(-.94,-.67,math.cos(t-phase))
                ink=max(ink,ring)
                warm=max(warm,(1-smooth(.65,.90,r))*.42)
                count=1+int(noise(i,j,9)*3)
                for dot in range(count):
                    px=(noise(i,j,10+dot*2)-.5)*.70;py=(noise(i,j,11+dot*2)-.5)*.65
                    d=math.hypot(a-px,b-py)
                    ink=max(ink,1-smooth(.13,.24,d))
            else:
                ink=max(ink,1-smooth(.66,.98,r))
    return ink,warm

GOLD=(.68,.36,.085);CREAM=(.84,.77,.59);INK=(.010,.006,.003);CENTER=(.45,.205,.045)

def jaguar_shade(obj,height_fraction,original):
    if obj.get('creature')=='jaguar' and (obj.get('coat_marking') in {'jaguar_rosettes','jaguar_tail'} or obj.get('pigment') in {'jaguar_gold','jaguar_muzzle'}):
        return .88+.10*height_fraction
    return original

@lru_cache(maxsize=160000)
def _sample(part,x,y,z):
    # Fixed art dimensions from the saved jaguar, not real-world measurements.
    centre=.425;depth=.170;width=.148;hx=-.2702;hz=.530;head=.143
    if part=='tail':
        q=(z-.450)*115+(x-.23)*16
        ring=smooth(.05,.42,math.sin(q+.24*math.sin(y*95)))
        tip=smooth(.716,.744,z)
        return blend(GOLD,INK,max(ring*.98,tip))
    if part=='muzzle':
        dark,_=markings(x*.72+z*.40,y,.026,False)
        return blend(CREAM,INK,dark*.90)
    if part=='ear':
        back=smooth(-.240,-.225,x)
        spot=((abs(y)-.0896)/.023)**2+((z-.638)/.022)**2
        ocellus=(1-smooth(.45,.85,spot))*back
        return blend(blend(GOLD,INK,back),CREAM,ocellus*.85)
    if part=='plain':return GOLD
    belly=1-smooth(centre-depth*.43,centre-depth*.04,z)
    lower_legs=1-smooth(.22,.34,z)
    base=blend(GOLD,CREAM,max(belly*.86,lower_legs*.88))
    if x<-.212 and z>.36:
        theta=math.atan2(y/.128,(z-hz)/(head*.9))
        ink,_=markings(x,theta*.105,.028,False)
        # Small dense face/neck spots, as in the supplied reference.
        return blend(GOLD,INK,ink*.96)
    if z<.315:
        # Wrap spots around each leg rather than projecting stripes through it.
        candidates=[(a,b) for a in [-.203,.212] for b in [-.113,.113]]
        ax,ay=min(candidates,key=lambda q:(x-q[0])**2+(y-q[1])**2)
        theta=math.atan2(y-ay,x-ax)
        ink,_=markings(z,theta*.034,.027,False)
        return blend(base,INK,ink*.98)
    # Cylindrical surface coordinates carry rosettes over both flanks and spine.
    theta=math.atan2(y/width,(z-centre)/depth)
    ink,warm=markings(x,theta*.140,.063,True)
    base=blend(base,CENTER,warm)
    return blend(base,INK,ink*.99)

def jaguar_pigment(obj,p):
    name=obj.name
    if 'whisker' in name:return CREAM
    part='tail' if 'raised_tail' in name else 'muzzle' if 'muzzle_pad' in name else 'ear' if 'rounded_ear' in name else 'body' if 'continuous_anatomy' in name else 'plain'
    return _sample(part,float(p.x),float(p.y),float(p.z))
