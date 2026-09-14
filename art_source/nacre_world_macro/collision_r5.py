"""NACRE R5 collision pass.

Adds simple static traversal collision proxies to the reproducible R4 macro blockout.
Godot import contract: mesh node names end in `-colonly`, so editor glTF import removes
the visual proxy mesh and creates StaticBody3D collision geometry.

Included: 10 archive bridge decks, entry bridge, entry service platform.
Explicitly waived here: archive chamber hulls, global shell surface and service rings.
Those require region/interior-aware collision and must not be replaced by solid convex hulls.
"""

import bpy
from mathutils import Vector

CHECKPOINT_REVISION = 5
COLLISION_PASS_VERSION = 1
COLLECTION = "50_COLLISION_PROXIES"


def local_mesh_dims(obj):
    xs = [v.co.x for v in obj.data.vertices]
    ys = [v.co.y for v in obj.data.vertices]
    zs = [v.co.z for v in obj.data.vertices]
    return Vector((max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs)))


def ensure_collection(scene):
    coll = bpy.data.collections.get(COLLECTION)
    if coll is None:
        coll = bpy.data.collections.new(COLLECTION)
        scene.collection.children.link(coll)
    elif coll.name not in scene.collection.children.keys():
        scene.collection.children.link(coll)
    return coll


def clear_previous():
    for obj in list(bpy.data.objects):
        if obj.name.startswith("NACRE_COLL_") and obj.name.endswith("-colonly"):
            bpy.data.objects.remove(obj, do_unlink=True)


def make_proxy(coll, name, src, z_ratio=0.62, min_z=0.35):
    dims = local_mesh_dims(src)
    pdims = Vector((dims.x, dims.y, max(min_z, dims.z*z_ratio)))
    bpy.ops.mesh.primitive_cube_add(size=1, location=src.location)
    proxy = bpy.context.object
    proxy.name = name
    proxy.data.name = name + "_MESH"
    for old in list(proxy.users_collection):
        old.objects.unlink(proxy)
    coll.objects.link(proxy)
    proxy.rotation_mode = "QUATERNION"
    proxy.rotation_quaternion = src.rotation_quaternion.copy()
    proxy.dimensions = pdims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    proxy["collision_role"] = "static_traversal_proxy"
    proxy["source_visual"] = src.name
    proxy["godot_import_hint"] = "-colonly"
    return proxy


def build():
    scene = bpy.context.scene
    coll = ensure_collection(scene)
    clear_previous()
    created = []
    for i in range(10):
        src = bpy.data.objects.get(f"BRIDGE_DECK_{i:02d}")
        if src is None or src.type != "MESH":
            raise RuntimeError(f"missing BRIDGE_DECK_{i:02d}")
        created.append(make_proxy(coll, f"NACRE_COLL_BRIDGE_{i:02d}-colonly", src, 0.62, 0.55))

    src = bpy.data.objects.get("BRIDGE_ENTRY_MAIN")
    if src is None:
        raise RuntimeError("missing BRIDGE_ENTRY_MAIN")
    created.append(make_proxy(coll, "NACRE_COLL_ENTRY_BRIDGE-colonly", src, 0.62, 0.70))

    src = bpy.data.objects.get("ENTRY_SERVICE_PLATFORM")
    if src is None:
        raise RuntimeError("missing ENTRY_SERVICE_PLATFORM")
    created.append(make_proxy(coll, "NACRE_COLL_ENTRY_PLATFORM-colonly", src, 0.66, 1.20))

    scene["NACRE_CHECKPOINT_REVISION"] = CHECKPOINT_REVISION
    scene["COLLISION_PASS_VERSION"] = COLLISION_PASS_VERSION
    scene["COLLISION_PROXY_COUNT"] = len(created)
    scene["COLLISION_POLICY"] = "12 simple static traversal proxies using Godot -colonly; archive shells/global shell intentionally waived"
    scene["COLLISION_WAIVER"] = "Archive chamber hulls and global shell require region/interior-aware collision; no solid convex chamber proxies."

    violations = []
    for proxy in created:
        src = bpy.data.objects.get(proxy["source_visual"])
        pdims = local_mesh_dims(proxy)
        sdims = local_mesh_dims(src)
        if pdims.x > sdims.x + 1e-5 or pdims.y > sdims.y + 1e-5 or pdims.z >= sdims.z:
            violations.append(proxy.name)
    if violations:
        raise RuntimeError("collision proxy containment failed: " + ", ".join(violations))
    return created


if __name__ == "__main__":
    build()
