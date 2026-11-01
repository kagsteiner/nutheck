"""Small, skull-conforming almond eyes, mirrored about the muzzle centreline."""
import math
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import CreatureGeometry as geo

def winter_wolf_eyes(key,hx,hz,head,body,iris='wolf_red',lid_pigment='winter_white',
                    seed_offset=(-.78,.46,.20),normal_hint=(-.78,.776,.247),horizontal_hint=(.705,.709,0)):
    geo.GROUP=key
    tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get())
    inverse=body.matrix_world.inverted()
    skull=Vector((hx,0,hz))
    # Anterior side of the skull, behind the muzzle root; paired forward gaze.
    # The aperture follows the actual sculpt surface instead of floating globes.
    for side in [-1,1]:
        seed=skull+Vector((seed_offset[0]*head,side*seed_offset[1]*head,seed_offset[2]*head))
        outward=Vector((normal_hint[0],side*normal_hint[1],normal_hint[2])).normalized()
        across=Vector((side*horizontal_hint[0],horizontal_hint[1],horizontal_hint[2])).normalized()
        up=outward.cross(across).normalized()
        if up.z<0:up=-up
        def surface(u,v,offset):
            target=seed+across*u+up*(v+side*u*.10)
            start=target+outward*.12
            hit,normal,face,distance=tree.ray_cast(inverse@start,(inverse.to_3x3()@(-outward)).normalized(),.30)
            assert hit is not None,(key,side,u,v)
            return body.matrix_world@hit+outward*offset
        width=head*.145;height=head*.069
        def patch(name,w,h,pigment,lift):
            verts=[surface(0,0,lift+.0007)]
            for i in range(48):
                a=math.tau*i/48
                # Pointed canthi and restrained vertical opening.
                u=w*math.cos(a);v=h*math.sin(a)*abs(math.sin(a))**.30
                verts.append(surface(u,v,lift))
            faces=[(0,i+1,(i+1)%48+1) for i in range(48)]
            mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
            obj=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(obj)
            geo.finish(obj,name,pigment)
            for polygon in mesh.polygons:polygon.use_smooth=True
            obj['eye_side']=side;obj['eye_surface_conforming']=True
            return obj
        patch('orbital_rim',width*1.10,height*1.20,'black',.0010)
        eye=patch('eye',width,height,iris,.0018)
        eye['eye_center']=list(surface(0,0,.0018));eye['gaze_normal']=list(outward)
        # Dark round pupil remains within the red aperture, looking forward.
        patch('round_pupil',head*.028,head*.028,'black',.0027)
        for upper in [True,False]:
            points=[]
            for i in range(13):
                a=(0 if upper else math.pi)+math.pi*i/12
                u=width*1.07*math.cos(a);v=height*1.17*math.sin(a)*abs(math.sin(a))**.30
                points.append(surface(u,v,.0021))
            lid=geo.limb('upper_eyelid' if upper else 'lower_eyelid',points,
                [head*(.018 if upper else .012)]*len(points),lid_pigment)
            lid['eye_side']=side
        glint=geo.orb('eye_glint',surface(-head*.033,head*.018,.0034),
            (head*.010,head*.010,head*.010),'glint')
        glint['eye_side']=side
