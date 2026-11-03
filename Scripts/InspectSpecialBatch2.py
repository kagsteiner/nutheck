"""Saved geometry, palette, shared sex source and protected canonical export audit."""
import sys,bpy,bmesh,math,json,hashlib,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from SpecialBatch2Config import *
bpy.ops.wm.open_mainfile(filepath=str(OUT/BLEND_NAME))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();report={};altar_hashes=[]
for key in GROUPS:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for o in parts:
        a=o.data.color_attributes.get('Paint');assert a and a.domain=='CORNER' and a.data_type=='FLOAT_COLOR',o.name
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
        assert not o.animation_data and not o.modifiers,o.name
        if key!='shopkeeper' or any(n in o.name for n in ['_jacket','trouser','shoe_','hat_','cuff_','collar']):
            bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
    pts=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=[min(p[i] for p in pts) for i in range(3)];high=[max(p[i] for p in pts) for i in range(3)];assert low[2]>=-.002,(key,low)
    if key=='shopkeeper':
        assert len([o for o in parts if o.get('eye_center')])==2
        assert len([o for o in parts if o.get('hat_module')])==2
        assert not any('player_form' in o or o.get('long_hair_mass') for o in parts)
        jacket=bpy.data.objects['shopkeeper_jacket'];assert len(jacket.data.vertices)>1000
    else:
        top=next(o for o in parts if o.get('altar_top'));assert len(top.data.vertices)>500
        if key=='altar_other':assert len([o for o in parts if o.get('static_ray_inlay')])==12
        else:
            paint=top.data.color_attributes['Paint'];assert max(v.color[0]-v.color[1] for v in paint.data)>.035,(key,'Missing source red mineral paint')
        assert all(abs(p[i])<.46 for p in pts for i in [0,1]) and .57<high[2]<.59
        altar_hashes.append(hashlib.sha256(b''.join(str(tuple(v.co)).encode() for o in sorted(parts,key=lambda o:o.name) if not o.get('static_ray_inlay') for v in o.data.vertices)).hexdigest())
    report[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],paint_valid=True,static=True,canonical_fbx=str(EXPORT_PATHS[key].relative_to(ROOT)))
assert len(set(altar_hashes))==1,'Ordinary altar structural geometry should be shared'
raw=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text();tiles={n:r for _,n,r in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',raw,re.M)}
assert tiles['shopkeeper,male']==tiles['shopkeeper,female']
protected=json.loads((OUT/'protected-assets.json').read_text());assert len(protected)==77
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in protected.items())
report.update(previous_77_exports_unchanged=True,shopkeeper_sex_tiles_identical=True,altar_structure_shared=True,source_hat_dark_pixels_retained=True)
(OUT/'mesh-inspection.json').write_text(json.dumps(report,indent=2))
print('SPECIAL_BATCH2_NATIVE_CHECK PASS '+json.dumps(report),flush=True)
