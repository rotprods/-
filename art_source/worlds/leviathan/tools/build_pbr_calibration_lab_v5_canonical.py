"""EXOVANT 2950 — LEVIATHAN canonical portable PBR calibration lab v5.

Clean source-of-truth builder integrating lessons from rejected development revisions:
- v1 GENERATED textures did not persist pixel data through provider checkpoint.
- v2 Blender Image.save() encoded blank PNGs in this worker.
- v3 introduced direct deterministic RGBA8 PNG encoding + FILE pack persistence.
- v4 made roughness ranges quantization-safe for 8-bit decode.

This builder starts from an empty scene and directly creates the accepted durable structure.
It does not mutate the LEVIATHAN world master and does not claim final art approval.
"""

import bpy
import hashlib
import math
import os
import tempfile
import struct
import zlib
import binascii
import numpy as np
from mathutils import Vector

STAGE = "LEVIATHAN_PBR_CALIBRATION_LAB_V5_CANONICAL"
RES = 256

SWATCHES = [
    {"name":"LEV_CAL_TISSUE_WARM","family":"LEV-MAT-001","role":"load-bearing living host tissue","base":(0.37,0.055,0.050),"rough":(0.36,0.58),"metal":0.0,"height_strength":1.8,"pattern":"tissue"},
    {"name":"LEV_CAL_MUCOSA_WET","family":"LEV-MAT-001","role":"moist pressure/lumen surface","base":(0.24,0.025,0.040),"rough":(0.10,0.28),"metal":0.0,"height_strength":1.35,"pattern":"mucosa"},
    {"name":"LEV_CAL_CARTILAGE","family":"LEV-MAT-001","role":"fibrous structural biological frame","base":(0.58,0.48,0.36),"rough":(0.38,0.62),"metal":0.0,"height_strength":1.15,"pattern":"cartilage"},
    {"name":"HUM_CAL_IVORY_CERAMIC","family":"LEV-MAT-002","role":"replaceable human graft shell","base":(0.72,0.69,0.61),"rough":(0.20,0.34),"metal":0.0,"height_strength":0.55,"pattern":"ceramic"},
    {"name":"HUM_CAL_BRUSHED_METAL","family":"LEV-MAT-002","role":"human technical load frame","base":(0.34,0.36,0.38),"rough":(0.24,0.42),"metal":1.0,"height_strength":0.75,"pattern":"metal"},
    {"name":"HUM_CAL_SEAL_RUBBER","family":"LEV-MAT-002","role":"compression gasket / soft technical seal","base":(0.035,0.040,0.045),"rough":(0.56,0.78),"metal":0.0,"height_strength":0.70,"pattern":"rubber"},
]


def _clear_scene():
    for obj in list(bpy.data.objects): bpy.data.objects.remove(obj,do_unlink=True)
    for coll in list(bpy.data.collections): bpy.data.collections.remove(coll)
    for mat in list(bpy.data.materials): bpy.data.materials.remove(mat)
    for img in list(bpy.data.images):
        if img.name not in {"Render Result","Viewer Node"}: bpy.data.images.remove(img)


def _coll(name,parent=None):
    c=bpy.data.collections.new(name); (parent or bpy.context.scene.collection).children.link(c); return c


def _move(obj,c):
    for old in list(obj.users_collection): old.objects.unlink(obj)
    c.objects.link(obj); return obj


def _look_at(obj,target): obj.rotation_euler=(Vector(target)-obj.location).to_track_quat("-Z","Y").to_euler()


