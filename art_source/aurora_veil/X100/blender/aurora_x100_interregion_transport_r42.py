"""EXOVANT-X100 V2 — Aurora inter-region transport r42.

Builds three terrain-supported route meshes and deterministic service markers from the r42 contract.
Requires the existing Aurora terrain, AUR-INF-002 beacon mesh and optionally AUR-INF-003 service junction.
Does not modify terrain topology. Collision/HLOD contracts are zero-scene-user datablocks.
"""
import bpy, math, json
from mathutils import Vector
from mathutils.bvhtree import BVHTree

WORKUNIT='AUR-X100-INTERREGION-TRANSPORT-001'
ROUTE_WIDTH=6.5
ROUTES={
 'CAMP_PLAIN':{'id':'AUR-ROUTE-CP-001','waypoints':[(-1600,350),(-1300,330),(-1000,300),(-700,260),(-400,220),(-150,170)],'class':'PRIMARY'},
 'PLAIN_ORCHARD':{'id':'AUR-ROUTE-PO-001','waypoints':[(-150,170),(-150,320),(100,400),(400,450),(700,460),(1000,420),(1300,350),(1500,300)],'class':'PRIMARY'},
 'CAMP_ORCHARD_BYPASS':{'id':'AUR-ROUTE-COB-001','waypoints':[(-1600,350),(-1300,380),(-900,390),(-450,410),(0,420),(500,430),(950,430),(1350,390),(1500,340)],'class':'SECONDARY_SERVICE_BYPASS'},
}

def chaikin(pts,it=3):
    out=[tuple(p) for p in pts]
    for _ in range(it):
        n=[out[0]]
        for a,b in zip(out[:-1],out[1:]):
            n += [(0.75*a[0]+0.25*b[0],0.75*a[1]+0.25*b[1]),(0.25*a[0]+0.75*b[0],0.25*a[1]+0.75*b[1])]
        n.append(out[-1]); out=n
    return out

def densify(pts,step=18):
    out=[]
    for a,b in zip(pts[:-1],pts[1:]):
        L=math.hypot(b[0]-a[0],b[1]-a[1]); n=max(1,int(math.ceil(L/step)))
        for j in range(n):
            t=j/n; out.append((a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t))
    out.append(pts[-1]); return out

def boxmesh(name,dims,mat=None):
    x,y,z=dims
    V=[(-x/2,-y/2,-z/2),(x/2,-y/2,-z/2),(x/2,y/2,-z/2),(-x/2,y/2,-z/2),(-x/2,-y/2,z/2),(x/2,-y/2,z/2),(x/2,y/2,z/2),(-x/2,y/2,z/2)]
    F=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]
    m=bpy.data.meshes.new(name);m.from_pydata(V,[],F);m.update()
    if mat:m.materials.append(mat)
    return m

