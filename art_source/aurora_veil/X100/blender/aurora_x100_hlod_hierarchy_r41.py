"""Aurora Veil X100 V2 HLOD source-contract generator, revision 41.

Creates only Blender Mesh datablocks with fake users. It deliberately creates NO scene objects,
so HLOD proxies do not enter the default GLB before EXO-012 provides a runtime adapter.
Source render geometry is read-only and remains untouched.
"""
import bpy, math, json
from mathutils import Vector, Matrix

WORKUNIT='AUR-X100-HLOD-HIERARCHY-001'

def explicit_matrix(o):
    local = Matrix.Translation(o.location) @ o.rotation_euler.to_matrix().to_4x4() @ Matrix.Diagonal((o.scale.x,o.scale.y,o.scale.z,1.0))
    return (explicit_matrix(o.parent) @ local) if o.parent else local

def bbox(o):
    M=explicit_matrix(o); pts=[M@Vector(c) for c in o.bound_box]
    return [min(p[i] for p in pts) for i in range(3)], [max(p[i] for p in pts) for i in range(3)]

def union(obs):
    bs=[bbox(o) for o in obs if o.type in {'MESH','CURVE'}]
    return [min(b[0][i] for b in bs) for i in range(3)], [max(b[1][i] for b in bs) for i in range(3)]

def tri(o):
    return sum(max(0,len(p.vertices)-2) for p in o.data.polygons) if o.type=='MESH' else 0

def mesh_tri(m):
    return sum(max(0,len(p.vertices)-2) for p in m.polygons)

