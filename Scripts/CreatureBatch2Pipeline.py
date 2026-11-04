# Coat markings blend pigments on existing anatomy, never add raised geometry.
def smooth_band(low,high,value):
    t=max(0,min(1,(value-low)/(high-low)))
    return t*t*(3-2*t)

# Apply sculpt modifiers and encode the palette/soft painted shading per corner.
bpy.context.view_layer.update()
for obj in list(bpy.context.scene.objects):
    if obj.type!='MESH': continue
    if obj.get('preserve_paint'): continue  # Reused, already-painted family parts.
    bpy.context.view_layer.objects.active=obj
    for modifier in list(obj.modifiers): bpy.ops.object.modifier_apply(modifier=modifier.name)
    mesh=obj.data; pigment=COLORS[obj['pigment']]
    topology=bmesh.new(); topology.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(topology,faces=list(topology.faces))
    topology.to_mesh(mesh); topology.free()
    paint=mesh.color_attributes.new(name='Paint',type='FLOAT_COLOR',domain='CORNER'); mesh.color_attributes.active_color=paint
    zmin=min(v.co.z for v in mesh.vertices); zmax=max(v.co.z for v in mesh.vertices)
    for loop in mesh.loops:
        v=mesh.vertices[loop.vertex_index]; p=obj.matrix_world@v.co
        surface_pigment=pigment
        if obj.get('coat_marking')=='saddle':
            weight=.85*smooth_band(.42,.525,p.z)*smooth_band(-.26,-.13,p.x)*(1-smooth_band(.16,.29,p.x))
            surface_pigment=tuple(a*(1-weight)+b*weight for a,b in zip(pigment,COLORS['saddle']))
        elif obj.get('coat_marking')=='cat_flank':
            length=obj['body_length']; width=obj['body_width']; center_z=obj['body_center_z']
            weight=.9*smooth_band(width*.28,width*.85,abs(p.y))
            weight*=smooth_band(-length*.65,-length*.25,p.x)*(1-smooth_band(length*.50,length*.90,p.x))
            weight*=smooth_band(center_z-.045,center_z+.045,p.z)
            surface_pigment=tuple(a*(1-weight)+b*weight for a,b in zip(pigment,COLORS['cat_peach']))
        elif obj.get('coat_marking')=='cat_tail':
            weight=.70*smooth_band(.35,.75,.5+.5*math.sin((p.z-obj['tail_root_z'])*48))
            surface_pigment=tuple(a*(1-weight)+b*weight for a,b in zip(pigment,COLORS['cat_peach']))
        elif obj.get('coat_marking')=='wolf_back':
            weight=.38*(1-smooth_band(obj['body_center_z']-.03,obj['body_center_z']+.09,p.z))
            surface_pigment=tuple(a*(1-weight)+b*weight for a,b in zip(pigment,COLORS['wolf_light']))
        elif obj.get('coat_marking') in {'canid_bib','dingo_underside'}:
            z=obj['body_center_z'];shoulder=obj['shoulder_x'];depth=obj['body_depth']
            if obj['coat_marking']=='canid_bib':
                weight=.86*(1-smooth_band(shoulder-.025,shoulder+.065,p.x))
                weight*=1-smooth_band(z+depth*.05,z+depth*.72,p.z)
                weight*=smooth_band(z-depth*1.10,z-depth*.50,p.z)
                pale=COLORS['dog_cream']
            else:
                weight=.83*(1-smooth_band(z-depth*.15,z+depth*.35,p.z))
                pale=COLORS['dingo_pale']
            surface_pigment=tuple(a*(1-weight)+b*weight for a,b in zip(pigment,pale))
        elif obj.get('coat_marking')=='coyote_shading':
            weight=.50*(1-smooth_band(obj['body_center_z']-.04,obj['body_center_z']+.06,p.z))
            surface_pigment=tuple(a*(1-weight)+b*weight for a,b in zip(pigment,COLORS['coyote_light']))
        elif obj.get('coat_marking')=='warg_mottle':
            weight=.32+.17*math.sin(p.x*27+p.y*33)*math.sin(p.z*31)
            surface_pigment=tuple(a*(1-weight)+b*weight for a,b in zip(pigment,COLORS['warg_cool']))
        if globals().get('PIGMENT_FUNCTION'):
            surface_pigment=PIGMENT_FUNCTION(obj,p,surface_pigment,COLORS)
        shade=.79+.19*(v.co.z-zmin)/max(.01,zmax-zmin)+.018*math.sin(p.x*28+p.y*21+p.z*13)
        if globals().get('SHADE_FUNCTION'):
            shade=SHADE_FUNCTION(obj,(v.co.z-zmin)/max(.01,zmax-zmin),shade)
        paint.data[loop.index].color=(*(max(0,min(1,c*shade)) for c in surface_pigment),1)
    # Blender and UE both use the painted vertex colour as the actual surface.
    for material in mesh.materials:
        shader=material.node_tree.nodes.get('Principled BSDF')
        attr=material.node_tree.nodes.get('Pigment')
        if not attr: attr=material.node_tree.nodes.new('ShaderNodeVertexColor'); attr.name='Pigment'; attr.layer_name='Paint'
        material.node_tree.links.new(attr.outputs['Color'],shader.inputs['Base Color'])

