"""Append reviewed kobold geometry; fit separate cloth/wrap state modules to it."""
import bpy,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import CreatureGeometry as g

def append_kobold(key,source):
    path=g.OUT/'CreatureBatch13.blend'
    with bpy.data.libraries.load(str(path),link=False) as (src,dst):dst.collections=[source]
    col=dst.collections[0];col.name=key;bpy.context.scene.collection.children.link(col)
    col.hide_viewport=False
    for obj in col.objects:
        obj.name=key+obj.name[len(source):];obj['creature']=key;obj.hide_render=False;obj.hide_viewport=False
        # Preserve shape but repaint the new derivative; never alter the source file.
        obj['source_family_object']=source+obj.name[len(key):]
        if 'preserve_paint' in obj:del obj['preserve_paint']
        for attr in list(obj.data.color_attributes):obj.data.color_attributes.remove(attr)
    bpy.context.view_layer.update()
    return col,bpy.data.objects[key+'_continuous_anatomy']

def wrap_ribbon(body,key,name,start,end,turns,width,pigment,lift=.003):
    """A solidified helical cloth strip follows first exits from the actual body."""
    g.GROUP=key;start=Vector(start);end=Vector(end);axis=(end-start).normalized()
    helper=Vector((1,0,0)) if abs(axis.x)<.9 else Vector((0,1,0))
    right=axis.cross(helper).normalized();up=axis.cross(right).normalized()
    tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());inv=body.matrix_world.inverted()
    steps=max(64,int(turns*64));verts=[];faces=[];max_gap=0
    for i in range(steps+1):
        t=i/steps;angle=t*math.tau*turns
        radial=right*math.cos(angle)+up*math.sin(angle)
        center=start.lerp(end,t)
        for side in [-1,1]:
            origin=center+axis*(side*width*.5)
            hit,normal,face,distance=tree.ray_cast(inv@origin,inv.to_3x3()@radial,.40)
            if hit is None:
                hit,normal,face,distance=tree.ray_cast(inv@(origin+radial*.16),inv.to_3x3()@(-radial),.32)
            assert hit is not None,(key,name,i,side)
            point=body.matrix_world@hit+normal*lift;point.z=max(.001,point.z)
            verts.append(point)
        if i<steps:
            a=i*2;faces.append((a,a+1,a+3,a+2))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(obj)
    g.finish(obj,name,pigment);obj['wrap_module']=True;obj['fitted_to_body']=True;obj['wrap_lift']=lift
    for p in mesh.polygons:p.use_smooth=True
    obj.modifiers.new('Linen thickness','SOLIDIFY').thickness=.0015
    return obj

def mummy_wraps(body,key):
    s=body['height_parameter']/.88
    def p(x,y,z):return (x*s,y*s,z*s)
    wrap_ribbon(body,key,'torso_linen',p(0,0,.315),p(0,0,.545),5,.043*s,'mummy_linen')
    wrap_ribbon(body,key,'forehead_linen',p(0,-.012,.755),p(0,-.012,.778),1.2,.028*s,'mummy_linen')
    wrap_ribbon(body,key,'jaw_linen',p(0,-.035,.654),p(0,-.035,.679),1.5,.026*s,'mummy_linen')
    wrap_ribbon(body,key,'crown_linen',p(0,-.020,.720),p(0,.015,.720),1.3,.027*s,'mummy_linen')
    for side in [-1,1]:
        wrap_ribbon(body,key,'upper_leg_linen',p(side*.069,-.003,.305),p(side*.082,-.015,.220),2.5,.026*s,'mummy_linen')
        wrap_ribbon(body,key,'lower_leg_linen',p(side*.085,-.013,.174),p(side*.083,.003,.075),3,.028*s,'mummy_linen')
        wrap_ribbon(body,key,'upper_arm_linen',p(side*.122,-.002,.512),p(side*.176,-.013,.434),2.5,.026*s,'mummy_linen')
        wrap_ribbon(body,key,'forearm_linen',p(side*.182,-.023,.405),p(side*.174,-.059,.337),2,.025*s,'mummy_linen')
        wrap_ribbon(body,key,'foot_linen',p(side*.085,-.100,.030),p(side*.085,-.065,.030),1.5,.018*s,'mummy_linen',.002)

def state_pigment(obj,p,color,colors):
    key=obj.get('creature');pigment=obj['pigment']
    if obj.get('ear_tip_height') and p.z>obj['ear_tip_height']:return colors['kobold_pale']
    if key=='kobold_shaman':
        if pigment=='kobold_orange':return colors['shaman_yellow']
        return color
    if key=='kobold_mummy':
        if pigment in ['kobold_blue','kobold_cool']:return colors['mummy_skin']
        if pigment=='mummy_linen':
            shade=.93+.035*math.sin(p.z*115+p.x*22)+.025*math.sin(p.y*83)
            return tuple(c*shade for c in colors['mummy_linen'])
        return color
    if key=='kobold_zombie' and pigment in ['kobold_blue','kobold_cool']:
        # Broad pigmentation on continuous skin; no raised wound/coat blobs.
        s=1.125;x=p.x/s;y=p.y/s;z=p.z/s
        weight=max(math.exp(-((x+.045)/.085)**2-((z-.72)/.10)**2),
                   .85*math.exp(-((x-.055)/.10)**2-((z-.47)/.14)**2),
                   .75*math.exp(-((x+.18)/.055)**2-((z-.37)/.11)**2))
        base=colors['zombie_blue'];green=colors['zombie_green']
        return tuple(a*(1-weight)+b*weight for a,b in zip(base,green))
    return color
