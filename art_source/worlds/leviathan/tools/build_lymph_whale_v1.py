"""EXOVANT 2950 — LEVIATHAN / LEV-ECO-002 Ballena de linfa representative anatomy v1.

Function-driven anatomy for the canonical "Ballena de linfa" ecology role.
Current canon names the organism but does not define exact dimensions, locomotion, cognition,
feeding cycle, rig, animation or gameplay. The existing 36 x 11 x 13 m proxy is treated only as
a blockout envelope reference.

Representative physical logic:
- long fusiform body aligned to the local lymph-flow direction;
- broad anterior intake mouth for lymph filtration;
- internal lamellar filtering combs and ventral filtered-flow outlet;
- paired dorsal pressure sacs / vascular reservoir;
- paired lateral control fins and paired tail lobes for slow-flow steering interface;
- cyan lateral pressure-line sensors;
- explicit sockets for mouth, filters, fins, tail, pressure sacs and root.

No collision authority, armature, animation, AI, locomotion or feeding gameplay is authored.
Claim: CLM-W10-WORLD-LEVIATHAN-001
Asset ID: LEV-ECO-002
"""
import bpy
import math
from mathutils import Vector

STAGE = "LYMPH_WHALE_REPRESENTATIVE_V1"
ASSET_ID = "LEV-ECO-002"
COLLECTION = "32_R2_LYMPH_WHALE_MICROSET"
ROOT_NAME = "R2_LYMPH_WHALE_ROOT"
ORIGIN = Vector((55.0, 168.0, 24.0))
REFERENCE_PROXY_DIMS = (36.0, 11.0, 13.0)


def _mat(name):
    m=bpy.data.materials.get(name)
    if m is None: raise RuntimeError(f"Required material missing: {name}")
    return m


def _link_only(o,col):
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o)


def _apply_scale(o):
    bpy.context.view_layer.objects.active=o; o.select_set(True)
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.select_set(False)


def _sphere(name,loc,dims,mat,col,seg=32,rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,radius=1.0,location=loc)
    o=bpy.context.object; o.name=name; o.scale=(dims[0]/2,dims[1]/2,dims[2]/2); _apply_scale(o); _link_only(o,col); o.data.materials.append(mat); return o


def _torus(name,loc,major,minor,mat,col,rot=(0,0,0),major_segments=40,minor_segments=10):
    bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=major_segments,minor_segments=minor_segments,location=loc,rotation=rot)
    o=bpy.context.object; o.name=name; _link_only(o,col); o.data.materials.append(mat); return o


def _curve(name,pts,bevel,mat,col):
    cu=bpy.data.curves.new(name+'_CURVE','CURVE'); cu.dimensions='3D'; cu.resolution_u=4; cu.bevel_depth=bevel; cu.bevel_resolution=2
    sp=cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts)-1)
    for bp,p in zip(sp.bezier_points,pts): bp.co=p; bp.handle_left_type='AUTO'; bp.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,cu); col.objects.link(o); cu.materials.append(mat); return o


def _fin(name,pts,thickness,mat,col):
    top=[Vector(p)+Vector((0,0,thickness*0.5)) for p in pts]; bot=[Vector(p)-Vector((0,0,thickness*0.5)) for p in pts]
    verts=[tuple(v) for v in top+bot]; n=len(pts); faces=[tuple(range(n)),tuple(range(2*n-1,n-1,-1))]
    for i in range(n):
        j=(i+1)%n; faces.append((i,j,n+j,n+i))
    me=bpy.data.meshes.new(name+'_MESH'); me.from_pydata(verts,[],faces); me.update(); o=bpy.data.objects.new(name,me); col.objects.link(o); me.materials.append(mat); return o


def _socket(name,loc,col,role):
    o=bpy.data.objects.new(name,None); o.empty_display_type='SPHERE'; o.empty_display_size=0.18; o.location=loc; col.objects.link(o)
    o['asset_id']=ASSET_ID; o['socket_role']=role; o['binding_status']='INTERFACE_ONLY_NO_RIG_OR_GAMEPLAY_BINDING'; return o