if globals().get('POST_PAINT'):
    POST_PAINT()

GROUPS=globals().get('GROUPS',['jackal','fox','gnome'])
BLEND_NAME=globals().get('BLEND_NAME','CreatureBatch2.blend')
REPORT_NAME=globals().get('REPORT_NAME','projection-report-batch2.json')
INITIAL_GROUP=GROUPS[0]
objects={key:[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('creature')==key] for key in GROUPS}
for key,parts in objects.items():
    bpy.ops.object.select_all(action='DESELECT')
    for obj in parts: obj.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]
    bpy.ops.export_scene.fbx(filepath=str(globals().get('EXPORT_PATHS',{}).get(key,OUT/(key+'.fbx'))),use_selection=True,object_types={'MESH'},apply_unit_scale=True,
        axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')

# Studio renders and camera-pose search for actual 16x16 reverse projections.
world=bpy.data.worlds.new('Neutral studio'); bpy.context.scene.world=world; world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.14,.17,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.45
for location,power,size in [((-2,-3,5),450,4),((3,2,4),300,3)]:
    data=bpy.data.lights.new('Softbox','AREA'); data.energy=power; data.size=size
    obj=bpy.data.objects.new('Softbox',data); bpy.context.collection.objects.link(obj); obj.location=location
    obj.rotation_euler=(Vector((0,0,.4))-obj.location).to_track_quat('-Z','Y').to_euler()
camera_data=bpy.data.cameras.new('Interpretation camera'); camera=bpy.data.objects.new('Interpretation camera',camera_data)
bpy.context.collection.objects.link(camera); camera_data.type='ORTHO'
scene=bpy.context.scene; scene.camera=camera; scene.render.engine='CYCLES'; scene.cycles.samples=16
scene.render.film_transparent=True; scene.render.image_settings.color_mode='RGBA'
source=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text()
tile_entries={name:rows.strip().splitlines() for number,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',source,re.M)}
tile_entries.update(globals().get('SOURCE_TILE_ENTRIES',{}))
report=[]
for key in GROUPS:
    # Partial revisions may preserve unrelated meshes in the same native scene.
    # Hide those too, so they cannot contaminate a selected group's studio view.
    for obj in bpy.context.scene.objects:
        if obj.type=='MESH': obj.hide_render=obj.get('creature')!=key
    for group,parts in objects.items():
        for obj in parts: obj.hide_render=group!=key
    bpy.context.view_layer.update()
    points=[o.matrix_world@Vector(corner) for o in objects[key] for corner in o.bound_box]
    center=sum(points,Vector())/len(points)
    low=Vector(tuple(min(p[i] for p in points) for i in range(3)))
    high=Vector(tuple(max(p[i] for p in points) for i in range(3)))
    center=(low+high)*.5
    def aim(yaw,elevation,scale):
        a=math.radians(yaw); e=math.radians(elevation)
        camera.location=center+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*5
        camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
        camera_data.ortho_scale=scale
        camera_data.shift_x=0; camera_data.shift_y=0
    scene.render.resolution_x=800; scene.render.resolution_y=800; scene.render.resolution_percentage=100
    for view,yaw,elevation in [('three-quarter',-125,30),('rear',55,25)]:
        aim(yaw,elevation,max((high-low).length*1.1,1.1))
        scene.render.filepath=str(OUT/(key+'-'+view+'.png')); bpy.ops.render.render(write_still=True)
    rows=[r.strip() for r in tile_entries[globals().get('SOURCE_TILE_NAMES',{}).get(key,key.replace('_',' ')+',male')]]
    is_bat=key in {'bat','giant_bat','vampire_bat'}
    # The bat tiles have a separate shadow silhouette in rows 9-15. Their
    # upper black pixels are anatomy, especially the all-black vampire bat.
    excluded={'.'} if is_bat else {'.','A'} | ({'B'} if key in {'winter_wolf_cub','winter_wolf'} else {'P'} if key in {'dog','large_dog','rabid_rat'} else set())
    target={(x,15-y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch not in excluded and (not is_bat or y<9)}
    spatial_shadow=[];mask_method='detached_shadow_rows' if is_bat else 'palette_heuristic'
    if key in {'jaguar','lynx','tiger','hell_hound_pup','hell_hound','valkyrie_female_human','barbarian_male_human','kobold','large_kobold','kobold_leader','kobold_shaman','kobold_mummy','kobold_zombie'} | set(globals().get('SPATIAL_MASK_KEYS',[])):
        # Retain enclosed black coat markings; exclude black regions reachable
        # from the background (a conservative cast-shadow diagnostic).
        foreground={(x,y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch not in {'.','A'}}
        outside=set();pending=[(x,y) for x in range(16) for y in range(16) if x in {0,15} or y in {0,15}]
        while pending:
            x,y=pending.pop()
            if not (0<=x<16 and 0<=y<16) or (x,y) in outside or (x,y) in foreground:continue
            outside.add((x,y));pending.extend([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
        black={(x,y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch=='A' and (x,y) not in outside}
        if key=='lynx':black|={(0,5),(5,5),(4,6)}  # Reviewed dark ear-tuft pixels.
        target={(x,15-y) for x,y in foreground|black}
        spatial_shadow=sorted((x,y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch=='A' and (x,y) not in black)
        excluded={'.'};mask_method='coloured_figure_with_enclosed_black_marks'
    elif key in {'pony','horse','warhorse'}:
        mouths={'pony':{(4,6),(3,7)},'horse':{(4,6),(3,7)},'warhorse':{(4,6),(3,7)}}
        retained=mouths[key]
        spatial_shadow=sorted((x,y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch=='A' and (x,y) not in retained)
        target={(x,15-y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch!='.' and (ch!='A' or (x,y) in retained)}
        excluded={'.'};mask_method='reviewed_equine_shadow_fringe_mouth_retained'
    elif key in {'white_unicorn','gray_unicorn','black_unicorn'}:
        mouth={(4,6),(3,7)}
        if key=='black_unicorn':
            # Its A body replaces white N/O pixels, and its P shadow replaces
            # white A fringe. Match spatial anatomy against the paired white tile,
            # retaining both the real black body and the coloured nostril accents.
            paired=[r.strip() for r in tile_entries['white unicorn,male']]
            keep={(x,y) for y,row in enumerate(paired) for x,ch in enumerate(row) if ch not in {'.','A'}}|mouth
            target={(x,15-y) for x,y in keep if rows[y][x]!='.'}
            spatial_shadow=sorted((x,y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch!='.' and (x,y) not in keep)
            mask_method='paired_white_unicorn_anatomy_black_body_retained'
        else:
            target={(x,15-y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch!='.' and (ch!='A' or (x,y) in mouth)}
            spatial_shadow=sorted((x,y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch=='A' and (x,y) not in mouth)
            mask_method='unicorn_shadow_fringe_mouth_and_mane_retained'
        excluded={'.'}
    elif key=='panther':
        # Preserve its black body, head, tail and limbs. Only the reviewed outer
        # fringe is dropped; this small ambiguous mask is not anatomical truth.
        spatial_shadow=[(14,9),(14,10),(14,11),(13,12),(2,13),(3,13),(8,13),(9,13)]
        target={(x,15-y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch!='.' and (x,y) not in spatial_shadow}
        excluded={'.'};mask_method='reviewed_panther_fringe_black_anatomy_retained'
    if key in globals().get('SOURCE_FIGURE_MASKS',{}):
        keep=set(SOURCE_FIGURE_MASKS[key])
        target={(x,15-y) for x,y in keep if rows[y][x]!='.'}
        spatial_shadow=sorted((x,y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch!='.' and (x,y) not in keep)
        excluded={'.'};mask_method='explicit_reviewed_spatial_mask_dark_anatomy_retained'
    target_width=max(x for x,y in target)-min(x for x,y in target)+1
    target_height=max(y for x,y in target)-min(y for x,y in target)+1
    candidates=[]; scene.render.resolution_x=16; scene.render.resolution_y=16; scene.cycles.samples=8
    for yaw in globals().get('PROJECTION_YAWS',([-180,-155,-125] if is_bat else [-115,-90,-65])):
        for elevation in [25,45]:
            aim(yaw,elevation,1)
            inverse=camera.rotation_euler.to_matrix().transposed()
            projected=[inverse@(p-center) for p in points]
            width=max(p.x for p in projected)-min(p.x for p in projected)
            height=max(p.y for p in projected)-min(p.y for p in projected)
            camera_data.ortho_scale=max(width*16/(target_width+1),height*16/(target_height+1))
            target_x=(min(x for x,y in target)+max(x for x,y in target)+1)/32-.5
            target_y=(min(y for x,y in target)+max(y for x,y in target)+1)/32-.5
            camera_data.shift_x=(min(p.x for p in projected)+max(p.x for p in projected))*.5/camera_data.ortho_scale-target_x
            camera_data.shift_y=(min(p.y for p in projected)+max(p.y for p in projected))*.5/camera_data.ortho_scale-target_y
            path=OUT/(key+f'-pixel-{yaw}-{elevation}.png'); scene.render.filepath=str(path)
            bpy.ops.render.render(write_still=True)
            image=bpy.data.images.load(str(path),check_existing=False)
            rgba=list(image.pixels); silhouette={(i%16,i//16) for i in range(256) if rgba[i*4+3]>.5}
            iou=len(silhouette&target)/max(1,len(silhouette|target))
            candidates.append(dict(yaw=yaw,elevation=elevation,silhouette_iou=round(iou,4),file=path.name))
            bpy.data.images.remove(image)
    report.append(dict(key=key,mask_method=mask_method,excluded_shadow_pixels=spatial_shadow,excluded_shadow_palette=sorted(excluded- {'.'}),excluded_shadow_rows=list(range(9,16)) if is_bat else [],bounds_m=[list(low),list(high)],best_projection=max(candidates,key=lambda c:c['silhouette_iou']),candidates=candidates))
    scene.cycles.samples=16
for parts in objects.values():
    for obj in parts: obj.hide_render=False
scene.render.resolution_x=800; scene.render.resolution_y=800
for key,parts in objects.items():
    collection=bpy.data.collections.new(key); scene.collection.children.link(collection)
    for obj in parts:
        for parent in list(obj.users_collection): parent.objects.unlink(obj)
        collection.objects.link(obj); obj.hide_render=key!=INITIAL_GROUP
    collection.hide_viewport=key!=INITIAL_GROUP
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/BLEND_NAME))
(OUT/REPORT_NAME).write_text(json.dumps(report,indent=2))
print('CREATURE_INTERPRETATIONS_READY count='+str(len(GROUPS)),flush=True)
