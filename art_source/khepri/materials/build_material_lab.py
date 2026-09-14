"""Exact-replay builder for KHEPRI X100 Material Lab R2.

Blender 5.2+. Calibration resolution is intentionally 128² and is NOT a runtime/final-art texture budget.
R1-authored states preserve their R1 kernels; only the eight R2 legibility targets use R2 kernels.
"""
from __future__ import annotations
import binascii, math, os, struct, tempfile, zlib
import bpy
from mathutils import Vector

CONTRACT="KHP_MATERIAL_PRODUCTION_X100_V1"; N=128; VALID_COMBINATIONS=139; LEGIBILITY="R2_CAUSAL_ENHANCEMENT"
FAMILIES={
"solar_glass":{"asset_id":"KHP_MAT_GLASS_SOLAR_001","base":(.34,.52,.56),"metal":0.,"rough":.16,"trans":.35,"finish":"cast_vitrified","states":["calibrated","service_worn","thermal_cycled","repair_laminated"]},
"mirror_optical":{"asset_id":"KHP_MAT_MIRROR_OPTICAL_001","base":(.62,.68,.70),"metal":.94,"rough":.075,"trans":0.,"finish":"broad_reflector","states":["calibrated","maintenance_cleaning","service_microabrasion","repair_recoated"]},
"bronze_synod":{"asset_id":"KHP_MAT_BRONZE_SYNOD_001","base":(.36,.17,.065),"metal":.82,"rough":.34,"trans":0.,"finish":"cast_structural","states":["service_clean","contact_polished","heat_affected_local","field_repaired"]},
"ceramic_scorched":{"asset_id":"KHP_MAT_CERAMIC_SCORCHED_001","base":(.31,.19,.13),"metal":0.,"rough":.60,"trans":0.,"finish":"pressed_tile","states":["intact","heat_cycled","stress_chipped","patch_replaced"]},
"fabric_shade":{"asset_id":"KHP_MAT_FABRIC_SHADE_001","base":(.27,.21,.145),"metal":0.,"rough":.84,"trans":0.,"finish":"woven_dense","states":["taut_service","handled_worn","solar_aged","stitched_repair"]},
"mineral_dark":{"asset_id":"KHP_MAT_MINERAL_DESERT_001","base":(.075,.068,.062),"metal":.04,"rough":.72,"trans":0.,"finish":"cut_plate","states":["cut_clean","foot_traffic_worn","thermal_fissure_proxy","mechanical_patch"]}}
CAUSE={
"calibrated":"base","intact":"base","taut_service":"base","cut_clean":"base",
"service_worn":"contact_use","service_microabrasion":"contact_use","contact_polished":"contact_use","handled_worn":"contact_use","foot_traffic_worn":"contact_use",
"maintenance_cleaning":"maintenance","service_clean":"maintenance",
"thermal_cycled":"thermal","heat_affected_local":"thermal","heat_cycled":"thermal","solar_aged":"thermal","thermal_fissure_proxy":"thermal",
"repair_laminated":"repair","repair_recoated":"repair","field_repaired":"repair","patch_replaced":"repair","stitched_repair":"repair","mechanical_patch":"repair",
"stress_chipped":"mechanical_stress"}
R2={('solar_glass','service_worn'),('solar_glass','thermal_cycled'),('solar_glass','repair_laminated'),('mirror_optical','maintenance_cleaning'),('mirror_optical','service_microabrasion'),('mirror_optical','repair_recoated'),('ceramic_scorched','heat_cycled'),('mineral_dark','thermal_fissure_proxy')}

