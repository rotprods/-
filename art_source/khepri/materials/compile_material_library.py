"""Deterministic identity compiler for the KHEPRI X100 material library.

Creates only production identity: 24 contract materials, 96 packed deterministic PNG maps,
and 48 stable calibration meshes. Presentation (labels/lights/backdrop) is intentionally excluded.
Blender 5.2+, 1 BU = 1 m. Calibration maps are 128 px evidence, not final-resolution art.
"""
from __future__ import annotations
import binascii, math, os, struct, tempfile, zlib
import bpy

CONTRACT="KHP_MATERIAL_PRODUCTION_X100_V1"
RES=128
F={
"solar_glass":("KHP_MAT_GLASS_SOLAR_001",(0.34,0.52,0.56),0.0,0.16,0.35,"cast_vitrified",["calibrated","service_worn","thermal_cycled","repair_laminated"]),
"mirror_optical":("KHP_MAT_MIRROR_OPTICAL_001",(0.62,0.68,0.70),0.94,0.075,0.0,"broad_reflector",["calibrated","maintenance_cleaning","service_microabrasion","repair_recoated"]),
"bronze_synod":("KHP_MAT_BRONZE_SYNOD_001",(0.36,0.17,0.065),0.82,0.34,0.0,"cast_structural",["service_clean","contact_polished","heat_affected_local","field_repaired"]),
"ceramic_scorched":("KHP_MAT_CERAMIC_SCORCHED_001",(0.31,0.19,0.13),0.0,0.60,0.0,"pressed_tile",["intact","heat_cycled","stress_chipped","patch_replaced"]),
"fabric_shade":("KHP_MAT_FABRIC_SHADE_001",(0.27,0.21,0.145),0.0,0.84,0.0,"woven_dense",["taut_service","handled_worn","solar_aged","stitched_repair"]),
"mineral_dark":("KHP_MAT_MINERAL_DESERT_001",(0.075,0.068,0.062),0.04,0.72,0.0,"cut_plate",["cut_clean","foot_traffic_worn","thermal_fissure_proxy","mechanical_patch"]),
}
CAUSE={
"calibrated":"base","intact":"base","taut_service":"base","cut_clean":"base",
"service_worn":"contact_use","service_microabrasion":"contact_use","contact_polished":"contact_use","handled_worn":"contact_use","foot_traffic_worn":"contact_use",
"maintenance_cleaning":"maintenance","service_clean":"maintenance",
"thermal_cycled":"thermal","heat_affected_local":"thermal","heat_cycled":"thermal","solar_aged":"thermal","thermal_fissure_proxy":"thermal",
"repair_laminated":"repair","repair_recoated":"repair","field_repaired":"repair","patch_replaced":"repair","stitched_repair":"repair","mechanical_patch":"repair",
"stress_chipped":"mechanical_stress"}
R2={
("solar_glass","service_worn"),("solar_glass","thermal_cycled"),("solar_glass","repair_laminated"),
("mirror_optical","maintenance_cleaning"),("mirror_optical","service_microabrasion"),("mirror_optical","repair_recoated"),
("ceramic_scorched","heat_cycled"),("mineral_dark","thermal_fissure_proxy")}
def cl(x,a=0.0,b=1.0): return a if x<a else b if x>b else x
def chunk(k,d): return struct.pack(">I",len(d))+k+d+struct.pack(">I",binascii.crc32(k+d)&0xffffffff)
def png(path,rgba,n=RES):
 raw=b"".join(b"\x00"+rgba[y*n*4:(y+1)*n*4] for y in range(n))
 data=b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",n,n,8,6,0,0,0))+chunk(b"IDAT",zlib.compress(raw,9))+chunk(b"IEND",b"")
 open(path,"wb").write(data)
def micro(f,u,v,enh=False):
 t=2*math.pi
 if f=="solar_glass": return (0.028 if enh else 0.025)*math.sin(t*(3*u+.35*v)),(0.020 if enh else 0.018)*math.cos(t*2*v)
 if f=="mirror_optical": return (0.008 if enh else 0.010)*math.sin(t*12*u),(0.005 if enh else 0.006)*math.cos(t*3*v)
 if f=="bronze_synod": return .040*math.sin(t*18*u),.012*math.sin(t*2*v)
 if f=="ceramic_scorched": return .030*math.sin(t*(4*u+2*v)),.028*math.cos(t*(3*v-u))
 if f=="fabric_shade": return .060*math.sin(t*24*u),.060*math.sin(t*24*v)
 return .035*math.sin(t*(5*u+1.7*v)),.035*math.cos(t*(4*v-1.2*u))
def mask(s,u,v):
 c=CAUSE[s]
 if c=="contact_use": return cl(1-abs(v-.31)/.25)*cl(1-abs(u-.52)/.54)
 if c=="maintenance": return cl(1-abs((u-v)-.04)/.16)
 if c=="thermal": return cl((u-.05)/.95)**1.25
 if c=="repair": return 1.0 if .54<u<.86 and .16<v<.84 else 0.0
 if c=="mechanical_stress": return cl(1-abs(v-(.82-.66*u+.035*math.sin(u*18)))/.025)
 return 0.0
