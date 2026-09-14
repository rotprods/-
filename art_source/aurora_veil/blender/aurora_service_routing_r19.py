"""Aurora Veil Camp proof contact + service routing r19.

Reconstructs the technically reviewed Camp foundation contact and service network from the
current modular proof interfaces. Blender 5.2. Final electrical classes and swept elbow
geometry remain pending.
"""
import bpy, math
from mathutils import Vector
from mathutils.bvhtree import BVHTree

CONTRACT='AUR-PROC-ROUTING-v1-r19'
SOCKET_CONTRACT='AUR-SOCKET-SERVICE-v1-r19'


def terrain_tools():
    terrain=bpy.data.objects['AURORA_MACRO_TERRAIN']; dg=bpy.context.evaluated_depsgraph_get(); eo=terrain.evaluated_get(dg); em=eo.to_mesh()
    verts=[eo.matrix_world@v.co for v in em.vertices]; polys=[list(p.vertices) for p in em.polygons]; bvh=BVHTree.FromPolygons(verts,polys,all_triangles=False)
    def ground(x,y):
        h=bvh.ray_cast(Vector((x,y,10000)),Vector((0,0,-1)),20000)[0]
        if h is None: raise RuntimeError(f'No terrain hit at {x},{y}')
        return h.z
    return eo,ground


def curve(col,name,pts,radius,mat,role):
    cu=bpy.data.curves.new(name,'CURVE'); cu.dimensions='3D'; cu.bevel_depth=radius; cu.bevel_resolution=3
    sp=cu.splines.new('POLY'); sp.points.add(len(pts)-1)
    for i,p in enumerate(pts): sp.points[i].co=(*p,1)
    o=bpy.data.objects.new(name,cu); col.objects.link(o); cu.materials.append(mat); o['asset_id']='AUR-INF-003'; o['routing_role']=role; o['radius_m']=radius; o['bend_status']='BLOCKOUT_POLYLINE_FINAL_ELBOW_RADIUS_PENDING'; return o


def box(col,name,loc,dims,mat):
    bpy.ops.mesh.primitive_cube_add(location=loc); o=bpy.context.object; o.name=name; o.dimensions=dims; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(mat)
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); o['asset_id']='AUR-INF-003'; o['manufacturing']='folded zinc-coated junction enclosure with removable cover'; return o


def length(pts): return sum((Vector(pts[i])-Vector(pts[i-1])).length for i in range(1,len(pts)))


