"""Texture-only coat treatment shared by new anatomical drafts."""
import bpy
from pathlib import Path

def apply_fur(objects):
    texture_dir=Path(__file__).resolve().parents[1]/'Art/FurStudy/Textures'
    brush=bpy.data.images.load(str(texture_dir/'FurBrush.png'),check_existing=True)
    normal=bpy.data.images.load(str(texture_dir/'FurBrushNormal.png'),check_existing=True)
    for image in [brush,normal]:image.colorspace_settings.name='Non-Color'
    materials={}
    for obj in objects:
        if not obj.get('fur_surface'):continue
        mesh=obj.data
        for layer in list(mesh.uv_layers):mesh.uv_layers.remove(layer)
        uv=mesh.uv_layers.new(name='FurFlow')
        for face in mesh.polygons:
            n=(obj.matrix_world.to_3x3()@face.normal).normalized()
            for index in face.loop_indices:
                p=obj.matrix_world@mesh.vertices[mesh.loops[index].vertex_index].co
                if 'tail' in obj.name or p.z<obj.get('fur_leg_height',.22):a,b=p.z,(p.x if abs(n.y)>.5 else p.y)
                elif abs(n.z)>.5:a,b=p.x,p.y
                elif abs(n.y)>.5:a,b=p.x,p.z
                else:a,b=p.z,p.y
                uv.data[index].uv=(a*4,b*4)
        for i,source in enumerate(list(mesh.materials)):
            if source.name not in materials:
                mat=source.copy();mat.name='Fur_'+source.name
                nodes=mat.node_tree.nodes;links=mat.node_tree.links
                shader=nodes.get('Principled BSDF');pigment=nodes.get('Pigment')
                tex=nodes.new('ShaderNodeTexImage');tex.image=brush;tex.extension='REPEAT'
                amount=nodes.new('ShaderNodeMath');amount.operation='MULTIPLY';amount.inputs[1].default_value=2
                links.new(tex.outputs['Color'],amount.inputs[0])
                mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
                links.new(pigment.outputs['Color'],mix.inputs[1]);links.new(amount.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],shader.inputs['Base Color'])
                norm=nodes.new('ShaderNodeTexImage');norm.image=normal
                bump=nodes.new('ShaderNodeNormalMap');links.new(norm.outputs['Color'],bump.inputs['Color']);links.new(bump.outputs['Normal'],shader.inputs['Normal'])
                materials[source.name]=mat
            mesh.materials[i]=materials[source.name]
    # Pack maps so rendering also works before this new blend has a save path.
    for image in [brush,normal]:image.pack()