def clamp(x,a=0.,b=1.): return a if x<a else b if x>b else x
def chunk(t,d): return struct.pack('>I',len(d))+t+d+struct.pack('>I',binascii.crc32(t+d)&0xffffffff)
def png(path,rgba):
 raw=b''.join(b'\x00'+rgba[y*N*4:(y+1)*N*4] for y in range(N));open(path,'wb').write(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',N,N,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b''))
def micro(f,u,v,r2=False):
 t=2*math.pi
 if f=='solar_glass': return ((.028 if r2 else .025)*math.sin(t*(3*u+.35*v)),(.020 if r2 else .018)*math.cos(t*2*v))
 if f=='mirror_optical': return ((.008 if r2 else .010)*math.sin(t*12*u),(.005 if r2 else .006)*math.cos(t*3*v))
 if f=='bronze_synod': return .040*math.sin(t*18*u),.012*math.sin(t*2*v)
 if f=='ceramic_scorched': return .030*math.sin(t*(4*u+2*v)),.028*math.cos(t*(3*v-u))
 if f=='fabric_shade': return .060*math.sin(t*24*u),.060*math.sin(t*24*v)
 return .035*math.sin(t*(5*u+1.7*v)),.035*math.cos(t*(4*v-1.2*u))
def mask_r1(state,u,v):
 c=CAUSE[state]
 if c=='contact_use': return clamp(1-abs(v-.28)/.24)*clamp(1-abs(u-.55)/.58)
 if c=='maintenance': return clamp(1-abs((u-v)-.05)/.20)
 if c=='thermal': return clamp((u-.12)/.88)**1.45
 if c=='repair': return 1. if .58<u<.84 and .25<v<.75 else 0.
 if c=='mechanical_stress': return clamp(1-abs(v-(.82-.66*u+.035*math.sin(u*18)))/.025)
 return 0.
def mask_r2(state,u,v):
 c=CAUSE[state]
 if c=='contact_use': return clamp(1-abs(v-.31)/.25)*clamp(1-abs(u-.52)/.54)
 if c=='maintenance': return clamp(1-abs((u-v)-.04)/.16)
 if c=='thermal': return clamp((u-.05)/.95)**1.25
 if c=='repair': return 1. if .54<u<.86 and .16<v<.84 else 0.
 if c=='mechanical_stress': return clamp(1-abs(v-(.82-.66*u+.035*math.sin(u*18)))/.025)
 return 0.
def fissure(u,v):
 m=clamp(1-abs(v-(.80-.62*u+.030*math.sin(u*20)))/.018)
 if u>.56:m=max(m,clamp(1-abs(v-(.47+.34*(u-.56)+.020*math.sin(u*17)))/.014))
 if u>.72:m=max(m,clamp(1-abs(v-(.58-.42*(u-.72)))/.012))
 return m

def maps(f,state,spec):
 enhanced=(f,state) in R2;bc=bytearray();mr=bytearray();nm=bytearray();sm=bytearray();cause=CAUSE[state]
 for y in range(N):
  v=y/(N-1)
  for x in range(N):
   u=x/(N-1);m=(mask_r2 if enhanced else mask_r1)(state,u,v);r,g,b=spec['base'];rough=spec['rough'];met=spec['metal'];nx,ny=micro(f,u,v,enhanced);stress=0.
   if enhanced:
    if state=='service_worn': rough+=.23*m;r=r*(1-.10*m)+.16*m;g=g*(1-.08*m)+.18*m;b=b*(1-.06*m)+.20*m;ny+=.11*m*math.sin(u*math.pi*48)
    elif state=='thermal_cycled': rough+=.20*m;r*=1+.28*m;g*=1-.24*m;b*=1-.38*m;nx+=.06*m*math.sin(v*math.pi*10)
    elif state=='repair_laminated':
     rough-=.08*m;r=r*(1-.26*m)+.10*m;g=g*(1-.22*m)+.20*m;b=b*(1-.18*m)+.24*m
     if m and (abs(u-.54)<.018 or abs(u-.86)<.018 or abs(v-.16)<.018 or abs(v-.84)<.018):nx+=.22
    elif state=='maintenance_cleaning': rough=.18*(1-m)+.035*m;r*=.88+.18*m;g*=.88+.18*m;b*=.88+.18*m
    elif state=='service_microabrasion': rough+=.28*m;r*=1-.10*m;g*=1-.09*m;b*=1-.08*m;ny+=.16*m*math.sin(u*math.pi*68)
    elif state=='repair_recoated':
     rough=.13*(1-m)+.025*m;r=r*(1-.18*m)+.72*m*.18;g=g*(1-.18*m)+.76*m*.18;b=b*(1-.18*m)+.78*m*.18
     if m and (abs(u-.54)<.018 or abs(u-.86)<.018):nx+=.18
    elif state=='heat_cycled': rough+=.18*m;r*=1+.20*m;g*=1-.25*m;b*=1-.40*m;ny+=.08*m*math.sin(v*math.pi*8)
    elif state=='thermal_fissure_proxy': stress=fissure(u,v);rough+=.10*m+.12*stress;r*=1-.58*stress;g*=1-.58*stress;b*=1-.58*stress;nx+=.20*stress;ny-=.16*stress
   else:
    manufacture=.025*(nx+ny)
    if cause=='contact_use':
     rough+=(-.16 if f in ('bronze_synod','mirror_optical') else .12)*m;r*=1+.08*m;g*=1+.065*m;b*=1+.045*m
    elif cause=='maintenance': rough-=.09*m;r*=1+.08*m;g*=1+.08*m;b*=1+.08*m
    elif cause=='thermal': rough+=.10*m;r*=1+.11*m;g*=1-.13*m;b*=1-.22*m
    elif cause=='repair':
     rough+=(.08 if f not in ('mirror_optical','bronze_synod') else -.04)*m;r=r*(1-.15*m)+.16*m;g=g*(1-.15*m)+.12*m;b=b*(1-.15*m)+.08*m
     if m and (abs(u-.58)<.015 or abs(u-.84)<.015):nx+=.20
    elif cause=='mechanical_stress': rough+=.18*m;r*=1-.55*m;g*=1-.55*m;b*=1-.55*m;ny+=.25*m;stress=m
    r*=1+manufacture;g*=1+manufacture;b*=1+manufacture
   r,g,b=clamp(r),clamp(g),clamp(b);rough=clamp(rough,.02,.97)
   bc+=bytes((round(r*255),round(g*255),round(b*255),255));mr+=bytes((255,round(rough*255),round(clamp(met)*255),255));nm+=bytes((round(clamp(.5+nx)*255),round(clamp(.5+ny)*255),255,255))
   use=m if cause in ('contact_use','maintenance') else 0.;thermal=m if cause=='thermal' else 0.;repair=m if cause=='repair' else 0.;sm+=bytes((round(use*255),round(thermal*255),round(repair*255),round(stress*255)))
 return {'BC':bytes(bc),'MR':bytes(mr),'N':bytes(nm),'SM':bytes(sm)}
def image(name,data,space,r2):
 path=os.path.join(tempfile.gettempdir(),name+'.png');png(path,data);im=bpy.data.images.load(path,check_existing=False);im.name=name;im.colorspace_settings.name=space;im.pack();im['contract']=CONTRACT;im['packed_source']='deterministic_png_r2' if r2 else 'deterministic_png';im['width']=N;im['height']=N
 try:os.remove(path)
 except OSError:pass
 im.filepath='';return im
def material(f,state,spec):
 r2=(f,state) in R2;stem=spec['asset_id']+'__'+state.upper();ims={k:image(stem+'__'+k,v,'sRGB' if k=='BC' else 'Non-Color',r2) for k,v in maps(f,state,spec).items()};m=bpy.data.materials.new(stem);m.use_nodes=True
 for k,v in {'family':f,'asset_id':spec['asset_id'],'state':state,'cause':CAUSE[state],'finish':spec['finish'],'contract':CONTRACT,'application_scale':'calibration'}.items():m[k]=v
 if r2:m['legibility_revision']=LEGIBILITY
 nt=m.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');bs=nt.nodes.new('ShaderNodeBsdfPrincipled');bs.name='KHP_PRINCIPLED';bs.inputs['IOR'].default_value=1.5;bs.inputs['Transmission Weight'].default_value=spec['trans'];uv=nt.nodes.new('ShaderNodeUVMap');uv.name='KHP_UV0';uv.uv_map='UVMap';tex={}
 for k in ('BC','MR','N','SM'):
  n=nt.nodes.new('ShaderNodeTexImage');n.name='KHP_TEX_'+k;n.image=ims[k];n.interpolation='Linear';n.extension='REPEAT';tex[k]=n;nt.links.new(uv.outputs['UV'],n.inputs['Vector'])
 sep=nt.nodes.new('ShaderNodeSeparateColor');sep.name='KHP_MR_SEPARATE';normal=nt.nodes.new('ShaderNodeNormalMap');normal.name='KHP_NORMALMAP';normal.space='TANGENT';normal.inputs['Strength'].default_value=.75
 nt.links.new(tex['BC'].outputs['Color'],bs.inputs['Base Color']);nt.links.new(tex['MR'].outputs['Color'],sep.inputs['Color']);nt.links.new(sep.outputs['Green'],bs.inputs['Roughness']);nt.links.new(sep.outputs['Blue'],bs.inputs['Metallic']);nt.links.new(tex['N'].outputs['Color'],normal.inputs['Color']);nt.links.new(normal.outputs['Normal'],bs.inputs['Normal']);nt.links.new(bs.outputs['BSDF'],out.inputs['Surface']);tex['SM'].label='Source-only causal state mask: R use/maintenance, G thermal, B repair, A stress';return m
def move(obj,coll):
 for c in list(obj.users_collection):c.objects.unlink(obj)
 coll.objects.link(obj)
def look(obj,p):obj.rotation_euler=(Vector(p)-obj.location).to_track_quat('-Z','Y').to_euler()
def build():
 for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
 for ds in (bpy.data.materials,bpy.data.images,bpy.data.meshes,bpy.data.curves):
  for d in list(ds):ds.remove(d)
 s=bpy.context.scene;s.name='KHEPRI_X100_MATERIAL_LAB';s.render.engine='BLENDER_EEVEE';s.render.resolution_x=960;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.world=bpy.data.worlds.get('World') or bpy.data.worlds.new('World');s.world.color=(.018,.018,.016);s['material_contract']=CONTRACT;s['valid_combinations']=139;s['calibration_texture_resolution']=N;s['material_legibility_revision']=LEGIBILITY
 root=bpy.data.collections.new('KHP_MATLAB_ROOT');s.collection.children.link(root);samples=bpy.data.collections.new('KHP_MATLAB_SAMPLES');labels=bpy.data.collections.new('KHP_MATLAB_LABELS');lights=bpy.data.collections.new('KHP_MATLAB_LIGHTS');root.children.link(samples);root.children.link(labels);root.children.link(lights);meta=bpy.data.objects.new('KHP_MATLAB_META',None);root.objects.link(meta);meta['contract']=CONTRACT;meta['claim_id']='CLM-KHEPRI-MATERIALS-001';meta['valid_combinations']=139;meta['calibration_cells']=24;meta['texture_resolution']=N
 lm=bpy.data.materials.new('KHP_MATLAB_LABEL');lm.use_nodes=True;lbs=lm.node_tree.nodes.get('Principled BSDF');lbs.inputs['Base Color'].default_value=(.72,.70,.62,1);lbs.inputs['Roughness'].default_value=.72
 def label(body,loc,size=.26,align='CENTER'):
  cu=bpy.data.curves.new('TXT_'+body[:20],'FONT');cu.body=body;cu.align_x=align;cu.size=size;cu.extrude=.008;o=bpy.data.objects.new('LBL_'+body[:32],cu);labels.objects.link(o);o.location=loc;o.rotation_euler=(math.radians(90),0,0);cu.materials.append(lm)
 bpy.ops.mesh.primitive_cube_add(location=(0,.8,0),scale=(11.7,.12,11.1));wall=bpy.context.object;wall.name='KHP_MATLAB_BACKDROP';move(wall,root);wm=bpy.data.materials.new('KHP_MATLAB_BACKDROP_MAT');wm.use_nodes=True;w=wm.node_tree.nodes.get('Principled BSDF');w.inputs['Base Color'].default_value=(.035,.032,.028,1);w.inputs['Roughness'].default_value=.82;wall.data.materials.append(wm)
 xs=[-7.8,-2.6,2.6,7.8];zs=[8.6,5.15,1.70,-1.75,-5.20,-8.65]
 for row,(f,spec) in enumerate(FAMILIES.items()):
  label(f.replace('_',' ').upper(),(-10.9,-.35,zs[row]+.35),.30,'LEFT')
  for col,state in enumerate(spec['states']):
   m=material(f,state,spec);x,z=xs[col],zs[row];bpy.ops.mesh.primitive_cube_add(location=(x-.45,0,z+.25),scale=(1.45,.15,.95));p=bpy.context.object;p.name=f'KHP_SAMPLE_PANEL__{f.upper()}__{state.upper()}';move(p,samples);p.data.materials.append(m);p['asset_id']=spec['asset_id'];p['state']=state;p['cause']=CAUSE[state];bev=p.modifiers.new('KHP_BEVEL','BEVEL');bev.width=.08;bev.segments=2;bpy.context.view_layer.objects.active=p;p.select_set(True);bpy.ops.object.modifier_apply(modifier=bev.name);p.select_set(False)
   bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=.62,location=(x+1.25,-.28,z+.12));q=bpy.context.object;q.name=f'KHP_SAMPLE_CURVED__{f.upper()}__{state.upper()}';move(q,samples);q.data.materials.append(m);q['asset_id']=spec['asset_id'];q['state']=state;q['cause']=CAUSE[state]
   for poly in q.data.polygons:poly.use_smooth=True
   label(state.replace('_',' '),(x-.05,-.38,z-1.12),.20)
 camd=bpy.data.cameras.new('KHP_MATLAB_CAM');cam=bpy.data.objects.new('KHP_MATLAB_CAM',camd);lights.objects.link(cam);cam.location=(0,-44,0);camd.lens=55;camd.sensor_width=36;camd.clip_end=200;look(cam,(0,0,0));s.camera=cam
 sd=bpy.data.lights.new('KHP_MATLAB_SUN','SUN');sd.energy=3.;sd.angle=math.radians(6);sun=bpy.data.objects.new('KHP_MATLAB_SUN',sd);lights.objects.link(sun);sun.rotation_euler=(math.radians(38),0,math.radians(-32))
 kd=bpy.data.lights.new('KHP_MATLAB_KEY','POINT');kd.energy=1250;kd.color=(1.,.78,.58);key=bpy.data.objects.new('KHP_MATLAB_KEY',kd);lights.objects.link(key);key.location=(-11,-12,11)
 fd=bpy.data.lights.new('KHP_MATLAB_FILL','POINT');fd.energy=780;fd.color=(.58,.70,1.);fill=bpy.data.objects.new('KHP_MATLAB_FILL',fd);lights.objects.link(fill);fill.location=(11,-10,4)
 return {'contract':CONTRACT,'materials':24,'images':96,'objects':len(bpy.data.objects),'legibility_revision':LEGIBILITY}
if __name__=='__main__':print(build())