def build():
    scene=bpy.context.scene; eo,ground=terrain_tools(); proof=bpy.data.collections['15B_PROOF_ASSEMBLY']; root=bpy.data.objects['AUR_CAMP_REFUGE_MODULAR_PROOF_A']
    pads=sorted([o for o in proof.objects if o.name.startswith('AUR_PROOF_PAD_')],key=lambda o:o.name)
    # Repair only the historical r18 double-shift case: healthy proof child locals are small (~0..4m).
    children=[o for o in proof.objects if o.parent==root and o.name.startswith('AUR_PROOF_')]
    median_abs=sorted(abs(o.location.z) for o in children)[len(children)//2] if children else 0
    if median_abs>10 and not root.get('r19_child_local_z_repaired',False):
        shift=float(root.get('uniform_platform_shift_m',17.112))
        for o in children: o.location.z-=shift; o['hierarchy_contact_revision']=19
        root['r19_child_local_z_repaired']=True
    heights=[ground(o.matrix_world.translation.x,o.matrix_world.translation.y) for o in pads]
    maxg=max(heights); ming=min(heights); root.location.z=maxg+.275-.08
    root['foundation_strategy']='LEVEL_PLATFORM_ON_VARIABLE_STEEL_PIERS; pad plane keyed to highest terrain -0.08m embed'; root['terrain_ground_min_m']=ming; root['terrain_ground_max_m']=maxg
    bpy.context.view_layer.update()
    # Foundation piers.
    for o in list(proof.objects):
        if o.name.startswith('AUR_PROOF_FOUNDATION_PIER_'): bpy.data.objects.remove(o,do_unlink=True)
    steel=bpy.data.materials['AUR_MAT_STRUCTURAL_GALV_STEEL']; piers=[]
    for idx,pad in enumerate(pads):
        w=pad.matrix_world.translation; g=ground(w.x,w.y); bottom=w.z-pad.dimensions.z/2
        if bottom-g<=.03: continue
        name=f'AUR_PROOF_FOUNDATION_PIER_{idx:02d}'; cu=bpy.data.curves.new(name+'_CURVE','CURVE'); cu.dimensions='3D'; cu.bevel_depth=.10; cu.bevel_resolution=3
        sp=cu.splines.new('POLY'); sp.points.add(1); sp.points[0].co=(w.x,w.y,g-.05,1); sp.points[1].co=(w.x,w.y,bottom,1)
        o=bpy.data.objects.new(name,cu); proof.objects.link(o); cu.materials.append(steel); o['asset_id']='AUR-ARC-003'; o['manufacturing']='adjustable galvanized steel foundation pier / jack'; o['length_m']=bottom-(g-.05); piers.append(o)
    # Re-ground clock/beacons independently.
    clock=bpy.data.objects['AUR_CLOCK_SYNC_PROOF_BASE']; head=bpy.data.objects['AUR_CLOCK_SYNC_PROOF_HEAD']; g=ground(clock.location.x,clock.location.y); target=g+clock.dimensions.z/2-.08; d=target-clock.matrix_world.translation.z; clock.location.z+=d; head.location.z+=d
    beacons=sorted([o for o in proof.objects if o.name.startswith('AUR_ROUTE_BEACON_PROOF_')],key=lambda o:o.name)
    for o in beacons:
        w=o.matrix_world.translation; g=ground(w.x,w.y); o.location.z+=g+o.dimensions.z/2-.05-w.z
    bpy.context.view_layer.update()
    # Rebuild route collection.
    root_col=bpy.data.collections.get('AURORA_VEIL_ROOT') or scene.collection; routing=bpy.data.collections.get('23_CAMP_SERVICE_ROUTING') or bpy.data.collections.new('23_CAMP_SERVICE_ROUTING')
    if routing.name not in [c.name for c in root_col.children]:
        try: root_col.children.link(routing)
        except RuntimeError: pass
    for o in list(routing.objects): bpy.data.objects.remove(o,do_unlink=True)
    boxmat=bpy.data.materials['AUR_MAT_SERVICE_TRAY']; pmat=bpy.data.materials['AUR_MAT_CABLE_POWER_JACKET']; dmat=bpy.data.materials['AUR_MAT_CABLE_DATA_JACKET']
    trays=sorted([o for o in proof.objects if o.name.startswith('AUR_PROOF_SERVICE_TRAY_')],key=lambda o:o.name); last=trays[-1]; tl=last.matrix_world.translation; tray=(tl.x+last.dimensions.x/2,tl.y,tl.z)
    cw=clock.matrix_world.translation; jh=(tray[0]+1,tray[1],tray[2]-.18); jl=(jh[0],jh[1],ground(jh[0],jh[1])+.72); jc=(cw.x,cw.y,ground(cw.x,cw.y)+.65)
    box(routing,'AUR_ROUTING_JBOX_TRAY_EXIT',jh,(.62,.42,.72),boxmat); box(routing,'AUR_ROUTING_JBOX_GROUND_RISER',jl,(.58,.40,.68),boxmat); box(routing,'AUR_ROUTING_JBOX_CLOCK',jc,(.58,.40,.68),boxmat)
    ppts=[tray,jh,jl,jc]; power=curve(routing,'AUR_ROUTE_POWER_TRAY_TO_CLOCK',ppts,.045,pmat,'POWER_TRUNK_TO_CLOCK'); power['length_m']=length(ppts); power['min_bend_radius_target_m']=.22; power['voltage_class']='UNSPECIFIED_PENDING_ELECTRICAL_CANON'
    control=[(cw.x,cw.y)]+[(o.matrix_world.translation.x,o.matrix_world.translation.y) for o in beacons]
    sampled=[]
    for si in range(1,len(control)):
        a=Vector(control[si-1]); b=Vector(control[si]); dist=(b-a).length; count=max(1,math.ceil(dist/6))
        for j in range(count):
            if si>1 and j==0: continue
            q=a.lerp(b,j/count); sampled.append((q.x,q.y))
    sampled.append(control[-1])
    def offset(sign):
        out=[]
        for i,(x,y) in enumerate(sampled):
            p0=Vector(sampled[max(0,i-1)]); p1=Vector(sampled[min(len(sampled)-1,i+1)]); d=p1-p0; d=d.normalized() if d.length else Vector((1,0)); n=Vector((-d.y,d.x)); q=Vector((x,y))+n*(.065*sign); out.append((q.x,q.y,ground(q.x,q.y)+.45))
        return out
    apts,bpts=offset(-1),offset(1); da=curve(routing,'AUR_ROUTE_DATA_A_CLOCK_TO_BEACONS',apts,.022,dmat,'DATA_REDUNDANT_A'); db=curve(routing,'AUR_ROUTE_DATA_B_CLOCK_TO_BEACONS',bpts,.022,dmat,'DATA_REDUNDANT_B')
    for o,pts in ((da,apts),(db,bpts)): o['length_m']=length(pts); o['ground_clearance_m']=.45; o['min_bend_radius_target_m']=.12
    # Shared stake mesh, no source object.
    sx=sy=.06; z0=-.36; z1=.36; vs=[(-sx,-sy,z0),(sx,-sy,z0),(sx,sy,z0),(-sx,sy,z0),(-sx,-sy,z1),(sx,-sy,z1),(sx,sy,z1),(-sx,sy,z1)]; fs=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]
    mesh=bpy.data.meshes.get('AUR_CABLE_STAKE_SHARED_MESH_R18') or bpy.data.meshes.new('AUR_CABLE_STAKE_SHARED_MESH_R18')
    if len(mesh.vertices)==0: mesh.from_pydata(vs,[],fs); mesh.update(); mesh.materials.append(boxmat)
    stakes=[]
    for i,(x,y,z) in enumerate(apts):
        if i==0 or i==len(apts)-1 or i%3: continue
        o=bpy.data.objects.new(f'AUR_CABLE_STAKE_{len(stakes):02d}',mesh); routing.objects.link(o); o.location=(x,y,ground(x,y)+.36); o['asset_id']='AUR-INF-003'; stakes.append(o)
    last['socket_service_out_world']=list(tray); last['socket_contract']=SOCKET_CONTRACT; clock['socket_power_in_world']=list(jc); clock['socket_data_out_world']=[cw.x,cw.y,ground(cw.x,cw.y)+.45]; clock['socket_contract']=SOCKET_CONTRACT
    for o in beacons:
        w=o.matrix_world.translation; o['socket_data_in_world']=[w.x,w.y,ground(w.x,w.y)+.45]; o['socket_contract']=SOCKET_CONTRACT
    routing['routing_contract']=CONTRACT; routing['proof_contact_revision']=19; routing['foundation_pier_count']=len(piers); routing['final_electrical_spec']='PENDING'; routing['final_bend_elbows']='PENDING'
    scene['camp_routing_contract']=CONTRACT; scene['camp_proof_contact_revision']=19; scene['status']='WAVE2_CAMP_PROOF_HIERARCHY_ROUTING_R19'; eo.to_mesh_clear()
    return {'piers':len(piers),'power_m':power['length_m'],'data_a_m':da['length_m'],'data_b_m':db['length_m'],'stakes':len(stakes)}

if __name__=='__main__': print(build())
