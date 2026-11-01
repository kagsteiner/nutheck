"""Detachable static mouth-froth cue; not disease animation or ground geometry."""
import CreatureGeometry as geo

def rat_saliva():
    for x,y,z,r in [(-.281,-.031,.057,.013),(-.281,.031,.057,.013),
        (-.266,-.039,.051,.011),(-.266,.039,.051,.011),(-.279,0,.040,.012)]:
        obj=geo.orb('saliva_foam',(x,y,z),(r,r*.78,r*.70),'saliva');obj['state_module']='saliva'
    for y in [-.032,.032]:
        obj=geo.limb('saliva_drip',[(-.274,y,.047),(-.277,y,.030),(-.277,y,.014)],
            [.0025,.002,.001],'saliva');obj['state_module']='saliva'