def fiss(u,v):
 z=cl(1-abs(v-(.80-.62*u+.030*math.sin(u*20)))/.018)
 if u>.56:z=max(z,cl(1-abs(v-(.47+.34*(u-.56)+.020*math.sin(u*17)))/.014))
 if u>.72:z=max(z,cl(1-abs(v-(.58-.42*(u-.72)))/.012))
 return z
def maps(f,s,base,metal,rough):
 BC=bytearray();MR=bytearray();N=bytearray();SM=bytearray();enh=(f,s) in R2
 for y in range(RES):
  v=y/(RES-1)
  for x in range(RES):
   u=x/(RES-1); c=CAUSE[s]; m=mask(s,u,v); r,g,b=base; ro=rough; nx,ny=micro(f,u,v,enh); stress=0.0
   if enh:
    if s=="service_worn": ro+=.23*m;r=r*(1-.10*m)+.16*m;g=g*(1-.08*m)+.18*m;b=b*(1-.06*m)+.20*m;ny+=.11*m*math.sin(u*math.pi*48)
    elif s=="thermal_cycled": ro+=.20*m;r*=1+.28*m;g*=1-.24*m;b*=1-.38*m;nx+=.06*m*math.sin(v*math.pi*10)
    elif s=="repair_laminated":
     ro-=.08*m;r=r*(1-.26*m)+.10*m;g=g*(1-.22*m)+.20*m;b=b*(1-.18*m)+.24*m
     if m and (abs(u-.54)<.018 or abs(u-.86)<.018 or abs(v-.16)<.018 or abs(v-.84)<.018):nx+=.22
    elif s=="maintenance_cleaning": ro=.18*(1-m)+.035*m;r*=.88+.18*m;g*=.88+.18*m;b*=.88+.18*m
    elif s=="service_microabrasion": ro+=.28*m;r*=1-.10*m;g*=1-.09*m;b*=1-.08*m;ny+=.16*m*math.sin(u*math.pi*68)
    elif s=="repair_recoated":
     ro=.13*(1-m)+.025*m;r=r*(1-.18*m)+.72*m*.18;g=g*(1-.18*m)+.76*m*.18;b=b*(1-.18*m)+.78*m*.18
     if m and (abs(u-.54)<.018 or abs(u-.86)<.018):nx+=.18
    elif s=="heat_cycled": ro+=.18*m;r*=1+.20*m;g*=1-.25*m;b*=1-.40*m;ny+=.08*m*math.sin(v*math.pi*8)
    elif s=="thermal_fissure_proxy": stress=fiss(u,v);ro+=.10*m+.12*stress;r*=1-.58*stress;g*=1-.58*stress;b*=1-.58*stress;nx+=.20*stress;ny-=.16*stress
   else:
    q=.025*(nx+ny)
    if c=="contact_use": ro+=(-.16 if f in ("bronze_synod","mirror_optical") else .12)*m;r*=1+.08*m;g*=1+.065*m;b*=1+.045*m
    elif c=="maintenance": ro-=.09*m;r*=1+.08*m;g*=1+.08*m;b*=1+.08*m
    elif c=="thermal": ro+=.10*m;r*=1+.11*m;g*=1-.13*m;b*=1-.22*m
    elif c=="repair":
     ro+=(.08 if f not in ("mirror_optical","bronze_synod") else -.04)*m;r=r*(1-.15*m)+.16*m;g=g*(1-.15*m)+.12*m;b=b*(1-.15*m)+.08*m
     if m and (abs(u-.54)<.018 or abs(u-.86)<.018):nx+=.20
    elif c=="mechanical_stress": ro+=.18*m;r*=1-.55*m;g*=1-.55*m;b*=1-.55*m;ny+=.25*m;stress=m
    r*=1+q;g*=1+q;b*=1+q
   r,g,b=cl(r),cl(g),cl(b);ro=cl(ro,.02,.97)
   BC+=bytes((round(r*255),round(g*255),round(b*255),255));MR+=bytes((255,round(ro*255),round(cl(metal)*255),255));N+=bytes((round(cl(.5+nx)*255),round(cl(.5+ny)*255),255,255))
   SM+=bytes((round((m if c in ("contact_use","maintenance") else 0)*255),round((m if c=="thermal" else 0)*255),round((m if c=="repair" else 0)*255),round(stress*255)))
 return {"BC":bytes(BC),"MR":bytes(MR),"N":bytes(N),"SM":bytes(SM)}
def image(name,data,cs,rev):
 p=os.path.join(tempfile.gettempdir(),name+".png");png(p,data);im=bpy.data.images.load(p,check_existing=False);im.name=name;im.colorspace_settings.name=cs;im.pack();im["contract"]=CONTRACT;im["packed_source"]="deterministic_png_r2" if rev else "deterministic_png";im["width"]=RES;im["height"]=RES
 try:os.remove(p)
 except OSError:pass
 im.filepath="";return im
