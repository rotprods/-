"""NACRE archive chamber MANUAL_REFERENCE_BUILD R2.

Reconstructs the geometry contract for NACRE-LOOK-ARCHIVE-CHAMBER-001 in Blender 5.2.
This is an explicit fallback because the connected client exposes image-to-3D model discovery
but no verified generic submit action. It must never be relabelled as Tripo/Meshy/Hunyuan output.
Proposal dimensions are witnesses, not planetary canon.
"""
import bpy, math
from mathutils import Vector


def ensure_world():
    if bpy.context.scene.world is None:
        bpy.context.scene.world = bpy.data.worlds.new('WORLD_NACRE_HERO')
    w=bpy.context.scene.world; w.use_nodes=True
    bg=w.node_tree.nodes.get('Background'); bg.inputs['Color'].default_value=(0.035,0.03,0.028,1); bg.inputs['Strength'].default_value=0.35


def make_mat(name, base, rough, metal=0.0):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*base,1); p.inputs['Roughness'].default_value=rough; p.inputs['Metallic'].default_value=metal
    if 'Coat Weight' in p.inputs: p.inputs['Coat Weight'].default_value=0.08 if metal<0.2 else 0.02
    return m


def assign(o,m):
    if o.data and hasattr(o.data,'materials'): o.data.materials.clear(); o.data.materials.append(m)


def align_z(o,n):
    o.rotation_mode='QUATERNION'; o.rotation_quaternion=Vector((0,0,1)).rotation_difference(Vector(n).normalized())


def look_at(o,target=(0,0,0)):
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()


def box(name,loc,dims,n,m,bevel=0.12):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=name; o.dimensions=dims; align_z(o,n)
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:
        b=o.modifiers.new('BEVEL','BEVEL'); b.width=bevel; b.segments=3
    assign(o,m); return o


def torus(name,loc,n,major,minor,m):
    bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=64,minor_segments=12,location=loc)
    o=bpy.context.object; o.name=name; align_z(o,n); assign(o,m)
    for p in o.data.polygons: p.use_smooth=True
    return o


def curve(name,pts,bevel,m):
    cu=bpy.data.curves.new(name+'_CURVE','CURVE'); cu.dimensions='3D'; cu.resolution_u=2; cu.bevel_depth=bevel; cu.bevel_resolution=3
    sp=cu.splines.new('POLY'); sp.points.add(len(pts)-1)
    for i,p in enumerate(pts): sp.points[i].co=(*p,1)
    o=bpy.data.objects.new(name,cu); bpy.context.collection.objects.link(o); assign(o,m); return o


def sdir(az_deg,el_deg=0):
    a=math.radians(az_deg); e=math.radians(el_deg)
    return Vector((math.cos(e)*math.cos(a),math.cos(e)*math.sin(a),math.sin(e))).normalized()


def tangents(n):
    n=Vector(n).normalized(); ref=Vector((0,0,1)) if abs(n.z)<0.9 else Vector((0,1,0)); t1=n.cross(ref).normalized(); return t1,n.cross(t1).normalized()


def camera(name,loc,lens=40):
    d=bpy.data.cameras.new(name+'_DATA'); d.lens=lens; d.sensor_width=36; o=bpy.data.objects.new(name,d); bpy.context.collection.objects.link(o); o.location=loc; look_at(o,(0,0,-2)); return o


def sun(name,rot,energy,angle):
    d=bpy.data.lights.new(name+'_DATA','SUN'); d.energy=energy; d.angle=math.radians(angle); o=bpy.data.objects.new(name,d); bpy.context.collection.objects.link(o); o.rotation_euler=tuple(math.radians(x) for x in rot); return o


def normalize_shell_material_slots(shell):
    """Boolean operations can append an unused NULL material slot in Blender 5.2.

    Remove only unreferenced trailing slots beyond the explicit outer/inner pair so a cold
    rebuild matches the qualified primary scene semantically and exports without phantom roles.
    """
    used={p.material_index for p in shell.data.polygons}
    for idx in reversed(range(len(shell.data.materials))):
        if idx >= 2 and idx not in used:
            shell.data.materials.pop(index=idx)


