import bpy, math, random
from mathutils import Vector
random.seed(2950)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'
scene.unit_settings.scale_length=1.0
scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=1200
scene.render.resolution_y=960
scene.render.resolution_percentage=100
scene.render.image_settings.media_type='IMAGE'
scene.render.image_settings.file_format='PNG'
scene.render.fps=24
scene.frame_start=1
scene.frame_end=120
if not scene.world:
    scene.world=bpy.data.worlds.new('Reliquary studio atmosphere')
scene.world.use_nodes=True
bg=scene.world.node_tree.nodes.get('Background')
bg.inputs['Color'].default_value=(0.16,0.20,0.23,1)
bg.inputs['Strength'].default_value=0.38
scene.view_settings.view_transform='Khronos PBR Neutral'
COL={}
for name in ['01_Foundation','02_Structural_ring','03_Bronze_armour','04_Alignment_mechanism','05_Service_details','06_Amber_memory','07_Presentation']:
    c=bpy.data.collections.new(name);scene.collection.children.link(c);COL[name]=c
def move(o,col):
    for c in list(o.users_collection): c.objects.unlink(o)
    COL[col].objects.link(o)
def mat(name,color,metal=0,rough=.5,emission=0):
    m=bpy.data.materials.new(name);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=metal
    p.inputs['Roughness'].default_value=rough
    if emission:
        p.inputs['Emission Color'].default_value=(*color,1)
        p.inputs['Emission Strength'].default_value=emission
    m.diffuse_color=(*color,1)
    return m
black=mat('Black basalt ceramic',(0.037,.046,.047),.22,.6)
dark=mat('Recesses / carbon gasket',(.012,.022,.023),.1,.72)
bronzes=[mat('Bronze panel %02d'%i,(.20+i*.009,.135+i*.006,.072+i*.004),.76,.34+i*.013) for i in range(7)]
patina=mat('Oxidized copper plates',(.065,.18,.15),.56,.61)
copper=mat('Machined bronze edges',(.39,.245,.10),.83,.3)
steel=mat('Titanium fasteners',(.27,.30,.29),.86,.31)
ivory=mat('Human ceramic repair',(.62,.62,.51),.08,.45)
amber=mat('Memory amber',(.95,.31,.035),.18,.25,3.5)
cyan=mat('Calibration cyan',(.10,.57,.52),.15,.28,1.6)
floor=mat('Studio floor',(.055,.068,.067),.05,.72)
def finish(o,name,m,col,bevel=0):
    o.name=name;move(o,col);o.data.materials.append(m)
    if bevel:
        mod=o.modifiers.new('Manufactured edge radius','BEVEL');mod.width=bevel;mod.segments=3
        mod=o.modifiers.new('Face-weighted corner normals','WEIGHTED_NORMAL')
    return o
def box(name,loc,dim,m,col,bevel=.02):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object;o.scale=dim
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    return finish(o,name,m,col,bevel)
def cyl(name,loc,r,depth,m,col,rot=(math.pi/2,0,0),verts=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=depth,location=loc,rotation=rot)
    o=finish(bpy.context.object,name,m,col,.008)
    return o
CZ=3.95
def arc(name,r0,r1,a0,a1,y0,y1,m,col,segments=10,bevel=.012):
    vs=[]
    for y in [y0,y1]:
        for r in [r0,r1]:
            for i in range(segments+1):
                a=a0+(a1-a0)*i/segments
                vs.append((r*math.sin(a),y,CZ+r*math.cos(a)))
    n=segments+1;fs=[]
    for i in range(segments):
        fs += [(i,i+1,n+i+1,n+i),(2*n+i,3*n+i,3*n+i+1,2*n+i+1),
               (i,2*n+i,2*n+i+1,i+1),(n+i,n+i+1,3*n+i+1,3*n+i)]
    fs.extend([(0,n,3*n,2*n),(n-1,3*n-1,4*n-1,2*n-1)])
    mesh=bpy.data.meshes.new(name+' geometry');mesh.from_pydata(vs,[],fs);mesh.update()
    o=bpy.data.objects.new(name,mesh);COL[col].objects.link(o);o.data.materials.append(m)
    if bevel:
        b=o.modifiers.new('Edge radius','BEVEL');b.width=bevel;b.segments=2
        o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o
