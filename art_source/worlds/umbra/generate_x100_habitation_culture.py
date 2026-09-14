"""EXOVANT 2950 / UMBRA / X100 habitation-culture systemic library.

Builds 10 daily-survival families × S/M/L × SERVICED/LIVED_IN/FIELD_REPAIRED.
The library is a production proposal derived from established Sin Sol constraints:
mobile twilight survival, constant wind, dark metal, tension fabric, ivory repair,
amber refuge hierarchy, low profile and maintainability.

This script intentionally does NOT invent religion, narrative text, native ecology,
planet scale or runtime interaction semantics.

The first authored refuge-site composition produced by this generator was later
relocated by `fix_x100_habitation_annex.py` after QA proved the existing refuge
hub base is still a closed blockout volume.
"""

import bpy
import math
from mathutils import Vector

scene = bpy.context.scene
terrain = bpy.data.objects["ENV_TERRAIN_TWILIGHT_BAND_BLOCKOUT"]
world = bpy.data.collections.get("W04_UMBRA")
assert world
if bpy.data.collections.get("92_X100_HABITATION_LIBRARY"):
    raise RuntimeError("X100 habitation library already exists")

lib = bpy.data.collections.new("92_X100_HABITATION_LIBRARY")
world.children.link(lib)
site = bpy.data.collections.new("93_X100_REFUGE_HABITATION")
world.children.link(site)

mats = {
    "metal": bpy.data.materials["MAT_SINSOL_DARK_METAL"],
    "fabric": bpy.data.materials["MAT_SINSOL_TENSION_FABRIC"],
    "ivory": bpy.data.materials["MAT_COLONIAL_IVORY_REPAIR"],
    "amber": bpy.data.materials["MAT_REFUGE_AMBER"],
    "copper": bpy.data.materials["MAT_SINSOL_THERMAL_COPPER"],
    "gasket": bpy.data.materials["MAT_SINSOL_GASKET"],
}

if bpy.data.materials.get("MAT_SINSOL_THERMAL_CERAMIC") is None:
    m = bpy.data.materials.new("MAT_SINSOL_THERMAL_CERAMIC")
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (0.32, 0.34, 0.33, 1)
    b.inputs["Roughness"].default_value = 0.42
    b.inputs["Metallic"].default_value = 0.05
mats["ceramic"] = bpy.data.materials["MAT_SINSOL_THERMAL_CERAMIC"]

box_cache = {}
cyl_cache = {}