def build():
    scene=bpy.context.scene
    # Cleanup only this workunit.
    for c in list(bpy.data.collections):
        if c.name in {'51_X100_INTERREGION_TRANSPORT','52_X100_INTERREGION_MARKERS','53_X100_INTERREGION_META'}:
            for o in list(c.objects): bpy.data.objects.remove(o,do_unlink=True)
            bpy.data.collections.remove(c)
    for m in list(bpy.data.meshes):
        if m.name.startswith('AUR_X100_ROUTE_') or m.name.startswith('AUR_HLOD_ROUTE_') or m.name.startswith('COL_AUR_ROUTE_'):
            if m.users==0 or m.use_fake_user:bpy.data.meshes.remove(m)
    cols={}
    for n in ['51_X100_INTERREGION_TRANSPORT','52_X100_INTERREGION_MARKERS','53_X100_INTERREGION_META']:
        c=bpy.data.collections.new(n);scene.collection.children.link(c);cols[n]=c

    roadmat=bpy.data.materials.get('AUR_MAT_COMPACTED_ROUTE_R42')
    if not roadmat:
        roadmat=bpy.data.materials.new('AUR_MAT_COMPACTED_ROUTE_R42');roadmat.use_nodes=True
        p=roadmat.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(0.095,0.082,0.071,1);p.inputs['Roughness'].default_value=.94;p.inputs['Metallic'].default_value=.02
    steel=bpy.data.materials.get('AUR_MAT_STRUCTURAL_GALV_STEEL') or bpy.data.materials.get('M_AUR_PRECISION_STEEL')
    terrain=bpy.data.objects['AURORA_MACRO_TERRAIN'];deps=bpy.context.evaluated_depsgraph_get();bvh=BVHTree.FromObject(terrain.evaluated_get(deps),deps);Mi=terrain.matrix_world.inverted();M=terrain.matrix_world
    def z_at(x,y):
        h=bvh.ray_cast(Mi@Vector((x,y,250)),(Mi.to_3x3()@Vector((0,0,-1))).normalized(),600)
        if h[0] is None:raise RuntimeError(f'terrain miss {x},{y}')
        return float((M@h[0]).z)
    stake=boxmesh('AUR_X100_ROUTE_EDGE_STAKE_MESH',(0.14,0.14,1.1),steel);stake['asset_family_id']='AUR-ROUTE-KIT-EDGE-001';stake['purpose']='route edge delineation / weather-service visibility'
    pull=boxmesh('AUR_X100_ROUTE_PULLOFF_MARKER_MESH',(0.26,0.26,1.6),steel);pull['asset_family_id']='AUR-ROUTE-KIT-PULLOFF-001';pull['purpose']='emergency pull-off marker'
    beacon_obj=bpy.data.objects.get('LIB_AUR_INF_002_ROUTE_BEACON');beacon=beacon_obj.data if beacon_obj and beacon_obj.type=='MESH' else None
    service=bpy.data.meshes.get('AUR_X100_INF_SERVICE_JUNCTION_MESH')
    def instance(name,mesh,loc,rot,props):
        o=bpy.data.objects.new(name,mesh);o.location=loc;o.rotation_euler[2]=rot;cols['52_X100_INTERREGION_MARKERS'].objects.link(o)
        for k,v in props.items():o[k]=v
        return o
    records=[]
    route_centers={}
    for name,spec in ROUTES.items():
        pts=densify(chaikin(spec['waypoints'],3),18);half=ROUTE_WIDTH/2;V=[];F=[];top=[];bottom=[];center=[];dist=[0.0];grades=[];cross=[];prev=None
        for i,(x,y) in enumerate(pts):
            if i==0:tx=pts[1][0]-x;ty=pts[1][1]-y
            elif i==len(pts)-1:tx=x-pts[i-1][0];ty=y-pts[i-1][1]
            else:tx=pts[i+1][0]-pts[i-1][0];ty=pts[i+1][1]-pts[i-1][1]
            L=max(1e-6,math.hypot(tx,ty));nx=-ty/L;ny=tx/L;zl=z_at(x+nx*half,y+ny*half);zr=z_at(x-nx*half,y-ny*half);cross.append(abs(zl-zr)/ROUTE_WIDTH*100)
            if zl>=zr:lz=zl+.08;rz=lz-min(zl-zr,.195)
            else:rz=zr+.08;lz=rz-min(zr-zl,.195)
            k=len(V);V += [(x+nx*half,y+ny*half,lz),(x-nx*half,y-ny*half,rz),(x+nx*half,y+ny*half,zl+.015),(x-nx*half,y-ny*half,zr+.015)];top.append((k,k+1));bottom.append((k+2,k+3));z=(lz+rz)/2;center.append((x,y,z,math.atan2(ty,tx),nx,ny))
            if prev:
                ds=math.hypot(x-prev[0],y-prev[1]);dist.append(dist[-1]+ds);grades.append(abs(z-prev[2])/max(ds,1e-6)*100)
            prev=(x,y,z)
        for i in range(len(pts)-1):
            l0,r0=top[i];l1,r1=top[i+1];tl0,tr0=bottom[i];tl1,tr1=bottom[i+1];F += [(l0,r0,r1,l1),(l0,l1,tl1,tl0),(r0,tr0,tr1,r1)]
        mesh=bpy.data.meshes.new(f'AUR_X100_ROUTE_{name}_MESH');mesh.from_pydata(V,[],F);mesh.update();mesh.materials.append(roadmat);mesh['asset_family_id']=spec['id'];mesh['route_class']=spec['class'];mesh['width_m']=ROUTE_WIDTH;mesh['crossfall_max_pct']=3.0;mesh['construction']='compacted mineral fill route with terrain-bearing high edge and fill berm low edge';mesh['engine_runtime']='BLOCKED_EXO_012'
        o=bpy.data.objects.new(f'AUR_ROUTE_{name}',mesh);cols['51_X100_INTERREGION_TRANSPORT'].objects.link(o);o['route_id']=spec['id'];o['route_class']=spec['class'];o['Peregrino_width_m']=2.7;o['route_width_m']=ROUTE_WIDTH;o['handling_authority']='PROPOSAL_UNTIL_VEHICLE_PROFILE'
        route_centers[name]=center
        ns=80;nb=300;np=650;sc=bc=pc=svc=0
        for i,c in enumerate(center):
            d=dist[i];x,y,z,ang,nx,ny=c
            if d>=ns:
                for side in (-1,1):
                    sx=x+nx*(half+.45)*side;sy=y+ny*(half+.45)*side;instance(f'AUR_ROUTE_{name}_STAKE_{sc:03d}_{side:+d}',stake,(sx,sy,z_at(sx,sy)+.55),ang,{'route_id':spec['id'],'role':'EDGE_DELINEATOR'});sc+=1
                ns+=80
            if beacon and d>=nb:
                side=-1 if bc%2 else 1;sx=x+nx*(half+1.1)*side;sy=y+ny*(half+1.1)*side;instance(f'AUR_ROUTE_{name}_BEACON_{bc:02d}',beacon,(sx,sy,z_at(sx,sy)+.775),ang,{'route_id':spec['id'],'role':'ROUTE_RECORDER_BEACON','reused_family':'AUR-INF-002'});bc+=1;nb+=300
            if d>=np:
                side=1 if pc%2==0 else -1;sx=x+nx*(half+4.8)*side;sy=y+ny*(half+4.8)*side;instance(f'AUR_ROUTE_{name}_PULLOFF_{pc:02d}',pull,(sx,sy,z_at(sx,sy)+.8),ang,{'route_id':spec['id'],'role':'EMERGENCY_PULLOFF_MARKER','bay_width_proposal_m':7.0,'bay_length_proposal_m':14.0});pc+=1;np+=650
                if service:
                    ssx=x+nx*(half+5.6)*side;ssy=y+ny*(half+5.6)*side;instance(f'AUR_ROUTE_{name}_SERVICE_{svc:02d}',service,(ssx,ssy,z_at(ssx,ssy)+.675),ang,{'route_id':spec['id'],'role':'SERVICE_JUNCTION','reused_family':'AUR-INF-003'});svc+=1
        CV=[];CF=[];idx=list(range(0,len(center),4));
        if idx[-1]!=len(center)-1:idx.append(len(center)-1)
        for j in idx:
            x,y,z,ang,nx,ny=center[j];CV += [(x+nx*half,y+ny*half,z),(x-nx*half,y-ny*half,z)]
        for j in range(len(idx)-1):k=2*j;CF.append((k,k+1,k+3,k+2))
        cm=bpy.data.meshes.new(f'COL_AUR_ROUTE_{name}_MESH');cm.from_pydata(CV,[],CF);cm.update();cm.use_fake_user=True;cm['collision_role']='route_surface_contract';cm['engine_runtime']='BLOCKED_EXO_012';cm['route_id']=spec['id']
        gs=sorted(grades);cs=sorted(cross);records.append({'route_id':spec['id'],'class':spec['class'],'samples':len(center),'length_m':round(dist[-1],1),'width_m':ROUTE_WIDTH,'Peregrino_width_m':2.7,'grade_p95_pct':round(gs[int(.95*(len(gs)-1))],2),'grade_max_pct':round(max(gs),2),'raw_cross_slope_p95_pct':round(cs[int(.95*(len(cs)-1))],2),'raw_cross_slope_max_pct':round(max(cs),2),'engineered_crossfall_max_pct':3.0,'stakes':sc,'beacons':bc,'pull_offs':pc,'service_nodes':svc,'collision_mesh':cm.name})
    # coarse route-vista HLOD, no scene users
    HV=[];HF=[]
    for name,centers in route_centers.items():
        pts=centers[::8]
        if pts[-1]!=centers[-1]:pts.append(centers[-1])
        base=len(HV)//2
        for i,(x,y,z,ang,nx,ny) in enumerate(pts):HV += [(x+nx*4,y+ny*4,z+1),(x-nx*4,y-ny*4,z+1)]
        for j in range(len(pts)-1):k=2*(base+j);HF.append((k,k+1,k+3,k+2))
    hm=bpy.data.meshes.new('AUR_HLOD_ROUTE_NETWORK_L2_MESH');hm.from_pydata(HV,[],HF);hm.update();hm.use_fake_user=True;hm['group_id']='AUR-HLOD-ROUTE-001';hm['hlod_level']='HLOD2_VISTA';hm['engine_runtime']='BLOCKED_EXO_012';hm['source_route_count']=3
    contract={'schema_version':1,'protocol':'EXOVANT-X100-V2','workunit':WORKUNIT,'remote_revision_target':42,'route_width_m':ROUTE_WIDTH,'vehicle_reference':'AUR_PEREGRINO_ROUTE_RECORDER 5.8x2.7x2.4m','smoothing':'Chaikin x3 / ~18m samples','crossfall_rule':'fill-only high-edge bearing; low edge <=3% engineered crossfall with berm to terrain','routes':records,'hlod_mesh':hm.name,'hlod_scene_users':0,'runtime':'BLOCKED_EXO_012'}
    t=bpy.data.texts.get('AUR_INTERREGION_ROUTE_CONTRACT_R42.json') or bpy.data.texts.new('AUR_INTERREGION_ROUTE_CONTRACT_R42.json');t.clear();t.write(json.dumps(contract,indent=2));scene['x100_interregion_route_contract']='AUR-ROUTE-v1-r42';scene['status']='X100_INTERREGION_TRANSPORT_R42'
    return records

if __name__=='__main__':
    print(json.dumps(build(),indent=2))
