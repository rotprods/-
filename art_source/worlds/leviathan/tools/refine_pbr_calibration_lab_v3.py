"""LEVIATHAN PBR calibration lab v3 — durable deterministic PNG correction.

v1 GENERATED images did not survive the provider checkpoint with pixel data.
v2 FILE+pack persisted, but Blender Image.save() encoded black blank buffers in this worker.
v3 removes Blender from PNG encoding: RGBA8 bytes are encoded directly with PNG filter-0 rows,
zlib and CRC-correct chunks, then loaded, packed and detached from the temporary backing file.

Geometry remains unchanged. Existing material families only: LEV-MAT-001 / LEV-MAT-002.
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

STAGE = "LEVIATHAN_PBR_CALIBRATION_LAB_V3_DURABLE_PNG"
RES = 256

SWATCHES = [
    {"name":"LEV_CAL_TISSUE_WARM","family":"LEV-MAT-001","role":"load-bearing living host tissue","base":(0.37,0.055,0.050),"rough":(0.36,0.58),"metal":0.0,"height_strength":1.8,"pattern":"tissue"},
    {"name":"LEV_CAL_MUCOSA_WET","family":"LEV-MAT-001","role":"moist pressure/lumen surface","base":(0.24,0.025,0.040),"rough":(0.10,0.28),"metal":0.0,"height_strength":1.35,"pattern":"mucosa"},
    {"name":"LEV_CAL_CARTILAGE","family":"LEV-MAT-001","role":"fibrous structural biological frame","base":(0.58,0.48,0.36),"rough":(0.38,0.62),"metal":0.0,"height_strength":1.15,"pattern":"cartilage"},
    {"name":"HUM_CAL_IVORY_CERAMIC","family":"LEV-MAT-002","role":"replaceable human graft shell","base":(0.72,0.69,0.61),"rough":(0.20,0.34),"metal":0.0,"height_strength":0.55,"pattern":"ceramic"},
    {"name":"HUM_CAL_BRUSHED_METAL","family":"LEV-MAT-002","role":"human technical load frame","base":(0.34,0.36,0.38),"rough":(0.24,0.42),"metal":1.0,"height_strength":0.75,"pattern":"metal"},
    {"name":"HUM_CAL_SEAL_RUBBER","family":"LEV-MAT-002","role":"compression gasket / soft technical seal","base":(0.035,0.040,0.045),"rough":(0.56,0.78),"metal":0.0,"height_strength":0.70,"pattern":"rubber"},
]


def _pattern(spec):
    y,x=np.mgrid[0:RES,0:RES].astype(np.float32); u=x/RES; v=y/RES; tau=np.float32(math.tau); p=spec["pattern"]
    if p=="tissue":
        macro=0.55+0.23*np.sin(tau*(u*2.0+0.14*np.sin(v*tau*2.0)))+0.12*np.sin(tau*(v*7.0-u*1.5)); micro=0.5+0.5*np.sin(tau*(u*31.0+v*23.0))*np.sin(tau*(v*37.0-u*11.0)); height=0.70*macro+0.30*micro; color_mod=0.84+0.24*macro
    elif p=="mucosa":
        ridges=0.5+0.5*np.sin(tau*(v*5.0+0.18*np.sin(u*tau*3.0))); pores=0.5+0.5*np.cos(tau*(u*29.0))*np.cos(tau*(v*31.0)); height=0.78*ridges+0.22*pores; color_mod=0.80+0.25*ridges
    elif p=="cartilage":
        fibers=0.5+0.5*np.sin(tau*(u*10.0+0.09*np.sin(v*tau*4.0))); cross=0.5+0.5*np.sin(tau*(v*3.0-u*1.2)); height=0.76*fibers+0.24*cross; color_mod=0.88+0.18*fibers
    elif p=="ceramic":
        speck=0.5+0.5*np.sin(tau*(u*47.0+v*19.0))*np.sin(tau*(u*13.0-v*43.0)); broad=0.5+0.5*np.sin(tau*(u*1.0+v*0.7)); height=0.30*speck+0.70*broad; color_mod=0.96+0.06*speck
    elif p=="metal":
        brush=0.5+0.5*np.sin(tau*(v*96.0+0.05*np.sin(u*tau*2.0))); broad=0.5+0.5*np.sin(tau*(u*2.0)); height=0.86*brush+0.14*broad; color_mod=0.88+0.18*brush
    elif p=="rubber":
        stipple=0.5+0.5*np.sin(tau*(u*41.0+v*17.0))*np.cos(tau*(v*37.0-u*7.0)); wave=0.5+0.5*np.sin(tau*(u*3.0+v*2.0)); height=0.70*stipple+0.30*wave; color_mod=0.88+0.16*stipple
    else:
        height=np.zeros((RES,RES),dtype=np.float32)+0.5; color_mod=np.ones((RES,RES),dtype=np.float32)
    return np.clip(height,0,1).astype(np.float32),np.clip(color_mod,0,1.2).astype(np.float32)


def _arrays(spec):
    height,color_mod=_pattern(spec)
    base=np.zeros((RES,RES,4),dtype=np.float32)
    for i,c in enumerate(spec["base"]): base[:,:,i]=np.clip(c*color_mod,0,1)
    base[:,:,3]=1.0
    rmin,rmax=spec["rough"]; rough=rmin+(rmax-rmin)*(0.25+0.75*height)
    mr=np.zeros((RES,RES,4),dtype=np.float32); mr[:,:,0]=1.0; mr[:,:,1]=np.clip(rough,0,1); mr[:,:,2]=spec["metal"]; mr[:,:,3]=1.0
    gy,gx=np.gradient(height); strength=np.float32(spec["height_strength"]); nx=-gx*strength; ny=-gy*strength; nz=np.ones_like(height); mag=np.sqrt(nx*nx+ny*ny+nz*nz); nx/=mag; ny/=mag; nz/=mag
    normal=np.zeros((RES,RES,4),dtype=np.float32); normal[:,:,0]=nx*0.5+0.5; normal[:,:,1]=ny*0.5+0.5; normal[:,:,2]=nz*0.5+0.5; normal[:,:,3]=1.0
    return base,mr,normal


def _to_rgba8(arr):
    return np.clip(np.rint(arr*255.0),0,255).astype(np.uint8)


def _chunk(kind,data):
    return struct.pack(">I",len(data))+kind+data+struct.pack(">I",binascii.crc32(kind+data)&0xffffffff)


def _encode_png_rgba8(rgba):
    if rgba.dtype != np.uint8 or rgba.ndim != 3 or rgba.shape[2] != 4:
        raise RuntimeError("RGBA8 encoder received invalid array")
    h,w,_=rgba.shape
    # PNG rows are top->bottom while Blender image pixel buffers are bottom->top.
    encoded_rows=np.flipud(rgba).copy()
    raw=b"".join(b"\x00"+encoded_rows[y].tobytes(order="C") for y in range(h))
    return (b"\x89PNG\r\n\x1a\n"+
            _chunk(b"IHDR",struct.pack(">IIBBBBB",w,h,8,6,0,0,0))+
            _chunk(b"IDAT",zlib.compress(raw,9))+
            _chunk(b"IEND",b""))


def _packed_png_image(final_name, arr, non_color):
    rgba=_to_rgba8(arr)
    source_sha=hashlib.sha256(rgba.tobytes(order="C")).hexdigest()
    png=_encode_png_rgba8(rgba)
    png_sha=hashlib.sha256(png).hexdigest()
    fd,path=tempfile.mkstemp(prefix="lev_pbr_v3_",suffix=".png"); os.close(fd)
    try:
        with open(path,"wb") as f: f.write(png)
        loaded=bpy.data.images.load(path,check_existing=False)
        loaded.name=final_name
        try: loaded.colorspace_settings.name="Non-Color" if non_color else "sRGB"
        except Exception: pass
        _=loaded.pixels[0]
        loaded.pack()
        if not loaded.packed_file:
            raise RuntimeError("packed_file missing for "+final_name)
        packed_sha=hashlib.sha256(bytes(loaded.packed_file.data)).hexdigest()
        if packed_sha != png_sha:
            raise RuntimeError("packed PNG digest mismatch for "+final_name)
        loaded["generator_stage"]=STAGE
        loaded["resolution"]=RES
        loaded["source_u8_rgba_sha256"]=source_sha
        loaded["packed_png_sha256"]=png_sha
        loaded.filepath_raw=""
        return loaded, source_sha, png_sha
    finally:
        if os.path.exists(path): os.remove(path)


def _rewire(spec, base_img, mr_img, normal_img):
    m=bpy.data.materials.get(spec["name"])
    if m is None: raise RuntimeError("Missing calibration material "+spec["name"])
    nt=m.node_tree; nt.nodes.clear()
    out=nt.nodes.new("ShaderNodeOutputMaterial")
    bs=nt.nodes.new("ShaderNodeBsdfPrincipled")
    uv=nt.nodes.new("ShaderNodeUVMap"); uv.uv_map="UVMap"; uv.label="UVMap"
    tbase=nt.nodes.new("ShaderNodeTexImage"); tbase.image=base_img; tbase.interpolation="Linear"; tbase.extension="REPEAT"; tbase.label="BASECOLOR"
    tmr=nt.nodes.new("ShaderNodeTexImage"); tmr.image=mr_img; tmr.interpolation="Linear"; tmr.extension="REPEAT"; tmr.label="MR"
    sep=nt.nodes.new("ShaderNodeSeparateColor"); sep.mode="RGB"; sep.label="MR_CHANNELS"
    tn=nt.nodes.new("ShaderNodeTexImage"); tn.image=normal_img; tn.interpolation="Linear"; tn.extension="REPEAT"; tn.label="NORMAL"
    nmap=nt.nodes.new("ShaderNodeNormalMap"); nmap.space="TANGENT"; nmap.inputs["Strength"].default_value=1.0
    for tex in (tbase,tmr,tn): nt.links.new(uv.outputs["UV"],tex.inputs["Vector"])
    nt.links.new(tbase.outputs["Color"],bs.inputs["Base Color"])
    nt.links.new(tmr.outputs["Color"],sep.inputs["Color"])
    nt.links.new(sep.outputs["Green"],bs.inputs["Roughness"])
    nt.links.new(sep.outputs["Blue"],bs.inputs["Metallic"])
    nt.links.new(tn.outputs["Color"],nmap.inputs["Color"])
    nt.links.new(nmap.outputs["Normal"],bs.inputs["Normal"])
    nt.links.new(bs.outputs["BSDF"],out.inputs["Surface"])
    bs.inputs["IOR"].default_value=1.46 if spec["metal"]==0.0 else 1.50
    m["generator_stage"]=STAGE
    m["production_state"]="CALIBRATION_PROTOTYPE_NOT_FINAL"
    m["asset_family"]=spec["family"]
    m["physical_role"]=spec["role"]
    m["roughness_intent_min"]=spec["rough"][0]
    m["roughness_intent_max"]=spec["rough"][1]
    m["metallic_intent"]=spec["metal"]


def build():
    receipts=[]
    for spec in SWATCHES:
        arrays=_arrays(spec); images=[]; srcs=[]; pngs=[]
        for suffix,arr,nc in (("_BASECOLOR",arrays[0],False),("_MR",arrays[1],True),("_NORMAL",arrays[2],True)):
            old=bpy.data.images.get(spec["name"]+suffix)
            if old: old.name=spec["name"]+suffix+"__V2_REJECTED"
            img,src,png=_packed_png_image(spec["name"]+suffix,arr,nc)
            images.append(img); srcs.append(src); pngs.append(png)
        _rewire(spec,*images)
        receipts.append({"name":spec["name"],"asset_family":spec["family"],"source_u8_sha256":srcs,"packed_png_sha256":pngs})
    for img in list(bpy.data.images):
        if img.name.endswith("__V2_REJECTED") or img.name.endswith("__V1_REJECTED"):
            bpy.data.images.remove(img)
    scene=bpy.context.scene
    scene["pbr_calibration_stage"]=STAGE
    scene["v1_persistence_contract"]="REJECTED_GENERATED_IMAGES_NOT_DURABLE"
    scene["v2_persistence_contract"]="REJECTED_BLENDER_IMAGE_SAVE_ENCODED_BLANK_PNG"
    scene["final_art_approved"]=False
    scene["world_master_propagation_approved"]=False
    calimgs=[i for i in bpy.data.images if i.name.startswith(("LEV_CAL_","HUM_CAL_")) and any(i.name.endswith(s) for s in ("_BASECOLOR","_MR","_NORMAL"))]
    packed_shas=[i.get("packed_png_sha256") for i in calimgs]
    return {
        "stage":STAGE,
        "swatches":receipts,
        "calibration_images":len(calimgs),
        "packed_images":sum(1 for i in calimgs if i.packed_file),
        "external_filepath_images":sum(1 for i in calimgs if i.filepath_raw),
        "file_sources":sum(1 for i in calimgs if i.source=="FILE"),
        "unique_packed_png_sha256":len(set(packed_shas)),
        "uvmap_nodes":sum(1 for m in bpy.data.materials if m.name.startswith(("LEV_CAL_","HUM_CAL_")) for n in m.node_tree.nodes if n.type=="UVMAP"),
        "status":"DURABLE_PNG_FIX_NOT_YET_REOPEN_VERIFIED",
    }

if __name__=="__main__": print(build())