def box_mesh(dims, mat):
    key = (tuple(round(float(v), 4) for v in dims), mat.name)
    if key in box_cache:
        return box_cache[key]
    dx, dy, dz = [v / 2 for v in dims]
    vs = [
        (-dx, -dy, -dz), (dx, -dy, -dz), (dx, dy, -dz), (-dx, dy, -dz),
        (-dx, -dy, dz), (dx, -dy, dz), (dx, dy, dz), (-dx, dy, dz),
    ]
    fs = [
        (0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
        (1, 5, 6, 2), (2, 6, 7, 3), (4, 0, 3, 7),
    ]
    me = bpy.data.meshes.new(f"MESH_X100H_BOX_{len(box_cache):03d}")
    me.from_pydata(vs, [], fs)
    me.materials.append(mat)
    box_cache[key] = me
    return me


def cyl_mesh(radius, depth, mat, verts=12):
    key = (round(radius, 4), round(depth, 4), mat.name, verts)
    if key in cyl_cache:
        return cyl_cache[key]
    vs, fs = [], []
    for z in (-depth / 2, depth / 2):
        for i in range(verts):
            a = 2 * math.pi * i / verts
            vs.append((radius * math.cos(a), radius * math.sin(a), z))
    for i in range(verts):
        j = (i + 1) % verts
        fs.append((i, j, verts + j, verts + i))
    fs.append(tuple(range(verts - 1, -1, -1)))
    fs.append(tuple(range(verts, 2 * verts)))
    me = bpy.data.meshes.new(f"MESH_X100H_CYL_{len(cyl_cache):03d}")
    me.from_pydata(vs, [], fs)
    me.materials.append(mat)
    cyl_cache[key] = me
    return me


def obj(name, mesh, parent, loc=(0, 0, 0), rot=(0, 0, 0)):
    o = bpy.data.objects.new(name, mesh)
    lib.objects.link(o)
    o.parent = parent
    o.location = loc
    o.rotation_euler = rot
    return o


def root(name, loc, props):
    o = bpy.data.objects.new(name, None)
    lib.objects.link(o)
    o.location = loc
    for k, v in props.items():
        o[k] = v
    return o


def terrain_z(x, y):
    inv = terrain.matrix_world.inverted()
    origin = inv @ Vector((x, y, 250.0))
    direction = (inv.to_3x3() @ Vector((0, 0, -1))).normalized()
    hit, loc, _n, _idx = terrain.ray_cast(origin, direction, distance=700.0)
    if not hit:
        raise RuntimeError(f"No terrain at {x},{y}")
    return (terrain.matrix_world @ loc).z


families = [
    ("SLEEP_POD", "insulated low-profile sleeping/rest module"),
    ("RATION_LOCKER", "sealed ration and dry-consumables locker"),
    ("MESS_TRAY", "washable heated meal tray / communal eating surface"),
    ("HEATED_BENCH", "low communal heated bench with under-seat storage"),
    ("DRYING_RACK", "glove/boot/textile drying and warming frame"),
    ("PERSONAL_LOCKER", "small personal-effects locker with glove latch"),
    ("MED_CABINET", "field first-aid/medical storage cabinet; contents unspecified"),
    ("PRIVACY_SCREEN", "tension-fabric privacy and thermal partition"),
    ("CREW_ID_PLATE", "non-text caravan/crew identity plate using notch/bar encoding"),
    ("THERMAL_VESSEL_RACK", "secured rack for insulated food/drink vessels"),
]
sizes = {"S": 0.82, "M": 1.0, "L": 1.24}
states = ["SERVICED", "LIVED_IN", "FIELD_REPAIRED"]
roots = []
base_x, base_y = -560, 292

for fi, (fam, purpose) in enumerate(families):
    row, col = fi // 5, fi % 5
    family_x, family_y = base_x + col * 70, base_y + row * 34
    for si, (skey, sc) in enumerate(sizes.items()):
        for ti, state in enumerate(states):
            x, y = family_x + si * 17, family_y + ti * 9
            gz = terrain_z(x, y)
            rid = fi * 9 + si * 3 + ti
            name = f"X100H_{fam}_{skey}_{state}_{rid:02d}"
            r = root(name, (x, y, gz + 0.03), {
                "stable_id": f"W04-X100H-{fam}-{skey}-{state}-{rid:02d}",
                "family": fam,
                "size_variant": skey,
                "state_variant": state,
                "semantic_purpose": purpose,
                "epistemic": "PRODUCTION_PROPOSAL_DERIVED_FROM_SINSOL_SURVIVAL_CONSTRAINTS",
                "culture_dna": "low-profile; glove-ergonomic; strapped/sealed storage; replaceable parts; dark metal+tension fabric+ivory repair+amber refuge hierarchy",
                "variation_cause": {
                    "SERVICED": "recently serviced / intact",
                    "LIVED_IN": "repeated daily use / occupancy",
                    "FIELD_REPAIRED": "local replacement / scarcity-driven repair",
                }[state],
                "placement_rule": "refuge/caravan habitation interiors or protected leeward service spaces; preserve >=1.2m local access and >=2.4m primary corridor",
                "gameplay_tags": "environmental affordance by default; interaction external unless explicitly integrated",
                "story_tags": "daily-survival, mobile-habitation, thermal-conservation, resource-scarcity, repair-history",
                "lod_strategy": "LOD0 foundation; LOD1/LOD2/HLOD pending runtime target contract",
                "collision_strategy": "simple box/convex proxy from occupied envelope pending integration owner",
                "credible_configurations": 108,
            })
            roots.append(r)

            if fam == "SLEEP_POD":
                w, L, h = 1.0 * sc, 2.05 * sc, 0.72 * sc
                obj(name + "_BASE", box_mesh((w, L, 0.16 * sc), mats["metal"]), r, (0, 0, 0.08 * sc))
                obj(name + "_PAD", box_mesh((w * 0.88, L * 0.88, 0.18 * sc), mats["fabric"]), r, (0, 0, 0.25 * sc))
                obj(name + "_HEAD", box_mesh((w, 0.12 * sc, h), mats["metal"]), r, (0, L * 0.47, h / 2))
                obj(name + "_THERMAL_RAIL", box_mesh((0.08 * sc, L * 0.76, 0.10 * sc), mats["copper"]), r, (w * 0.46, 0, 0.39 * sc))
                for yy in (-L * 0.28, L * 0.28):
                    obj(name + f"_STRAP_{yy:.2f}", box_mesh((w * 0.96, 0.08 * sc, 0.06 * sc), mats["ivory"]), r, (0, yy, 0.39 * sc))
            elif fam == "RATION_LOCKER":
                w, d, h = 1.15 * sc, 0.62 * sc, 1.45 * sc
                obj(name + "_BODY", box_mesh((w, d, h), mats["metal"]), r, (0, 0, h / 2))
                obj(name + "_DOOR", box_mesh((w * 0.90, 0.05 * sc, h * 0.88), mats["ivory"]), r, (0, -d / 2 - 0.03 * sc, h * 0.52))
                for zz in (0.38, 0.78, 1.15):
                    obj(name + f"_SHELF_{zz}", box_mesh((w * 0.86, d * 0.72, 0.05 * sc), mats["ceramic"]), r, (0, 0, zz * sc))
                obj(name + "_LATCH", box_mesh((0.22 * sc, 0.10 * sc, 0.34 * sc), mats["amber"]), r, (w * 0.30, -d / 2 - 0.07 * sc, h * 0.55))
            elif fam == "MESS_TRAY":
                w, d, h = 1.65 * sc, 0.82 * sc, 0.78 * sc
                obj(name + "_TOP", box_mesh((w, d, 0.10 * sc), mats["ceramic"]), r, (0, 0, h))
                for xx in (-w * 0.42, w * 0.42):
                    obj(name + f"_LEG_{xx:.2f}", box_mesh((0.10 * sc, d * 0.72, h), mats["metal"]), r, (xx, 0, h / 2))
                obj(name + "_HEAT_BAR", box_mesh((w * 0.68, 0.12 * sc, 0.12 * sc), mats["copper"]), r, (0, d * 0.32, h - 0.12 * sc))
                for xx in (-0.45, 0, 0.45):
                    obj(name + f"_VESSEL_STOP_{xx}", cyl_mesh(0.12 * sc, 0.08 * sc, mats["ivory"], 12), r, (xx * sc, 0, h + 0.09 * sc))
            elif fam == "HEATED_BENCH":
                w, d, h = 1.8 * sc, 0.62 * sc, 0.52 * sc
                obj(name + "_SEAT", box_mesh((w, d, 0.14 * sc), mats["fabric"]), r, (0, 0, h))
                obj(name + "_UNDERBOX", box_mesh((w * 0.82, d * 0.78, h * 0.72), mats["metal"]), r, (0, 0, h * 0.42))
                obj(name + "_THERMAL", box_mesh((w * 0.72, 0.08 * sc, 0.12 * sc), mats["copper"]), r, (0, d * 0.42, h * 0.70))
                for xx in (-w * 0.38, w * 0.38):
                    obj(name + f"_FOOT_{xx:.2f}", box_mesh((0.12 * sc, d * 0.8, 0.10 * sc), mats["ivory"]), r, (xx, 0, 0.05 * sc))
            elif fam == "DRYING_RACK":
                w, d, h = 1.45 * sc, 0.55 * sc, 1.65 * sc
                for xx in (-w / 2, w / 2):
                    obj(name + f"_POST_{xx:.2f}", box_mesh((0.08 * sc, 0.08 * sc, h), mats["metal"]), r, (xx, 0, h / 2))
                obj(name + "_TOP", box_mesh((w + 0.08 * sc, 0.08 * sc, 0.08 * sc), mats["metal"]), r, (0, 0, h))
                obj(name + "_HEAT", box_mesh((w * 0.82, 0.10 * sc, 0.10 * sc), mats["copper"]), r, (0, 0, h * 0.28))
                for xx in (-0.45, -0.15, 0.15, 0.45):
                    obj(name + f"_HOOK_{xx}", cyl_mesh(0.035 * sc, 0.28 * sc, mats["ivory"], 8), r, (xx * w, 0, h * 0.73), (math.pi / 2, 0, 0))
                obj(name + "_FOOT", box_mesh((w * 1.1, d, 0.08 * sc), mats["metal"]), r, (0, 0, 0.04 * sc))
            elif fam == "PERSONAL_LOCKER":
                w, d, h = 0.72 * sc, 0.48 * sc, 1.25 * sc
                obj(name + "_BODY", box_mesh((w, d, h), mats["metal"]), r, (0, 0, h / 2))
                obj(name + "_DOOR", box_mesh((w * 0.90, 0.05 * sc, h * 0.90), mats["fabric"]), r, (0, -d / 2 - 0.03 * sc, h / 2))
                obj(name + "_LATCH", box_mesh((0.16 * sc, 0.09 * sc, 0.28 * sc), mats["ivory"]), r, (w * 0.28, -d / 2 - 0.07 * sc, h * 0.54))
                for i in range(3):
                    obj(name + f"_IDBAR_{i}", box_mesh((0.08 * sc, 0.04 * sc, (0.12 + 0.06 * i) * sc), mats["amber"]), r, ((-0.16 + 0.12 * i) * sc, -d / 2 - 0.06 * sc, h * 0.82))
            elif fam == "MED_CABINET":
                w, d, h = 0.94 * sc, 0.42 * sc, 1.05 * sc
                obj(name + "_BODY", box_mesh((w, d, h), mats["metal"]), r, (0, 0, h / 2))
                obj(name + "_DOOR", box_mesh((w * 0.90, 0.05 * sc, h * 0.88), mats["ceramic"]), r, (0, -d / 2 - 0.03 * sc, h / 2))
                obj(name + "_MARK_A", box_mesh((w * 0.44, 0.04 * sc, 0.08 * sc), mats["amber"]), r, (0, -d / 2 - 0.06 * sc, h * 0.60))
                obj(name + "_MARK_B", box_mesh((0.08 * sc, 0.04 * sc, h * 0.34), mats["amber"]), r, (0, -d / 2 - 0.06 * sc, h * 0.60))
                obj(name + "_GASKET", box_mesh((w * 0.96, d * 0.04, h * 0.96), mats["gasket"]), r, (0, -d / 2, h / 2))
            elif fam == "PRIVACY_SCREEN":
                w, h = 1.75 * sc, 1.85 * sc
                for xx in (-w / 2, w / 2):
                    obj(name + f"_POST_{xx:.2f}", box_mesh((0.07 * sc, 0.12 * sc, h), mats["metal"]), r, (xx, 0, h / 2))
                obj(name + "_TOP", box_mesh((w, 0.10 * sc, 0.08 * sc), mats["ivory"]), r, (0, 0, h))
                obj(name + "_FABRIC", box_mesh((w * 0.90, 0.025 * sc, h * 0.82), mats["fabric"]), r, (0, 0, h * 0.52))
                for xx in (-w * 0.42, w * 0.42):
                    obj(name + f"_FOOT_{xx:.2f}", box_mesh((0.42 * sc, 0.55 * sc, 0.07 * sc), mats["metal"]), r, (xx, 0, 0.035 * sc))
            elif fam == "CREW_ID_PLATE":
                w, h = 1.10 * sc, 0.58 * sc
                obj(name + "_PLATE", box_mesh((w, 0.08 * sc, h), mats["metal"]), r, (0, 0, h / 2))
                for i, hh in enumerate((0.18, 0.30, 0.42, 0.25)):
                    obj(name + f"_BAR_{i}", box_mesh((0.07 * sc, 0.05 * sc, hh * sc), mats["ivory"] if i % 2 == 0 else mats["amber"]), r, ((-0.33 + 0.22 * i) * sc, -0.065 * sc, h * 0.52))
                obj(name + "_HORIZON", box_mesh((w * 0.72, 0.05 * sc, 0.06 * sc), mats["ivory"]), r, (0, -0.065 * sc, h * 0.22))
            elif fam == "THERMAL_VESSEL_RACK":
                w, d, h = 1.35 * sc, 0.55 * sc, 1.10 * sc
                obj(name + "_BASE", box_mesh((w, d, 0.10 * sc), mats["metal"]), r, (0, 0, 0.05 * sc))
                for xx in (-w * 0.46, w * 0.46):
                    obj(name + f"_POST_{xx:.2f}", box_mesh((0.07 * sc, 0.07 * sc, h), mats["metal"]), r, (xx, 0, h / 2))
                for i, xx in enumerate((-0.36, 0, 0.36)):
                    obj(name + f"_VESSEL_{i}", cyl_mesh(0.16 * sc, 0.62 * sc, mats["ceramic"], 12), r, (xx * w, 0, 0.42 * sc))
                    obj(name + f"_BAND_{i}", cyl_mesh(0.18 * sc, 0.08 * sc, mats["copper"], 12), r, (xx * w, 0, 0.50 * sc))
                obj(name + "_TOPRAIL", box_mesh((w, 0.08 * sc, 0.08 * sc), mats["ivory"]), r, (0, 0, h))

            if state == "SERVICED":
                obj(name + "_SERVICE_TAG", box_mesh((0.24 * sc, 0.045 * sc, 0.12 * sc), mats["amber"]), r, (0, -0.42 * sc, 0.22 * sc))
            elif state == "LIVED_IN":
                obj(name + "_USE_STRAP", box_mesh((0.42 * sc, 0.06 * sc, 0.08 * sc), mats["fabric"]), r, (0.18 * sc, -0.38 * sc, 0.18 * sc), (0, 0, math.radians(7)))
                r["lived_in_cause"] = "daily occupancy / repeated handling; no random grunge"
            else:
                obj(name + "_REPAIR_PATCH", box_mesh((0.38 * sc, 0.05 * sc, 0.24 * sc), mats["ivory"]), r, (-0.22 * sc, -0.40 * sc, 0.26 * sc), (0, 0, math.radians(-6)))
                obj(name + "_REPAIR_CLAMP", box_mesh((0.10 * sc, 0.09 * sc, 0.36 * sc), mats["metal"]), r, (0.06 * sc, -0.43 * sc, 0.26 * sc))


def descendants(r):
    out, stack = [], list(r.children)
    while stack:
        o = stack.pop()
        out.append(o)
        stack.extend(list(o.children))
    return out


def source(fam, size, state):
    return [r for r in roots if r.get("family") == fam and r.get("size_variant") == size and r.get("state_variant") == state][0]


def clone_to_site(src, name, loc, rz=0):
    nr = src.copy()
    nr.data = None
    nr.parent = None
    nr.name = name
    nr.location = loc
    nr.rotation_euler = (0, 0, math.radians(rz))
    for c in list(nr.users_collection):
        c.objects.unlink(nr)
    site.objects.link(nr)
    nr["source_stable_id"] = src.get("stable_id")
    nr["site"] = "REFUGE_HABITATION"
    nr["integration_status"] = "HABITATION_SITE_PROPOSAL"
    for so in descendants(src):
        no = so.copy()
        no.data = so.data
        no.name = f"{name}__{so.name}"
        no.parent = nr
        no.matrix_parent_inverse = so.matrix_parent_inverse.copy()
        no.location = so.location.copy()
        no.rotation_euler = so.rotation_euler.copy()
        no.scale = so.scale.copy()
        for c in list(no.users_collection):
            c.objects.unlink(no)
        site.objects.link(no)
    return nr


ref = bpy.data.objects["ARCH_REFUGE_HUB_BASE"]
floor = ref.matrix_world.translation.z - ref.dimensions.z / 2 + 0.10
layout = [
    ("SLEEP_POD", "M", "LIVED_IN", (56, 25, floor), 0),
    ("SLEEP_POD", "M", "FIELD_REPAIRED", (64, 25, floor), 0),
    ("PERSONAL_LOCKER", "M", "LIVED_IN", (55, 30, floor), 90),
    ("PERSONAL_LOCKER", "M", "FIELD_REPAIRED", (59, 30, floor), 90),
    ("HEATED_BENCH", "L", "LIVED_IN", (72, 25, floor), 0),
    ("MESS_TRAY", "M", "LIVED_IN", (72, 30, floor), 0),
    ("RATION_LOCKER", "M", "SERVICED", (86, 26, floor), 90),
    ("THERMAL_VESSEL_RACK", "M", "LIVED_IN", (89, 31, floor), 90),
    ("DRYING_RACK", "M", "LIVED_IN", (56, 45, floor), 0),
    ("PRIVACY_SCREEN", "M", "FIELD_REPAIRED", (65, 45, floor), 0),
    ("MED_CABINET", "M", "SERVICED", (82, 45, floor), 180),
    ("CREW_ID_PLATE", "L", "LIVED_IN", (90, 44, floor), 180),
]
site_roots = []
for i, (fam, sz, st, loc, rz) in enumerate(layout):
    site_roots.append(clone_to_site(source(fam, sz, st), f"X100HI_REFUGE_{i:02d}_{fam}", loc, rz))

scene["checkpoint"] = "X100_HABITATION_CULTURE_FOUNDATION_001"
scene["x100_habitation_family_count"] = 10
scene["x100_habitation_library_roots"] = len(roots)
scene["x100_habitation_site_roots"] = len(site_roots)
scene["x100_habitation_states"] = "SERVICED|LIVED_IN|FIELD_REPAIRED"
scene["x100_habitation_sizes"] = "S|M|L"
scene["x100_habitation_status"] = "SYSTEMIC_FOUNDATION_NOT_FAMILY_COMPLETE"
scene["x100_habitation_culture_contract"] = "daily survival identity through fabrication/repair/ergonomics; no invented religion/lore text"
scene["x100_refuge_primary_corridor"] = "central x~72/y~35 protected; domestic layout kept to perimeter rows"