def tube(name,points,radius,m,col):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=2
    cu.bevel_depth=radius;cu.bevel_resolution=3
    sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
    for p,co in zip(sp.points,points):p.co=(*co,1)
    o=bpy.data.objects.new(name,cu);COL[col].objects.link(o);o.data.materials.append(m)
    return o
def radialpos(r,a,y):return (r*math.sin(a),y,CZ+r*math.cos(a))
start=math.radians(12);end=math.radians(348)
# A buildable foundation and an unobstructed threshold.
box('Basalt load-bearing plinth',(0,.05,.47),(8.9,3.9,.94),black,'01_Foundation',.10)
box('Upper landing',(0,-.05,1.01),(7.75,3.55,.20),bronzes[1],'01_Foundation',.04)
box('Threshold walkway',(0,-.2,1.14),(3.1,4.0,.12),dark,'01_Foundation',.025)
for i in range(7):
    h=(i+1)*.16;y=-4.75+i*.49
    box('Approach stair %02d'%i,(0,y,h/2),(3.2,.54,h),black,'01_Foundation',.025)
    box('Stair bronze nosing %02d'%i,(0,y-.255,h-.018),(3.12,.038,.038),copper,'05_Service_details',.007)
    for x in [-1.33,1.33]:
        box('Step safety marker',(x,y-.10,h+.008),(.045,.22,.018),amber,'06_Amber_memory',.005)
for side in [-1,1]:
    box('Foundation shoulder',(side*3.15,-.10,.98),(1.45,3.7,.30),black,'01_Foundation',.05)
    box('Support armour',(side*3.27,-.06,1.70),(.95,1.6,1.36),bronzes[3],'03_Bronze_armour',.08)
    box('Service faceplate',(side*3.27,-.89,1.65),(.69,.12,.94),dark,'05_Service_details',.02)
    for j in range(9):
        box('Vent fin',(side*3.27,-.98,1.31+j*.073),(.50,.07,.025),copper,'05_Service_details',.005)
    for xoff in [-.28,.28]:
        for z in [1.27,2.03]:
            cyl('Hex service fastener',(side*3.27+xoff,-1.00,z),.046,.032,steel,'05_Service_details',verts=6)
    for j in range(6):
        box('Foundation seam',(side*(1.9+j*.36),-1.916,.5),(.012,.012,.56),copper,'05_Service_details',.003)
# Deep layered ring, with genuine aperture and an intentional top fracture.
arc('Primary basalt ring',2.60,3.69,start,end,-.35,.47,black,'02_Structural_ring',180,.028)
arc('Rear structural flange',2.63,3.82,start,end,.47,.67,bronzes[1],'02_Structural_ring',180,.02)
arc('Outer raised rim',3.60,3.77,start,end,-.57,-.36,copper,'02_Structural_ring',180,.013)
arc('Inner gasket',2.60,2.75,start,end,-.49,-.34,dark,'02_Structural_ring',180,.008)
arc('Inner machined ring',2.69,2.78,start,end,-.57,-.47,copper,'02_Structural_ring',180,.012)
# Armour consists of individually editable sectors with consistent machining.
for i in range(28):
    a0=start+(end-start)*i/28+.007;a1=start+(end-start)*(i+1)/28-.007
    arc('Bronze armour sector %02d'%i,3.16,3.57,a0,a1,-.65,-.36,bronzes[i%7],'03_Bronze_armour',8,.018)
    arc('Raised patina inlay %02d'%i,3.23,3.44,a0+.016,a1-.016,-.681,-.65,patina if i%3 else bronzes[2],'03_Bronze_armour',7,.009)
    a=(a0+a1)/2
    for r in [3.20,3.51]:
        cyl('Armour bolt %02d'%i,radialpos(r,a,-.70),.035,.03,steel,'05_Service_details',verts=6)
    if i%4==1:
        arc('Ceramic field repair %02d'%i,3.18,3.55,a0+.025,a1-.025,-.718,-.686,ivory,'03_Bronze_armour',5,.012)