def _fields(spec):
    y,x=np.mgrid[0:RES,0:RES].astype(np.float32); u=x/RES; v=y/RES; t=np.float32(math.tau); p=spec["pattern"]
    if p=="tissue":
        a=.55+.23*np.sin(t*(u*2+.14*np.sin(v*t*2)))+.12*np.sin(t*(v*7-u*1.5)); b=.5+.5*np.sin(t*(u*31+v*23))*np.sin(t*(v*37-u*11)); h=.70*a+.30*b; cm=.84+.24*a
    elif p=="mucosa":
        a=.5+.5*np.sin(t*(v*5+.18*np.sin(u*t*3))); b=.5+.5*np.cos(t*(u*29))*np.cos(t*(v*31)); h=.78*a+.22*b; cm=.80+.25*a
    elif p=="cartilage":
        a=.5+.5*np.sin(t*(u*10+.09*np.sin(v*t*4))); b=.5+.5*np.sin(t*(v*3-u*1.2)); h=.76*a+.24*b; cm=.88+.18*a
    elif p=="ceramic":
        a=.5+.5*np.sin(t*(u*47+v*19))*np.sin(t*(u*13-v*43)); b=.5+.5*np.sin(t*(u+v*.7)); h=.30*a+.70*b; cm=.96+.06*a
    elif p=="metal":
        a=.5+.5*np.sin(t*(v*96+.05*np.sin(u*t*2))); b=.5+.5*np.sin(t*(u*2)); h=.86*a+.14*b; cm=.88+.18*a
    else:
        a=.5+.5*np.sin(t*(u*41+v*17))*np.cos(t*(v*37-u*7)); b=.5+.5*np.sin(t*(u*3+v*2)); h=.70*a+.30*b; cm=.88+.16*a
    return np.clip(h,0,1).astype(np.float32),np.clip(cm,0,1.2).astype(np.float32)


def _arrays(spec):
    h,cm=_fields(spec)
    base=np.zeros((RES,RES,4),np.float32)
    for i,v in enumerate(spec["base"]): base[:,:,i]=np.clip(v*cm,0,1)
    base[:,:,3]=1
    lo,hi=spec["rough"]
    qlo=math.ceil(lo*255.0)/255.0; qhi=math.floor(hi*255.0)/255.0
    rough=np.clip(lo+(hi-lo)*(.25+.75*h),qlo,qhi)
    mr=np.zeros_like(base); mr[:,:,0]=1; mr[:,:,1]=rough; mr[:,:,2]=spec["metal"]; mr[:,:,3]=1
    gy,gx=np.gradient(h); nx=-gx*np.float32(spec["height_strength"]); ny=-gy*np.float32(spec["height_strength"]); nz=np.ones_like(h); mag=np.sqrt(nx*nx+ny*ny+nz*nz); nx/=mag; ny/=mag; nz/=mag
    normal=np.zeros_like(base); normal[:,:,0]=nx*.5+.5; normal[:,:,1]=ny*.5+.5; normal[:,:,2]=nz*.5+.5; normal[:,:,3]=1
    return base,mr,normal,qlo,qhi


def _rgba8(a): return np.clip(np.rint(a*255),0,255).astype(np.uint8)
def _chunk(k,d): return struct.pack(">I",len(d))+k+d+struct.pack(">I",binascii.crc32(k+d)&0xffffffff)

def _png(q):
    h,w,_=q.shape; rows=np.flipud(q).copy(); raw=b"".join(b"\x00"+rows[y].tobytes(order="C") for y in range(h))
    return b"\x89PNG\r\n\x1a\n"+_chunk(b"IHDR",struct.pack(">IIBBBBB",w,h,8,6,0,0,0))+_chunk(b"IDAT",zlib.compress(raw,9))+_chunk(b"IEND",b"")


def _image(name,arr,non_color):
    q=_rgba8(arr); src_sha=hashlib.sha256(q.tobytes(order="C")).hexdigest(); data=_png(q); png_sha=hashlib.sha256(data).hexdigest()
    fd,path=tempfile.mkstemp(prefix="lev_pbr_v5_",suffix=".png"); os.close(fd)
    try:
        with open(path,"wb") as f: f.write(data)
        img=bpy.data.images.load(path,check_existing=False); img.name=name
        try: img.colorspace_settings.name="Non-Color" if non_color else "sRGB"
        except Exception: pass
        _=img.pixels[0]; img.pack()
        if not img.packed_file: raise RuntimeError("packed_file missing for "+name)
        if hashlib.sha256(bytes(img.packed_file.data)).hexdigest()!=png_sha: raise RuntimeError("packed PNG digest mismatch for "+name)
        img["generator_stage"]=STAGE; img["resolution"]=RES; img["source_u8_rgba_sha256"]=src_sha; img["packed_png_sha256"]=png_sha; img.filepath_raw=""
        return img,src_sha,png_sha
    finally:
        if os.path.exists(path): os.remove(path)