def _look_at(cam,target): cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()


def build():
    scene=bpy.context.scene; root_col=bpy.data.collections.get('LEV_W10_MASTER')
    if root_col is None: raise RuntimeError('LEV_W10_MASTER missing')
    old_proxy=bpy.data.objects.get('R2_BALLENA_LINFA_PROXY'); proxy_receipt=None
    if old_proxy:
        proxy_receipt={'location':[float(x) for x in old_proxy.location],'dimensions':[float(x) for x in old_proxy.dimensions],'collections':[c.name for c in old_proxy.users_collection]}
        bpy.data.objects.remove(old_proxy,do_unlink=True)
    old=bpy.data.collections.get(COLLECTION)
    if old:
        for o in list(old.all_objects): bpy.data.objects.remove(o,do_unlink=True)
        bpy.data.collections.remove(old)
    col=bpy.data.collections.new(COLLECTION); root_col.children.link(col)

    mats={'warm':_mat('LEV_MAT_TISSUE_WARM'),'dark':_mat('LEV_MAT_TISSUE_DARK'),'mem':_mat('LEV_MAT_MEMBRANE'),'cart':_mat('LEV_MAT_CARTILAGE'),'vascular':_mat('LEV_MAT_VASCULAR'),'mucosa':_mat('LEV_MAT_MUCOSA_WET'),'lumen':_mat('LEV_MAT_PRESSURE_LUMEN'),'cyan':_mat('SIGNAL_CYAN_MEMORY')}

    root=bpy.data.objects.new(ROOT_NAME,None); root.location=ORIGIN; root.empty_display_type='CUBE'; root.empty_display_size=0.65; col.objects.link(root)
    root['asset_id']=ASSET_ID; root['production_state']='REPRESENTATIVE_FUNCTIONAL_ANATOMY_NOT_FINAL'; root['reference_proxy_dims_m']=REFERENCE_PROXY_DIMS; root['reference_proxy_status']='BLOCKOUT_ENVELOPE_NOT_CANON'; root['ecology_role']='LYMPH_FLOW_FILTERING_ORGANISM'; root['dimension_status']='MEASURED_PROPOSAL_NOT_CANON'; root['locomotion_status']='NOT_AUTHORED'; root['feeding_gameplay']='NOT_AUTHORED'; root['collision_authority']='NONE'; root['rig_status']='SOCKETS_ONLY_NO_ARMATURE'; root['animation_status']='NOT_AUTHORED'; root['generator_stage']=STAGE

    # X axis is nose-to-tail. Body is deliberately inside the 36 m reference envelope.
    body=_sphere('LW_MAIN_BODY',ORIGIN+Vector((0.5,0,0)),(28.0,8.6,8.4),mats['warm'],col,40,20)
    head=_sphere('LW_FILTER_HEAD',ORIGIN+Vector((13.0,0,0.15)),(7.0,8.1,7.6),mats['mucosa'],col,36,18)
    tail_peduncle=_sphere('LW_TAIL_PEDUNCLE',ORIGIN+Vector((-13.3,0,-0.10)),(5.8,4.0,4.0),mats['warm'],col,28,14)
    for o in (body,head,tail_peduncle): o['asset_id']=ASSET_ID; o['collision_authority']='NONE'

    # Mouth ring opens forward (+X), torus normally around Z so rotate Y 90deg.
    mouth_center=ORIGIN+Vector((16.35,0,0.0))
    mouth=_torus('LW_FILTER_MOUTH_RING',mouth_center,2.65,0.30,mats['cart'],col,rot=(0,math.radians(90),0),major_segments=48,minor_segments=12)
    mouth['functional_role']='LYMPH_INTAKE_MOUTH_INTERFACE'; mouth['feeding_gameplay']='NOT_AUTHORED'; _socket('LW_SOCKET_MOUTH',mouth_center,col,'FILTER_MOUTH_CENTER')
    intake=_sphere('LW_INTAKE_LUMEN',ORIGIN+Vector((15.6,0,0)),(2.6,5.0,5.0),mats['dark'],col,28,14); intake['functional_role']='INTAKE_LUMEN_VISUAL'; intake['collision_authority']='NONE'

    # Eight internal lamellar comb rings reduce toward posterior; interfaces only.
    for i in range(8):
        x=ORIGIN.x+12.0-i*1.15; r=2.20-i*0.10
        ring=_torus(f'LW_FILTER_LAMELLA_{i}',Vector((x,ORIGIN.y,ORIGIN.z)),r,0.085,mats['mem'],col,rot=(0,math.radians(90),0),major_segments=36,minor_segments=8)
        ring['functional_role']='FILTER_LAMELLA'; ring['collision_authority']='NONE'
    _socket('LW_SOCKET_FILTER_BANK',ORIGIN+Vector((8.0,0,0)),col,'FILTER_BANK_ROOT')

    # Dorsal pressure sacs and vascular line.
    for i,xoff in enumerate((3.5,-3.8)):
        sac=_sphere(f'LW_DORSAL_PRESSURE_SAC_{i}',ORIGIN+Vector((xoff,0,3.45)),(6.4,3.6,1.7),mats['lumen'],col,28,14)
        sac['functional_role']='DORSAL_LYMPH_PRESSURE_RESERVOIR'; sac['collision_authority']='NONE'; _socket(f'LW_SOCKET_PRESSURE_SAC_{i}',ORIGIN+Vector((xoff,0,3.25)),col,f'PRESSURE_SAC_{i}')
    dorsal=_curve('LW_DORSAL_VASCULAR_LINE',[ORIGIN+Vector((10.0,0,2.8)),ORIGIN+Vector((4.0,0,3.65)),ORIGIN+Vector((-4.0,0,3.65)),ORIGIN+Vector((-10.0,0,2.65))],0.16,mats['vascular'],col); dorsal['functional_role']='DORSAL_PRESSURE_TRANSFER_VESSEL'; dorsal['collision_authority']='NONE'

    # Lateral fins. Y span kept within 11 m envelope.
    for side in (-1,1):
        tag='L' if side<0 else 'R'
        fin=_fin(f'LW_CONTROL_FIN_{tag}',[
            ORIGIN+Vector((4.0,side*3.2,-0.5)),
            ORIGIN+Vector((0.5,side*5.2,-0.7)),
            ORIGIN+Vector((-3.5,side*4.1,-1.0)),
            ORIGIN+Vector((-1.5,side*2.7,-0.7)),
        ],0.12,mats['mem'],col)
        fin['functional_role']='SLOW_FLOW_STEERING_FIN_INTERFACE'; fin['locomotion_status']='NOT_AUTHORED'; _socket(f'LW_SOCKET_FIN_{tag}',ORIGIN+Vector((2.0,side*3.0,-0.6)),col,f'FIN_{tag}_ROOT')

    # Bifurcated tail lobes, still inside 36m X envelope and 11m Y.
    tail_x=ORIGIN.x-16.0
    for side in (-1,1):
        tag='L' if side<0 else 'R'
        lobe=_fin(f'LW_TAIL_LOBE_{tag}',[
            ORIGIN+Vector((-14.3,0,0.0)),
            Vector((tail_x,ORIGIN.y+side*4.9,ORIGIN.z+0.15)),
            ORIGIN+Vector((-17.2,side*2.2,-0.1)),
            ORIGIN+Vector((-14.8,side*0.8,0.0)),
        ],0.15,mats['mem'],col)
        lobe['functional_role']='TAIL_FLOW_CONTROL_INTERFACE'; lobe['locomotion_status']='NOT_AUTHORED'; _socket(f'LW_SOCKET_TAIL_{tag}',ORIGIN+Vector((-14.4,side*0.55,0)),col,f'TAIL_{tag}_ROOT')

    # Ventral filtered-flow outlet and diagnostic pressure line.
    outlet=_torus('LW_FILTERED_FLOW_OUTLET',ORIGIN+Vector((-4.0,0,-3.85)),1.15,0.16,mats['cart'],col,rot=(math.radians(90),0,0),major_segments=36,minor_segments=8); outlet['functional_role']='FILTERED_LYMPH_OUTLET_INTERFACE'; outlet['collision_authority']='NONE'; _socket('LW_SOCKET_OUTLET',ORIGIN+Vector((-4.0,0,-3.85)),col,'FILTERED_FLOW_OUTLET')

    for side in (-1,1):
        tag='L' if side<0 else 'R'
        line=_curve(f'LW_PRESSURE_SENSOR_LINE_{tag}',[
            ORIGIN+Vector((10.5,side*3.25,0.65)),
            ORIGIN+Vector((3.0,side*4.1,0.95)),
            ORIGIN+Vector((-5.0,side*3.7,0.75)),
            ORIGIN+Vector((-11.0,side*2.6,0.45)),
        ],0.07,mats['cyan'],col)
        line['functional_role']='LATERAL_PRESSURE_SENSOR_LINE'; line['collision_authority']='NONE'
        for j,xoff in enumerate((7.0,1.0,-6.0)):
            node=_sphere(f'LW_PRESSURE_NODE_{tag}_{j}',ORIGIN+Vector((xoff,side*(3.35+0.15*j),0.85)),(0.28,0.28,0.28),mats['cyan'],col,12,6); node['functional_role']='PRESSURE_SENSOR_NODE'; node['collision_authority']='NONE'
        _socket(f'LW_SOCKET_SENSOR_LINE_{tag}',ORIGIN+Vector((3.0,side*4.1,0.95)),col,f'SENSOR_LINE_{tag}')

    _socket('LW_SOCKET_ROOT',ORIGIN,col,'ROOT')
    _socket('LW_SOCKET_HEAD',ORIGIN+Vector((12.8,0,0.15)),col,'HEAD_ROOT')
    _socket('LW_SOCKET_TAIL',ORIGIN+Vector((-14.0,0,0)),col,'TAIL_PEDUNCLE_ROOT')

    for o in list(col.objects):
        if o!=root:
            mw=o.matrix_world.copy(); o.parent=root; o.matrix_world=mw; o['asset_id']=ASSET_ID
            if 'collision_authority' not in o: o['collision_authority']='NONE'

    cam_data=bpy.data.cameras.new('CAM_LYMPH_WHALE_CLOSE_DATA'); cam=bpy.data.objects.new('CAM_LYMPH_WHALE_CLOSE',cam_data); col.objects.link(cam); cam.location=ORIGIN+Vector((30.0,-34.0,17.0)); cam_data.lens=54; _look_at(cam,ORIGIN+Vector((1,0,0.3))); cam['qa_only']=True

    scene['lymph_whale_stage']=STAGE; scene['lymph_whale_asset_id']=ASSET_ID; scene['lymph_whale_final_anatomy_claimed']=False
    meshes=[o for o in col.all_objects if o.type=='MESH']; curves=[o for o in col.all_objects if o.type=='CURVE']; sockets=[o for o in col.all_objects if o.type=='EMPTY' and o.name.startswith('LW_SOCKET_')]; tris=0
    for o in meshes: o.data.calc_loop_triangles(); tris+=len(o.data.loop_triangles)
    return {'stage':STAGE,'asset_id':ASSET_ID,'replaced_proxy':proxy_receipt,'mesh_objects':len(meshes),'curve_objects':len(curves),'interface_sockets':len(sockets),'native_mesh_triangles':tris,'collision_authority':'NONE','status':'REPRESENTATIVE_FUNCTIONAL_ANATOMY_NOT_FINAL'}

if __name__=='__main__':
    print(build())