# Thin concentric conductive paths with repeated mounting ribs.
for k in range(3):
    r=2.89+k*.073
    arc('Conductive track %02d'%k,r,r+.027,start+.012,end-.012,-.56,-.51,copper,'05_Service_details',180,.004)
    arc('Track shadow groove %02d'%k,r-.016,r-.006,start,end,-.512,-.50,dark,'05_Service_details',180,.002)
for i in range(84):
    a=start+(end-start)*(i+.5)/84
    o=box('Radial mounting rib %03d'%i,radialpos(3.03,a,-.61),(.037,.12,.27),bronzes[(i+2)%7],'05_Service_details',.007)
    o.rotation_euler[1]=a
# Alignment collar has an explicit single-axis motion, independent of the static shell.
root=bpy.data.objects.new('Alignment collar / animated 8 degree sweep',None)
COL['04_Alignment_mechanism'].objects.link(root);root.location=(0,0,CZ)
def parent_keep(o,parent):
    o.parent=parent;o.matrix_parent_inverse=parent.matrix_world.inverted()
bpy.context.view_layer.update()
collar=arc('Alignment collar',2.54,2.65,start+.02,end-.02,-.58,-.37,bronzes[5],'04_Alignment_mechanism',160,.012)
parent_keep(collar,root)
for i in range(64):
    a=start+.04+(end-start-.08)*(i+.5)/64
    o=box('Alignment tooth %03d'%i,radialpos(2.58,a,-.635),(.052,.15,.125),steel if i%8==0 else bronzes[2],'04_Alignment_mechanism',.007)
    o.rotation_euler[1]=a;parent_keep(o,root)
    if i%8==0:
        o=cyl('Calibration light',radialpos(2.66,a,-.7),.026,.025,cyan,'06_Amber_memory',verts=16);parent_keep(o,root)
for frame,ang in [(1,0),(60,math.radians(8)),(120,0)]:
    root.rotation_euler[1]=ang;root.keyframe_insert(data_path='rotation_euler',index=1,frame=frame)
scene.frame_set(1)
# Arched reinforcing struts around the cut ends; no floating broken debris.
for a in [start+.04,end-.04]:
    o=box('Fracture end clamp',radialpos(3.20,a,-.13),(.19,1.27,1.13),bronzes[4],'02_Structural_ring',.035);o.rotation_euler[1]=a
    for r in [2.86,3.53]:
        cyl('Fracture clamp bolt',radialpos(r,a,-.81),.060,.045,steel,'05_Service_details',verts=6)
# Side actuators and maintenance conduits make the gate's function tangible.
for side in [-1,1]:
    for z in [2.0,2.5,3.0]:
        x=side*3.48
        cyl('Actuator socket',(x,-.43,z),.18,.32,black,'05_Service_details')
        cyl('Actuator bronze cap',(x,-.62,z),.12,.10,copper,'05_Service_details')
    pts=[(side*3.72,.15,1.32),(side*4.05,.15,1.40),(side*4.12,.15,2.50),(side*3.62,.15,3.01)]
    tube('External service conduit',pts,.065,black,'05_Service_details')
    tube('Copper conduit companion',[(x+side*.12,y+.16,z) for x,y,z in pts],.034,copper,'05_Service_details')
# Amber core remains beneath walking height, in an open protective housing.
cyl('Memory core bezel',(0,-1.76,.64),.35,.22,copper,'06_Amber_memory',verts=64)
cyl('Core inner gasket',(0,-1.89,.64),.274,.10,dark,'06_Amber_memory',verts=48)
bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=24,radius=1,location=(0,-1.96,.64))
o=bpy.context.object;o.scale=(.22,.105,.25);finish(o,'Amber memory lens',amber,'06_Amber_memory')
for p in o.data.polygons:p.use_smooth=True
for i in range(8):
    a=i*math.tau/8
    cyl('Core bezel bolt',(.305*math.sin(a),-1.91,.64+.305*math.cos(a)),.025,.025,steel,'05_Service_details',verts=6)
