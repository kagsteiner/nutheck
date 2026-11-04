"""Saved-model studio review with a broad reflection card for worked metals."""
import bpy,math,json
from mathutils import Vector
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'Art/ObjectInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'Snickersnee.blend'))
for c in bpy.data.collections:c.hide_viewport=False
# A vertical softbox lets silver reflect light along the shaft rather than only
# at its end caps. This is review lighting, never an exported part or game glow.
light=bpy.data.objects.get('Metal reflection card')
if not light:
    data=bpy.data.lights.new('Metal reflection card','AREA');data.shape='RECTANGLE';data.energy=110;data.size=2.5;data.size_y=3
    light=bpy.data.objects.new('Metal reflection card',data);bpy.context.collection.objects.link(light)
light.location=(0,-3,.70);light.rotation_euler=(Vector((0,0,.65))-light.location).to_track_quat('-Z','Y').to_euler()
scene=bpy.context.scene;camera=scene.camera;scene.render.film_transparent=True
bpy.ops.wm.save_as_mainfile(filepath=str(out/'Snickersnee.blend'))
report=[]
for key in ['snickersnee']:
    parts=[]
    for o in scene.objects:
        if o.type=='MESH':
            o.hide_render=o.get('creature')!=key
            if not o.hide_render:parts.append(o)
    bpy.context.view_layer.update();pts=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=Vector(tuple(min(p[i] for p in pts) for i in range(3)));high=Vector(tuple(max(p[i] for p in pts) for i in range(3)));center=(low+high)*.5
    def aim(yaw,elev,scale):
        a=math.radians(yaw);e=math.radians(elev);camera.location=center+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*5
        camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.ortho_scale=scale;camera.data.shift_x=camera.data.shift_y=0
    scene.cycles.samples=16;scene.render.resolution_x=scene.render.resolution_y=800
    for view,yaw,elev in [('three-quarter',-125,30),('rear',55,25)]:
        aim(yaw,elev,max((high-low).length*1.1,.025));scene.render.filepath=str(out/(key+'-'+view+'.png'));bpy.ops.render.render(write_still=True)
    candidates=[];scene.cycles.samples=8;scene.render.resolution_x=scene.render.resolution_y=16
    for yaw in [-115,-90,-65]:
        for elev in [25,45]:
            aim(yaw,elev,1);inverse=camera.rotation_euler.to_matrix().transposed();projected=[inverse@(p-center) for p in pts]
            width=max(p.x for p in projected)-min(p.x for p in projected);height=max(p.y for p in projected)-min(p.y for p in projected)
            camera.data.ortho_scale=max(width,height)*16/13
            name=key+f'-pixel-{yaw}-{elev}.png';scene.render.filepath=str(out/name);bpy.ops.render.render(write_still=True)
            candidates.append(dict(yaw=yaw,elevation=elev,file=name))
    report.append(dict(key=key,comparison='Actual 16x16 physical-appearance readability; no official-tile fidelity score',bounds_m=[list(low),list(high)],candidates=candidates))
(out/'projection-report-snickersnee.json').write_text(json.dumps(report,indent=2))
print('SNICKERSNEE_STUDIO_READY',flush=True)
