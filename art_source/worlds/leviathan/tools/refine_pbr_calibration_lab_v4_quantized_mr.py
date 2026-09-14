"""LEVIATHAN PBR calibration lab v4 — quantization-safe metallic/roughness maps.

r3 persistence is valid, but the 8-bit decoded Ivory Ceramic roughness reached 87/255 = 0.341176,
slightly above its declared 0.34 ceiling. v4 regenerates only the six MR maps and clamps authored
roughness to the nearest representable 8-bit values strictly inside each declared interval:
ceil(min*255)/255 <= decoded roughness <= floor(max*255)/255.

BaseColor, Normal, geometry, cameras and lights remain unchanged.
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

STAGE = "LEVIATHAN_PBR_CALIBRATION_LAB_V4_QUANTIZED_MR"
RES = 256

SPECS = [
    {"name":"LEV_CAL_TISSUE_WARM","rough":(0.36,0.58),"metal":0.0,"pattern":"tissue"},
    {"name":"LEV_CAL_MUCOSA_WET","rough":(0.10,0.28),"metal":0.0,"pattern":"mucosa"},
    {"name":"LEV_CAL_CARTILAGE","rough":(0.38,0.62),"metal":0.0,"pattern":"cartilage"},
    {"name":"HUM_CAL_IVORY_CERAMIC","rough":(0.20,0.34),"metal":0.0,"pattern":"ceramic"},
    {"name":"HUM_CAL_BRUSHED_METAL","rough":(0.24,0.42),"metal":1.0,"pattern":"metal"},
    {"name":"HUM_CAL_SEAL_RUBBER","rough":(0.56,0.78),"metal":0.0,"pattern":"rubber"},
]


def _height(spec):
    y,x=np.mgrid[0:RES,0:RES].astype(np.float32); u=x/RES; v=y/RES; t=np.float32(math.tau); p=spec["pattern"]
    if p=="tissue":
        a=0.55+0.23*np.sin(t*(u*2.0+0.14*np.sin(v*t*2.0)))+0.12*np.sin(t*(v*7.0-u*1.5)); b=0.5+0.5*np.sin(t*(u*31.0+v*23.0))*np.sin(t*(v*37.0-u*11.0)); h=0.70*a+0.30*b
    elif p=="mucosa":
        a=0.5+0.5*np.sin(t*(v*5.0+0.18*np.sin(u*t*3.0))); b=0.5+0.5*np.cos(t*(u*29.0))*np.cos(t*(v*31.0)); h=0.78*a+0.22*b
    elif p=="cartilage":
        a=0.5+0.5*np.sin(t*(u*10.0+0.09*np.sin(v*t*4.0))); b=0.5+0.5*np.sin(t*(v*3.0-u*1.2)); h=0.76*a+0.24*b
    elif p=="ceramic":
        a=0.5+0.5*np.sin(t*(u*47.0+v*19.0))*np.sin(t*(u*13.0-v*43.0)); b=0.5+0.5*np.sin(t*(u*1.0+v*0.7)); h=0.30*a+0.70*b
    elif p=="metal":
        a=0.5+0.5*np.sin(t*(v*96.0+0.05*np.sin(u*t*2.0))); b=0.5+0.5*np.sin(t*(u*2.0)); h=0.86*a+0.14*b
    else:
        a=0.5+0.5*np.sin(t*(u*41.0+v*17.0))*np.cos(t*(v*37.0-u*7.0)); b=0.5+0.5*np.sin(t*(u*3.0+v*2.0)); h=0.70*a+0.30*b
    return np.clip(h,0,1).astype(np.float32)


def _mr(spec):
    h=_height(spec); rmin,rmax=spec["rough"]
    rough=rmin+(rmax-rmin)*(0.25+0.75*h)
    qlo=math.ceil(rmin*255.0)/255.0
    qhi=math.floor(rmax*255.0)/255.0
    if qlo>qhi: raise RuntimeError("No 8-bit representable roughness interval for "+spec["name"])
    rough=np.clip(rough,qlo,qhi)
    arr=np.zeros((RES,RES,4),dtype=np.float32); arr[:,:,0]=1.0; arr[:,:,1]=rough; arr[:,:,2]=spec["metal"]; arr[:,:,3]=1.0
    return arr,qlo,qhi


def _rgba8(a): return np.clip(np.rint(a*255.0),0,255).astype(np.uint8)
def _chunk(k,d): return struct.pack(">I",len(d))+k+d+struct.pack(">I",binascii.crc32(k+d)&0xffffffff)
def _png(q):
    h,w,_=q.shape; rows=np.flipud(q).copy(); raw=b"".join(b"\x00"+rows[y].tobytes(order="C") for y in range(h))
    return b"\x89PNG\r\n\x1a\n"+_chunk(b"IHDR",struct.pack(">IIBBBBB",w,h,8,6,0,0,0))+_chunk(b"IDAT",zlib.compress(raw,9))+_chunk(b"IEND",b"")


def _packed_mr(name,arr):
    q=_rgba8(arr); source_sha=hashlib.sha256(q.tobytes(order="C")).hexdigest(); data=_png(q); png_sha=hashlib.sha256(data).hexdigest()
    fd,path=tempfile.mkstemp(prefix="lev_pbr_mr_v4_",suffix=".png"); os.close(fd)
    try:
        with open(path,"wb") as f: f.write(data)
        img=bpy.data.images.load(path,check_existing=False); img.name=name
        try: img.colorspace_settings.name="Non-Color"
        except Exception: pass
        _=img.pixels[0]; img.pack()
        if not img.packed_file: raise RuntimeError("MR pack failed for "+name)
        if hashlib.sha256(bytes(img.packed_file.data)).hexdigest()!=png_sha: raise RuntimeError("MR packed digest mismatch for "+name)
        img["generator_stage"]=STAGE; img["resolution"]=RES; img["source_u8_rgba_sha256"]=source_sha; img["packed_png_sha256"]=png_sha; img.filepath_raw=""
        return img,source_sha,png_sha
    finally:
        if os.path.exists(path): os.remove(path)


def build():
    receipts=[]
    for spec in SPECS:
        arr,qlo,qhi=_mr(spec)
        old=bpy.data.images.get(spec["name"]+"_MR")
        if old: old.name=spec["name"]+"_MR__V3_REJECTED_RANGE"
        img,src,png_sha=_packed_mr(spec["name"]+"_MR",arr)
        mat=bpy.data.materials.get(spec["name"])
        mrnodes=[n for n in mat.node_tree.nodes if n.type=="TEX_IMAGE" and n.label=="MR"]
        if len(mrnodes)!=1: raise RuntimeError("Expected one labeled MR node for "+spec["name"])
        mrnodes[0].image=img
        mat["roughness_quantized_min"] = qlo
        mat["roughness_quantized_max"] = qhi
        receipts.append({"name":spec["name"],"declared":list(spec["rough"]),"quantized_bounds":[qlo,qhi],"source_u8_sha256":src,"packed_png_sha256":png_sha})
    for img in list(bpy.data.images):
        if img.name.endswith("__V3_REJECTED_RANGE"): bpy.data.images.remove(img)
    scene=bpy.context.scene; scene["pbr_calibration_stage"]=STAGE; scene["final_art_approved"]=False; scene["world_master_propagation_approved"]=False
    return {"stage":STAGE,"mr_receipts":receipts,"status":"QUANTIZED_MR_FIX_NOT_YET_REOPEN_VERIFIED"}

if __name__=="__main__": print(build())