def add_box(V,F,mn,mx):
    i=len(V); x0,y0,z0=mn; x1,y1,z1=mx
    V += [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    F += [(i,i+1,i+2,i+3),(i+4,i+7,i+6,i+5),(i,i+4,i+5,i+1),(i+1,i+5,i+6,i+2),(i+2,i+6,i+7,i+3),(i+4,i,i+3,i+7)]

def add_ring(V,F,o,r0,r1,half_t,segs):
    M=explicit_matrix(o); base=len(V)
    for z in (-half_t,half_t):
        for r in (r0,r1):
            for k in range(segs):
                a=2*math.pi*k/segs; p=M@Vector((r*math.cos(a),r*math.sin(a),z)); V.append(tuple(p))
    def I(zl,rl,k): return base+zl*(2*segs)+rl*segs+(k%segs)
    for k in range(segs):
        n=k+1
        F += [(I(0,0,k),I(0,1,k),I(0,1,n),I(0,0,n)),(I(1,0,k),I(1,0,n),I(1,1,n),I(1,1,k)),(I(0,1,k),I(1,1,k),I(1,1,n),I(0,1,n)),(I(0,0,k),I(0,0,n),I(1,0,n),I(1,0,k))]

def mk(name,V,F,meta):
    old=bpy.data.meshes.get(name)
    if old: bpy.data.meshes.remove(old)
    m=bpy.data.meshes.new(name); m.from_pydata(V,[],F); m.update(); m.use_fake_user=True
    for k,v in meta.items(): m[k]=v
    return m

def rec(gid,src,m1,m2):
    mn,mx=union(src); src_tris=sum(tri(o) for o in src); src_objects=len(src)
    return {'group_id':gid,'source_objects':src_objects,'source_triangles':src_tris,'source_bbox_min':mn,'source_bbox_max':mx,
            'hlod1_mesh':m1.name,'hlod1_triangles':mesh_tri(m1),'hlod2_mesh':m2.name,'hlod2_triangles':mesh_tri(m2),
            'mesh_scene_users':[sum(1 for o in bpy.data.objects if o.data==m1),sum(1 for o in bpy.data.objects if o.data==m2)],
            'object_reduction_hlod1':round(1-1/max(1,src_objects),4),
            'triangle_reduction_hlod1':round(1-mesh_tri(m1)/max(1,src_tris),4),'triangle_reduction_hlod2':round(1-mesh_tri(m2)/max(1,src_tris),4)}

def build():
    for m in list(bpy.data.meshes):
        if m.name.startswith('AUR_HLOD_'): bpy.data.meshes.remove(m)

    # CAMP: exact per-cluster HLOD1 and per-row HLOD2 envelopes from every source object.
    camp=[]
    for cn in ['28_X100_CAMP_DISTRICT_PROOF','42_X100_CAMP_HISTORY_PROOF']:
        camp += [o for o in bpy.data.collections[cn].objects if o.type in {'MESH','CURVE'} and not o.hide_render]
    roots=[bpy.data.objects.get(f'AUR_X100_CAMP_CONFIG_{i:02d}') for i in range(12)]; roots=[r for r in roots if r]
    clusters={r.name:[] for r in roots}
    for o in camp:
        r=min(roots,key=lambda q:(o.location.x-q.location.x)**2+(o.location.y-q.location.y)**2); clusters[r.name].append(o)
    V=[];F=[]
    for r in roots:
        if clusters[r.name]: add_box(V,F,*union(clusters[r.name]))
    cmn,cmx=union(camp); cmeta={'group_id':'AUR-HLOD-CAMP-001','source_objects':len(camp),'source_triangles':sum(tri(o) for o in camp),'source_bbox_min':cmn,'source_bbox_max':cmx,'transform_rule':'EXPLICIT_LOCAL_MATRIX_R41','engine_runtime':'BLOCKED_EXO_012'}
    c1=mk('AUR_HLOD_CAMP_L1_MESH',V,F,{**cmeta,'hlod_level':'HLOD1','switch_role':'DISTRICT_MID_DISTANCE'})
    V=[];F=[]
    for y in sorted(set(round(r.location.y,3) for r in roots)):
        members=[]
        for r in roots:
            if abs(r.location.y-y)<1: members.extend(clusters[r.name])
        if members: add_box(V,F,*union(members))
    c2=mk('AUR_HLOD_CAMP_L2_MESH',V,F,{**cmeta,'hlod_level':'HLOD2','switch_role':'DISTRICT_FAR_DISTANCE'})

    # OBSERVATORY + ANNEX: preserve the tilted ring silhouette plus mast/support/annex envelopes.
    ring=bpy.data.objects['AUR_OBSERVATORY_PRIMARY_RING']; timing=bpy.data.objects['AUR_OBSERVATORY_TIMING_RING']; mast=bpy.data.objects['AUR_OBSERVATORY_MAST']
    supports=[bpy.data.objects[f'AUR_OBS_SUPPORT_{i}'] for i in range(4)]
    interior=[o for o in bpy.data.collections['48_X100_OBSERVATORY_INTERIOR_PROOF'].objects if o.type in {'MESH','CURVE'} and not o.hide_render]
    obs=[ring,timing,mast]+supports+interior; omn,omx=union(obs); imn,imx=union(interior)
    ometa={'group_id':'AUR-HLOD-OBS-001','source_objects':len(obs),'source_triangles':sum(tri(o) for o in obs),'source_bbox_min':omn,'source_bbox_max':omx,'transform_rule':'EXPLICIT_LOCAL_MATRIX_R41','engine_runtime':'BLOCKED_EXO_012','ring_envelope_basis':'oriented torus with conservative source-section radius'}
    V=[];F=[]; add_ring(V,F,ring,17.5,25.35,1.0,24); add_box(V,F,*bbox(mast)); [add_box(V,F,*bbox(s)) for s in supports]; add_box(V,F,imn,imx)
    o1=mk('AUR_HLOD_OBSERVATORY_L1_MESH',V,F,{**ometa,'hlod_level':'HLOD1','switch_role':'LANDMARK_MID_DISTANCE'})
    V=[];F=[]; add_ring(V,F,ring,17.0,25.5,1.1,12); add_box(V,F,*bbox(mast)); [add_box(V,F,*bbox(s)) for s in supports]; add_box(V,F,imn,imx)
    o2=mk('AUR_HLOD_OBSERVATORY_L2_MESH',V,F,{**ometa,'hlod_level':'HLOD2','switch_role':'LANDMARK_FAR_DISTANCE'})

    # Small mission sites: HLOD1 batches component envelopes; HLOD2 uses one coarse site envelope.
    def site(cname,prefix,gid):
        src=[o for o in bpy.data.collections[cname].objects if o.type in {'MESH','CURVE'} and not o.hide_render]
        smn,smx=union(src); smeta={'group_id':gid,'source_objects':len(src),'source_triangles':sum(tri(o) for o in src),'source_bbox_min':smn,'source_bbox_max':smx,'engine_runtime':'BLOCKED_EXO_012'}
        V=[];F=[]
        for o in src: add_box(V,F,*bbox(o))
        a=mk(f'AUR_HLOD_{prefix}_L1_MESH',V,F,{**smeta,'hlod_level':'HLOD1','switch_role':'SITE_MID_DISTANCE','optimization_note':'OBJECT_BATCHING_ONLY'})
        V=[];F=[]; add_box(V,F,smn,smx)
        b=mk(f'AUR_HLOD_{prefix}_L2_MESH',V,F,{**smeta,'hlod_level':'HLOD2','switch_role':'SITE_FAR_DISTANCE'})
        return src,a,b
    acc,a1,a2=site('44_X100_PLAIN_ACCIDENT_SITE','ACCIDENT','AUR-HLOD-ACC-001')
    res,r1,r2=site('45_X100_PLAIN_RESCUE_SITE','RESCUE','AUR-HLOD-RES-001')

    records=[rec('AUR-HLOD-CAMP-001',camp,c1,c2),rec('AUR-HLOD-OBS-001',obs,o1,o2),rec('AUR-HLOD-ACC-001',acc,a1,a2),rec('AUR-HLOD-RES-001',res,r1,r2)]
    contract={'schema_version':1,'protocol':'EXOVANT-X100-V2','workunit':WORKUNIT,'remote_revision_target':41,'switching':'CONTRACT_ONLY_BLOCKED_EXO_012','default_export':'SOURCE_GEOMETRY_ONLY_HLOD_DATABLOCKS_ZERO_SCENE_USERS','groups':records}
    txt=bpy.data.texts.get('AUR_HLOD_CONTRACT_R38.json') or bpy.data.texts.new('AUR_HLOD_CONTRACT_R38.json'); txt.clear(); txt.write(json.dumps(contract,indent=2))
    bpy.context.scene['x100_hlod_contract']='AUR-HLOD-v4-r41'; bpy.context.scene['x100_hlod_groups']=4; bpy.context.scene['x100_hlod_runtime']='BLOCKED_EXO_012'; bpy.context.scene['status']='X100_HLOD_HIERARCHY_R41_FINAL_ENVELOPE'
    return records

if __name__=='__main__':
    print(json.dumps(build(),indent=2))