def _material(spec,base,mr,normal,qlo,qhi):
    m=bpy.data.materials.new(spec["name"]); m.use_nodes=True; nt=m.node_tree; nt.nodes.clear()
    out=nt.nodes.new("ShaderNodeOutputMaterial"); bs=nt.nodes.new("ShaderNodeBsdfPrincipled"); uv=nt.nodes.new("ShaderNodeUVMap"); uv.uv_map="UVMap"; uv.label="UVMap"
    tb=nt.nodes.new("ShaderNodeTexImage"); tb.image=base; tb.interpolation="Linear"; tb.extension="REPEAT"; tb.label="BASECOLOR"
    tm=nt.nodes.new("ShaderNodeTexImage"); tm.image=mr; tm.interpolation="Linear"; tm.extension="REPEAT"; tm.label="MR"
    sep=nt.nodes.new("ShaderNodeSeparateColor"); sep.mode="RGB"; sep.label="MR_CHANNELS"
    tn=nt.nodes.new("ShaderNodeTexImage"); tn.image=normal; tn.interpolation="Linear"; tn.extension="REPEAT"; tn.label="NORMAL"
    nm=nt.nodes.new("ShaderNodeNormalMap"); nm.space="TANGENT"; nm.inputs["Strength"].default_value=1
    for tex in (tb,tm,tn): nt.links.new(uv.outputs["UV"],tex.inputs["Vector"])
    nt.links.new(tb.outputs["Color"],bs.inputs["Base Color"]); nt.links.new(tm.outputs["Color"],sep.inputs["Color"]); nt.links.new(sep.outputs["Green"],bs.inputs["Roughness"]); nt.links.new(sep.outputs["Blue"],bs.inputs["Metallic"]); nt.links.new(tn.outputs["Color"],nm.inputs["Color"]); nt.links.new(nm.outputs["Normal"],bs.inputs["Normal"]); nt.links.new(bs.outputs["BSDF"],out.inputs["Surface"])
    bs.inputs["IOR"].default_value=1.46 if spec["metal"]==0 else 1.5
    m["asset_family"]=spec["family"]; m["physical_role"]=spec["role"]; m["roughness_intent_min"]=spec["rough"][0]; m["roughness_intent_max"]=spec["rough"][1]; m["roughness_quantized_min"]=qlo; m["roughness_quantized_max"]=qhi; m["metallic_intent"]=spec["metal"]; m["generator_stage"]=STAGE; m["production_state"]="CALIBRATION_PROTOTYPE_NOT_FINAL"
    return m


def _neutral(name,color,rough):
    m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get("Principled BSDF");bs.inputs["Base Color"].default_value=(*color,1);bs.inputs["Roughness"].default_value=rough;return m