def material(f,s,spec):
 aid,base,metal,rough,trans,finish,_=spec; rev=(f,s) in R2; mm=maps(f,s,base,metal,rough); stem=f"{aid}__{s.upper()}";ims={k:image(f"{stem}__{k}",v,"sRGB" if k=="BC" else "Non-Color",rev) for k,v in mm.items()}
 m=bpy.data.materials.new(stem);m.use_nodes=True
 for k,v in {"family":f,"asset_id":aid,"state":s,"cause":CAUSE[s],"finish":finish,"contract":CONTRACT,"application_scale":"calibration"}.items():m[k]=v
 if rev:m["legibility_revision"]="R2_CAUSAL_ENHANCEMENT"
 t=m.node_tree;t.nodes.clear();out=t.nodes.new("ShaderNodeOutputMaterial");bs=t.nodes.new("ShaderNodeBsdfPrincipled");bs.name="KHP_PRINCIPLED";bs.inputs["IOR"].default_value=1.5;bs.inputs["Transmission Weight"].default_value=trans;uv=t.nodes.new("ShaderNodeUVMap");uv.uv_map="UVMap";tex={}
 for k in ("BC","MR","N","SM"):
  n=t.nodes.new("ShaderNodeTexImage");n.name="KHP_TEX_"+k;n.image=ims[k];n.interpolation="Linear";n.extension="REPEAT";tex[k]=n;t.links.new(uv.outputs["UV"],n.inputs["Vector"])
 sep=t.nodes.new("ShaderNodeSeparateColor");norm=t.nodes.new("ShaderNodeNormalMap");norm.space="TANGENT";norm.inputs["Strength"].default_value=.75;t.links.new(tex["BC"].outputs["Color"],bs.inputs["Base Color"]);t.links.new(tex["MR"].outputs["Color"],sep.inputs["Color"]);t.links.new(sep.outputs["Green"],bs.inputs["Roughness"]);t.links.new(sep.outputs["Blue"],bs.inputs["Metallic"]);t.links.new(tex["N"].outputs["Color"],norm.inputs["Color"]);t.links.new(norm.outputs["Normal"],bs.inputs["Normal"]);t.links.new(bs.outputs["BSDF"],out.inputs["Surface"]);tex["SM"].label="Source-only causal state mask"
 return m
def clean():
 for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
 for db in (bpy.data.materials,bpy.data.images,bpy.data.meshes,bpy.data.curves):
  for x in list(db):db.remove(x)
def build():
 clean();scene=bpy.context.scene;scene["material_contract"]=CONTRACT;scene["valid_combinations"]=139;scene["calibration_texture_resolution"]=RES;scene["material_legibility_revision"]="R2_CAUSAL_ENHANCEMENT"
 coll=bpy.data.collections.new("KHP_MATLIB_IDENTITY");scene.collection.children.link(coll);xs=[-7.8,-2.6,2.6,7.8];zs=[8.6,5.15,1.70,-1.75,-5.20,-8.65];count=0
 for row,(f,spec) in enumerate(F.items()):
  for col,s in enumerate(spec[-1]):
   mat=material(f,s,spec);x,z=xs[col],zs[row]
   bpy.ops.mesh.primitive_cube_add(location=(x-.45,0,z+.25),scale=(1.45,.15,.95));p=bpy.context.object;p.name=f"KHP_SAMPLE_PANEL__{f.upper()}__{s.upper()}";p.data.materials.append(mat);p["asset_id"]=spec[0];p["state"]=s;p["cause"]=CAUSE[s]
   for c in list(p.users_collection):c.objects.unlink(p)
   coll.objects.link(p);bev=p.modifiers.new("KHP_BEVEL","BEVEL");bev.width=.08;bev.segments=2;bpy.context.view_layer.objects.active=p;p.select_set(True);bpy.ops.object.modifier_apply(modifier=bev.name);p.select_set(False)
   bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=.62,location=(x+1.25,-.28,z+.12));q=bpy.context.object;q.name=f"KHP_SAMPLE_CURVED__{f.upper()}__{s.upper()}";q.data.materials.append(mat);q["asset_id"]=spec[0];q["state"]=s;q["cause"]=CAUSE[s]
   for c in list(q.users_collection):c.objects.unlink(q)
   coll.objects.link(q)
   for poly in q.data.polygons:poly.use_smooth=True
   count+=1
 meta=bpy.data.objects.new("KHP_MATLIB_META",None);coll.objects.link(meta);meta["contract"]=CONTRACT;meta["claim_id"]="CLM-KHEPRI-MATERIALS-001";meta["valid_combinations"]=139;meta["calibration_cells"]=24;meta["texture_resolution"]=RES
 return {"contract":CONTRACT,"materials":count,"images":sum(i.get("contract")==CONTRACT for i in bpy.data.images),"samples":sum(o.name.startswith("KHP_SAMPLE_") for o in bpy.data.objects)}
if __name__=="__main__":print(build())