for side in [-1,1]:
    tube('Core power rail',[(side*.36,-1.82,.64),(side*1.0,-1.82,.64),(side*1.42,-1.82,.91),(side*2.22,-1.0,1.05)],.027,copper,'06_Amber_memory')
# A small human-scale service terminal and handrail provide scale cues.
box('Service terminal pedestal',(-4.5,-1.65,.65),(.44,.44,1.3),black,'05_Service_details',.05)
o=box('Service terminal ceramic hood',(-4.5,-1.65,1.37),(.64,.46,.24),ivory,'05_Service_details',.04);o.rotation_euler[0]=math.radians(16)
box('Service terminal display',(-4.5,-1.90,1.42),(.45,.016,.13),dark,'05_Service_details',.007)
for i in range(3):
    box('Terminal status slot',(-4.64+i*.14,-1.913,1.42),(.075,.008,.025),amber if i==0 else cyan,'06_Amber_memory',.002)
for side in [-1,1]:
    tube('Approach handrail',[(side*1.73,-4.72,.96),(side*1.73,-1.63,2.08),(side*1.73,-.91,2.08)],.041,bronzes[4],'05_Service_details')
    for y,z in [(-4.65,.11),(-3.1,.60),(-1.7,1.09)]:
        tube('Handrail support',[(side*1.73,y,z),(side*1.73,y,z+.88)],.032,bronzes[2],'05_Service_details')
# Ground and lights are presentation only, separate from asset collections.
box('Presentation floor',(0,0,-.10),(30,30,.16),floor,'07_Presentation',.02)
def light(name,kind,loc,color,energy,radius,target):
    d=bpy.data.lights.new(name,kind);d.energy=energy;d.color=color;d.shadow_soft_size=radius
    o=bpy.data.objects.new(name,d);COL['07_Presentation'].objects.link(o);o.location=loc
    if kind=='SPOT':
        d.spot_size=math.radians(85);d.spot_blend=.65
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    return o
light('Warm overhead key','POINT',(-4,-6,10),(1,.79,.52),2700,3,(0,0,3))
light('Cool broad fill','POINT',(6,-3,6),(.53,.77,1),1600,4,(0,0,3))
light('Teal edge from rear','POINT',(-3,4,7),(.34,.80,.74),3000,2,(0,0,4))
light('Frontal readable fill','POINT',(0,-10,4),(1,.91,.76),700,3,(0,0,3))
light('Memory core local light','POINT',(0,-2.12,.65),(1,.27,.025),12,.12,(0,0,0))
camd=bpy.data.cameras.new('Asset review 54mm')
cam=bpy.data.objects.new('Delivery camera',camd);COL['07_Presentation'].objects.link(cam)
cam.location=(9.3,-18.8,10.3);target=Vector((0,-.3,3.3))
cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camd.lens=54;scene.camera=cam
scene['asset_id']='EXO_PROP_RELIQUARY_GATE_001'
scene['status']='DETAILED_ASSET_STUDY_NOT_ENGINE_VALIDATED'
scene['reference_job']='15883828-66c7-4280-b94d-bffcf17d533b'
scene['scale_note']='Metres; approx 7.8m ring height; 1.37m service terminal'
scene['animation_note']='Frame 1 rest, 60 alignment peak, 120 return; 24 fps'
bpy.context.view_layer.update()
target=artifacts.file(name='reliquary-gate-beauty.png',media_type='image/png')
scene.render.filepath=str(target.path)
bpy.ops.render.render(write_still=True)
target.publish()
result={'asset_id':scene['asset_id'],'objects':len(bpy.data.objects),'mesh_objects':sum(o.type=='MESH' for o in bpy.data.objects),'polygons_base':sum(len(o.data.polygons) for o in bpy.data.objects if o.type=='MESH'),'materials':len(bpy.data.materials),'collections':list(COL),'frames':[1,60,120],'status':'Detailed geometry and material study; visual and export review required'}