def build():
    _clear_scene(); scene=bpy.context.scene; scene.unit_settings.system="METRIC"; scene.unit_settings.scale_length=1; scene.render.engine="BLENDER_EEVEE"; scene.render.fps=24; scene.render.resolution_x=960; scene.render.resolution_y=540; scene.render.resolution_percentage=100
    scene.world=bpy.data.worlds.new("LEVIATHAN_CAL_WORLD"); scene.world.use_nodes=True; bg=scene.world.node_tree.nodes.get("Background"); bg.inputs["Color"].default_value=(.015,.018,.022,1); bg.inputs["Strength"].default_value=.18
    root=_coll("LEV_PBR_CAL_LAB");host=_coll("10_HOST_SWATCHES",root);human=_coll("20_HUMAN_GRAFT_SWATCHES",root);refs=_coll("80_REFERENCE",root);lights=_coll("90_CAMERAS_LIGHTS",root)
    floor_mat=_neutral("CAL_NEUTRAL_FLOOR",(.055,.060,.068),.82);ref_mat=_neutral("CAL_HUMAN_REF",(.42,.46,.50),.56)
    bpy.ops.mesh.primitive_cube_add(location=(0,0,-.12));floor=bpy.context.object;floor.name="CAL_FLOOR";floor.dimensions=(14,8,.24);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);floor.data.materials.append(floor_mat);_move(floor,refs)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.24,depth=1.45,location=(-6.1,2.6,.725));body=bpy.context.object;body.name="CAL_REF_HUMAN_BODY_1P85M";body.data.materials.append(ref_mat);_move(body,refs)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=.22,location=(-6.1,2.6,1.63));head=bpy.context.object;head.name="CAL_REF_HUMAN_HEAD";head.data.materials.append(ref_mat);_move(head,refs)
    rr=bpy.data.objects.new("CAL_REF_HUMAN_1P85M",None);refs.objects.link(rr);rr["reference_height_m"]=1.85
    xs=[-4.3,0,4.3];ys=[1.8,-1.7];receipts=[]
    for idx,spec in enumerate(SWATCHES):
        b,mr,n,qlo,qhi=_arrays(spec); bi,bsrc,bpng=_image(spec["name"]+"_BASECOLOR",b,False);mi,msrc,mpng=_image(spec["name"]+"_MR",mr,True);ni,nsrc,npng=_image(spec["name"]+"_NORMAL",n,True);mat=_material(spec,bi,mi,ni,qlo,qhi);c=host if spec["family"]=="LEV-MAT-001" else human;loc=(xs[idx%3],ys[idx//3],.9)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,radius=.82,location=loc);s=bpy.context.object;s.name=spec["name"]+"_SPHERE";s.data.materials.append(mat);_move(s,c);s["asset_family"]=spec["family"];s["calibration_role"]=spec["role"]
        bpy.ops.mesh.primitive_cube_add(location=(loc[0],loc[1]+1.08,.72),rotation=(math.radians(62),0,0));cp=bpy.context.object;cp.name=spec["name"]+"_COUPON";cp.dimensions=(1.45,.08,1.45);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);cp.data.materials.append(mat);_move(cp,c);cp["asset_family"]=spec["family"];cp["calibration_role"]=spec["role"]
        bpy.ops.object.text_add(location=(loc[0]-.95,loc[1]-.95,.10),rotation=(math.radians(90),0,0));lab=bpy.context.object;lab.name=spec["name"]+"_LABEL";lab.data.body=spec["name"];lab.data.size=.22;lab.data.extrude=.004;lab.data.materials.append(ref_mat);_move(lab,refs)
        receipts.append({"name":spec["name"],"asset_family":spec["family"],"declared_roughness":list(spec["rough"]),"quantized_roughness":[qlo,qhi],"metallic":spec["metal"],"source_u8_sha256":[bsrc,msrc,nsrc],"packed_png_sha256":[bpng,mpng,npng]})
    sd=bpy.data.lights.new("CAL_KEY_SUN_DATA","SUN");sd.energy=2.2;sd.color=(1,.86,.72);sun=bpy.data.objects.new("CAL_KEY_SUN",sd);sun.rotation_euler=(math.radians(38),math.radians(-22),math.radians(-34));lights.objects.link(sun)
    pd=bpy.data.lights.new("CAL_COOL_FILL_DATA","POINT");pd.energy=850;pd.color=(.33,.52,1);pd.shadow_soft_size=2.6;p=bpy.data.objects.new("CAL_COOL_FILL",pd);p.location=(0,-2,5.6);lights.objects.link(p)
    gd=bpy.data.lights.new("CAL_GRAZE_SPOT_DATA","SPOT");gd.energy=1700;gd.color=(1,.34,.22);gd.spot_size=math.radians(75);gd.spot_blend=.55;g=bpy.data.objects.new("CAL_GRAZE_SPOT",gd);g.location=(-5.8,-4.8,2.3);_look_at(g,(0,0,.75));lights.objects.link(g)
    cd=bpy.data.cameras.new("CAM_CAL_OVERVIEW_DATA");cd.lens=48;cam=bpy.data.objects.new("CAM_CAL_OVERVIEW",cd);cam.location=(0,-12.8,6);_look_at(cam,(0,.3,.75));lights.objects.link(cam)
    c2d=bpy.data.cameras.new("CAM_CAL_GRAZE_DATA");c2d.lens=70;c2=bpy.data.objects.new("CAM_CAL_GRAZE",c2d);c2.location=(0,-6.3,1.45);_look_at(c2,(0,-1.1,.72));lights.objects.link(c2);scene.camera=cam
    scene["pbr_calibration_stage"]=STAGE;scene["texture_resolution"]=RES;scene["asset_families"]="LEV-MAT-001,LEV-MAT-002";scene["final_art_approved"]=False;scene["world_master_propagation_approved"]=False;scene["gltf_sampler_warning_classification"]="EXPECTED_SHARED_MR_TEXTURE_FOR_METALLIC_AND_ROUGHNESS_SOCKETS_SAME_SAMPLER"
    return {"stage":STAGE,"texture_resolution":RES,"swatches":receipts,"images":18,"packed_images":18,"unique_packed_pngs":18,"objects":len(scene.objects),"status":"CANONICAL_LAB_NOT_FINAL_ART"}

if __name__=="__main__": print(build())
