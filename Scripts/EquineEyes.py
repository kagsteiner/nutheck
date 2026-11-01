"""Small lateral equine eyes fitted to the actual skull, with horizontal pupils."""
import math,bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import CreatureGeometry as geo

def equine_eyes(key,hx,hz,head,body,coat,iris='equine_blue'):
    geo.GROUP=key
    tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());inverse=body.matrix_world.inverted()
    for side in [-1,1]:
        seed=Vector((hx-head*.23,side*head*.47,hz+head*.09))
        outward=Vector((-.28,side*.955,.10)).normalized()
        across=Vector((side*.96,.28,0)).normalized();up=outward.cross(across).normalized()
        if up.z<0:up=-up
        def surface(u,v,lift):
            start=seed+across*u+up*v+outward*.14
            hit,normal,face,distance=tree.ray_cast(inverse@start,(inverse.to_3x3()@(-outward)).normalized(),.35)
            assert hit is not None,(key,side,u,v)
            return body.matrix_world@hit+outward*lift
        width=head*.137;height=head*.079
        def patch(name,w,h,color,lift):
            vertices=[surface(0,0,lift+.0006)]
            for i in range(48):
                a=math.tau*i/48;vertices.append(surface(w*math.cos(a),h*math.sin(a)*abs(math.sin(a))**.20,lift))
            mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],[(0,i+1,(i+1)%48+1) for i in range(48)]);mesh.update()
            obj=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(obj);geo.finish(obj,name,color)
            for p in mesh.polygons:p.use_smooth=True
            obj['eye_side']=side;obj['eye_surface_conforming']=True
            return obj
        patch('orbital_rim',width*1.12,height*1.17,'equine_dark',.0009)
        eye=patch('eye',width,height,iris,.0016)
        eye['eye_center']=list(surface(0,0,.0016));eye['gaze_normal']=list(outward)
        patch('horizontal_pupil',width*.61,height*.30,'black',.0024)
        for upper in [True,False]:
            points=[]
            for i in range(17):
                a=(0 if upper else math.pi)+math.pi*i/16
                points.append(surface(width*1.07*math.cos(a),height*1.11*math.sin(a),.002))
            lid=geo.limb('upper_eyelid' if upper else 'lower_eyelid',points,[head*(.019 if upper else .013)]*len(points),coat)
            lid['eye_side']=side
        glint=geo.orb('eye_glint',surface(-width*.30,height*.27,.003),(.0013,.0013,.0013),'glint');glint['eye_side']=side
