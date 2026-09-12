"""Semantic reproducibility fingerprint for EXOVANT KHEPRI world-macro.

Canonicalizes geometry independently of mesh vertex-index ordering. This is required because
Blender primitive operators may assign equivalent UV-sphere indices differently across fresh
projects even when the actual vertex multiset and face geometry are identical.

This script does NOT claim binary-identical .blend/GLB serialization. It proves semantic scene
reproduction for the CLM-KHEPRI-WMACRO-001 blockout contract.
"""
import bpy, json, hashlib

ROUND_DIGITS = 6

def rnd(v): return round(float(v), ROUND_DIGITS)
def sha(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def custom_props(idblock):
    out = {}
    for key in sorted(idblock.keys()):
        if key == "_RNA_UI" or key == "hf_id" or key.startswith("hf_"):
            continue
        value = idblock[key]
        if isinstance(value, (str, int, float, bool)):
            out[key] = value
        elif hasattr(value, "__len__") and not isinstance(value, (str, bytes)):
            try:
                out[key] = [rnd(x) if isinstance(x, (int, float)) else str(x) for x in value]
            except Exception:
                out[key] = str(value)
        else:
            out[key] = str(value)
    return out

def semantic_fingerprint():
    objects = []
    for obj in sorted(bpy.data.objects, key=lambda x: x.name):
        row = {
            "name": obj.name,
            "type": obj.type,
            "location": [rnd(v) for v in obj.location],
            "rotation": [rnd(v) for v in obj.rotation_euler],
            "scale": [rnd(v) for v in obj.scale],
            "dimensions": [rnd(v) for v in obj.dimensions],
            "collections": sorted(c.name for c in obj.users_collection),
            "materials": sorted(m.name for m in (obj.data.materials if getattr(obj, "data", None) and hasattr(obj.data, "materials") else []) if m),
            "props": custom_props(obj),
        }
        if obj.type == "CAMERA":
            row["camera"] = [rnd(obj.data.lens), rnd(obj.data.sensor_width)]
        if obj.type == "LIGHT":
            row["light"] = [obj.data.type, rnd(obj.data.energy), [rnd(v) for v in obj.data.color]]
        objects.append(row)

    meshes = []
    for mesh in sorted(bpy.data.meshes, key=lambda x: x.name):
        indexed_vertices = [tuple(rnd(c) for c in v.co) for v in mesh.vertices]
        vertex_multiset = sorted(indexed_vertices)
        face_geometry = []
        for polygon in mesh.polygons:
            face_geometry.append(sorted(indexed_vertices[index] for index in polygon.vertices))
        meshes.append({
            "name": mesh.name,
            "vertex_multiset": vertex_multiset,
            "face_geometry": sorted(face_geometry),
            "materials": [m.name if m else None for m in mesh.materials],
        })

    curves = []
    for curve in sorted(bpy.data.curves, key=lambda x: x.name):
        curves.append({
            "name": curve.name,
            "bevel_depth": rnd(curve.bevel_depth),
            "splines": [
                {"type": spline.type, "points": [[rnd(v) for v in p.co] for p in spline.points]}
                for spline in curve.splines
            ],
            "materials": [m.name if m else None for m in curve.materials],
        })

    materials = []
    for mat in sorted(bpy.data.materials, key=lambda x: x.name):
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        materials.append({
            "name": mat.name,
            "base": [rnd(v) for v in bsdf.inputs["Base Color"].default_value],
            "metallic": rnd(bsdf.inputs["Metallic"].default_value),
            "roughness": rnd(bsdf.inputs["Roughness"].default_value),
            "emission": [rnd(v) for v in bsdf.inputs["Emission Color"].default_value],
            "emission_strength": rnd(bsdf.inputs["Emission Strength"].default_value),
        })

    payload = {
        "objects": objects,
        "meshes": meshes,
        "curves": curves,
        "materials": materials,
        "scene": custom_props(bpy.context.scene),
        "units": [bpy.context.scene.unit_settings.system, rnd(bpy.context.scene.unit_settings.scale_length)],
    }
    return {
        "semantic_sha256": sha(payload),
        "objects": len(objects),
        "meshes": len(meshes),
        "curves": len(curves),
        "materials": len(materials),
    }

result = semantic_fingerprint()
print(json.dumps(result, indent=2, sort_keys=True))