def build():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    sc=bpy.context.scene; sc.unit_settings.system='METRIC'; sc.unit_settings.scale_length=1.0; sc.render.engine='BLENDER_EEVEE'; sc.render.resolution_x=960; sc.render.resolution_y=960; sc.render.resolution_percentage=100; sc.render.image_settings.file_format='PNG'; ensure_world()
    outer=make_mat('MAT_NACRE_OUTER_MINERAL',(0.29,0.25,0.21),0.86)
    inner_m=make_mat('MAT_NACRE_INNER_LAYER',(0.63,0.57,0.50),0.34)
    dark=make_mat('MAT_NACRE_STRUCTURE_DARK',(0.07,0.075,0.08),0.38,0.66)
    repair=make_mat('MAT_NACRE_REPAIR_CERAMIC',(0.47,0.43,0.38),0.63,0.04)
    strata=make_mat('MAT_NACRE_GROWTH_STRATA',(0.38,0.32,0.27),0.78)
    lichen=make_mat('MAT_NACRE_BIO_TRACE',(0.12,0.18,0.11),0.9)
    scale=make_mat('MAT_SCALE_WITNESS',(0.18,0.42,0.55),0.55)
    floor_m=make_mat('MAT_NACRE_FLOOR',(0.10,0.085,0.075),0.95)

    bpy.ops.mesh.primitive_uv_sphere_add(segments=96,ring_count=64,radius=24.0,location=(0,0,0)); shell=bpy.context.object; shell.name='NACRE_HERO_ARCHIVE_SHELL'
    for p in shell.data.polygons: p.use_smooth=True
    shell.data.materials.append(outer); shell.data.materials.append(inner_m)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96,ring_count=64,radius=22.4,location=(0,0,0)); cavity=bpy.context.object
    md=shell.modifiers.new('HOLLOW_1P6M','BOOLEAN'); md.operation='DIFFERENCE'; md.solver='EXACT'; md.object=cavity; bpy.context.view_layer.objects.active=shell; bpy.ops.object.modifier_apply(modifier=md.name); bpy.data.objects.remove(cavity,do_unlink=True)
    for p in shell.data.polygons: p.material_index=1 if p.center.length<23.1 else 0
    shell['stable_id']='NACRE-LOOK-ARCHIVE-CHAMBER-001'; shell['proposal_diameter_m']=48.0; shell['proposal_wall_thickness_m']=1.6; shell['truth']='MANUAL_REFERENCE_BUILD'

    docks=[('A',sdir(-65,2)),('B',sdir(55,6)),('C',sdir(176,-4))]
    for label,n in docks:
        bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=5.2,depth=9.0,location=n*23.2); cut=bpy.context.object; align_z(cut,n)
        md=shell.modifiers.new('OPENING_'+label,'BOOLEAN'); md.operation='DIFFERENCE'; md.solver='EXACT'; md.object=cut; bpy.context.view_layer.objects.active=shell; bpy.ops.object.modifier_apply(modifier=md.name); bpy.data.objects.remove(cut,do_unlink=True)
        torus('NACRE_DOCK_'+label+'_LOAD_RING',n*24.35,n,5.55,0.48,dark); torus('NACRE_DOCK_'+label+'_MINERAL_RING',n*24.10,n,6.20,0.34,repair); torus('NACRE_DOCK_'+label+'_INNER_LIP',n*23.15,n,5.05,0.26,dark)
        t1,t2=tangents(n)
        for ri,t in enumerate((t1,-t1,t2,-t2),1):
            pts=[]
            for j in range(12):
                a=(j/11)*math.radians(25); d=(n*math.cos(a)+t*math.sin(a)).normalized(); pts.append(d*24.28)
            r=curve(f'NACRE_DOCK_{label}_LOAD_RIB_{ri:02d}',pts,0.34,dark); r['function']='dock_load_transfer'; r['era']='ERA_1_ARCHIVE_RETROFIT'
    normalize_shell_material_slots(shell)

    for label,n,w,h in [('A',sdir(126,18),2.9,3.5),('B',sdir(-154,-12),2.5,3.0)]:
        c=n*24.12; p=box('NACRE_SERVICE_HATCH_'+label,c,(w,h,0.22),n,repair,0.10); p['count_contract']='EXACTLY_TWO'; p['era']='ERA_2_CURRENT_MAINTENANCE'; t1,t2=tangents(n)
        for si,(off,dim) in enumerate(((t1*(w/2+0.15),(0.28,h+0.45,0.32)),(-t1*(w/2+0.15),(0.28,h+0.45,0.32)),(t2*(h/2+0.15),(w+0.45,0.28,0.32)),(-t2*(h/2+0.15),(w+0.45,0.28,0.32))),1): box(f'NACRE_HATCH_{label}_FRAME_{si:02d}',c+off+n*0.08,dim,n,dark,0.06)

    for i,lat in enumerate((-58,-48,-37,-27,-16,-5,8,19,31,43,54)):
        start=math.radians((i*37+15)%360); arc=math.radians(185+(i%4)*17); pts=[]
        for j in range(56):
            u=j/55; ang=start+arc*u; el=math.radians(lat+1.6*math.sin(ang*3+i*0.7)); rr=24.18+0.09*math.sin(ang*5+i); pts.append((rr*math.cos(el)*math.cos(ang),rr*math.cos(el)*math.sin(ang),rr*math.sin(el)))
        o=curve(f'NACRE_GROWTH_STRATUM_{i+1:02d}',pts,0.12+0.03*(i%3),strata); o['cause']='mineral_growth_lamination'; o['era']='ERA_0_ORIGINAL_GROWTH'

    for i,(az,el,w,h) in enumerate(((28,34,4.8,2.1),(-12,43,3.6,1.8),(105,-22,5.2,2.2),(205,31,4.0,2.0),(248,-28,3.2,1.6),(320,18,4.4,1.9)),1):
        n=sdir(az,el); o=box(f'NACRE_REPAIR_PATCH_{i:02d}',n*24.20,(w,h,0.18),n,repair,0.10); o['era']='ERA_2_REPAIR'; o['cause']='localized_shell_repair'; t1,t2=tangents(n)
        for ci,off in enumerate((t1*w*0.36,-t1*w*0.36),1): box(f'NACRE_REPAIR_PATCH_{i:02d}_CLEAT_{ci}',n*24.38+off,(0.32,h*0.82,0.20),n,dark,0.04)

    for i,(az,el,sx,sy) in enumerate(((20,-48,2.5,1.0),(72,-55,1.8,0.8),(145,-50,2.2,0.9),(225,-46,1.6,0.7),(300,-53,2.8,1.1)),1):
        n=sdir(az,el); box(f'NACRE_BIO_TRACE_{i:02d}',n*24.24,(sx,sy,0.06),n,lichen,0.12)['cause']='lower_shell_moisture_deposition'

    bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,-24.1)); fl=bpy.context.object; fl.name='NACRE_HERO_CONTEXT_FLOOR'; fl.dimensions=(140,140,0.2); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); assign(fl,floor_m); fl['context_only']=True
    bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=0.22,depth=1.4,location=(8,-30,-23.3)); body=bpy.context.object; body.name='SCALE_HUMAN_1P8M_BODY'; assign(body,scale); body['witness_height_m']=1.8; body['proposal_only']=True
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=0.2,location=(8,-30,-22.4)); head=bpy.context.object; head.name='SCALE_HUMAN_1P8M_HEAD'; assign(head,scale)

    a=camera('CAM_TARGET_A_3Q_FRONT',(64,-66,42),40); camera('CAM_TARGET_B_SIDE',(0,-92,0),55); camera('CAM_TARGET_C_REAR',(-66,62,34),42); camera('CAM_TARGET_D_TOP',(0,0,96),55); sc.camera=a
    sun('SUN_MNEME_KEY',(32,-18,28),3.0,18); sun('SUN_MNEME_FILL',(58,25,-118),1.25,25)
    ld=bpy.data.lights.new('POINT_ARCHIVE_BOUNCE_DATA','POINT'); ld.energy=520; ld.color=(0.75,0.64,0.50); ld.shadow_soft_size=12; lo=bpy.data.objects.new('POINT_ARCHIVE_BOUNCE',ld); bpy.context.collection.objects.link(lo); lo.location=(0,-18,-10)

    sc['claim_id']='CLM-NACRE-LOOKDEV-HERO-001'; sc['asset_id']='NACRE-LOOK-ARCHIVE-CHAMBER-001'; sc['build_class']='MANUAL_REFERENCE_BUILD'; sc['not_image_to_3d']=True; sc['proposal_diameter_m']=48.0; sc['proposal_wall_thickness_m']=1.6; sc['dock_count_contract']=3; sc['service_hatch_count_contract']=2; sc['human_gate_art']='OPEN'; sc['target_pack_identity_element']='fa973079-15b8-4648-a602-e1adb4e96655'; sc['source_target_jobs']='165810de-cdb8-40ee-8340-c13cd3eddcf0;3b988b0b-89c0-411c-bb12-294a8ab09b09;3db84e38-bcb6-4ed4-bf2b-59fe0de706e6;7d6e08d7-c9d0-4c25-bc07-0e10f05c28b0'; sc['qa_r2_floor_contact']='PHYSICAL_SLAB_TOP_Z_NEG24'; sc['qa_r2_witness']='EXACT_1P8M'; sc['qa_r2_shell_material_slots']='NO_UNUSED_TRAILING_SLOT'
    return shell


if __name__ == '__main__':
    build()
