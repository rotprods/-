"""EXOVANT 2950 / UMBRA / X100 causal material-history foundation.

Precondition: UMBRA X100 service/site/history/habitation foundations already exist.
Checkpoint: X100_MATERIAL_CAUSALITY_FOUNDATION_001.

Creates portable whole-object Principled material-state variants and applies them only
to site-integrated X100 objects from semantic parent/root context. Catalog libraries
remain neutral. This is deliberately NOT final PBR: directional masks, UV0, texture
sets, texel density and runtime calibration remain blocked by target-engine evidence.
"""

import bpy

scene = bpy.context.scene
if scene.get("x100_material_history_checkpoint"):
    raise RuntimeError("X100 material history already applied")

base_roles = {
    "MAT_SINSOL_DARK_METAL": "METAL",
    "MAT_SINSOL_TENSION_FABRIC": "FABRIC",
    "MAT_COLONIAL_IVORY_REPAIR": "IVORY_REPAIR",
    "MAT_SINSOL_THERMAL_COPPER": "THERMAL_COPPER",
    "MAT_SINSOL_GASKET": "GASKET",
    "MAT_SINSOL_THERMAL_CERAMIC": "THERMAL_CERAMIC",
}
states = ["COLD_ABRADED", "THERMAL_CYCLED", "SERVICE_RENEWED", "FIELD_REPAIRED"]


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def bsdf(mat):
    if not mat.use_nodes:
        mat.use_nodes = True
    return mat.node_tree.nodes.get("Principled BSDF")


def values(base, state):
    b = bsdf(base)
    col = list(b.inputs["Base Color"].default_value)
    rough = float(b.inputs["Roughness"].default_value)
    metal = float(b.inputs["Metallic"].default_value)

    if state == "COLD_ABRADED":
        col = [clamp(c * 1.06 + 0.015) for c in col[:3]] + [1.0]
        rough = clamp(rough - 0.08, 0.18, 0.92)
    elif state == "THERMAL_CYCLED":
        col = [clamp(c * 0.82) for c in col[:3]] + [1.0]
        rough = clamp(rough + 0.12, 0.18, 0.96)
        metal = clamp(metal * 0.96)
    elif state == "SERVICE_RENEWED":
        col = [clamp(c * 1.03 + 0.01) for c in col[:3]] + [1.0]
        rough = clamp(rough - 0.12, 0.14, 0.88)
    elif state == "FIELD_REPAIRED":
        col = [clamp(c * 0.92 + 0.055) for c in col[:3]] + [1.0]
        rough = clamp(rough + 0.08, 0.20, 0.96)
    return col, rough, metal


causal_contract = {
    "COLD_ABRADED": "windborne ice/dust exposure; whole-object proxy for later directional mask",
    "THERMAL_CYCLED": "repeated cold/heat service cycles; darker/rougher response",
    "SERVICE_RENEWED": "recent cleaning/replacement/service; tighter material response",
    "FIELD_REPAIRED": "scarcity-driven mismatched repair/replacement; rougher/lighter proxy",
}

variants = {}
for base_name, role in base_roles.items():
    base = bpy.data.materials.get(base_name)
    if base is None:
        continue
    for state in states:
        name = f"{base_name}__X100_{state}"
        mat = bpy.data.materials.get(name)
        if mat is None:
            mat = base.copy()
            mat.name = name
        b = bsdf(mat)
        col, rough, metal = values(base, state)
        b.inputs["Base Color"].default_value = col
        b.inputs["Roughness"].default_value = rough
        b.inputs["Metallic"].default_value = metal
        mat["x100_material_role"] = role
        mat["x100_causal_state"] = state
        mat["epistemic"] = "PORTABLE_MATERIAL_HISTORY_FOUNDATION_NOT_FINAL_PBR"
        mat["causal_contract"] = causal_contract[state]
        variants[(base_name, state)] = mat


def root_context(obj):
    current = obj
    for _ in range(8):
        if current is None:
            break
        if (
            current.get("temporal_layer")
            or current.get("state_variant")
            or current.get("x100_site")
            or current.get("site")
        ):
            return current
        current = current.parent
    return None


def state_for(root):
    if root is None:
        return None
    state = str(root.get("state_variant", ""))
    era = str(root.get("temporal_layer", ""))
    name = root.name.upper()

    if state == "SERVICED":
        return "SERVICE_RENEWED"
    if state == "LIVED_IN":
        return "THERMAL_CYCLED"
    if state == "FIELD_REPAIRED":
        return "FIELD_REPAIRED"
    if "ERA_0" in era:
        return "COLD_ABRADED"
    if "ERA_1" in era:
        return "FIELD_REPAIRED"
    if "ERA_2" in era:
        if any(token in name for token in ("REPAIR", "RENEW", "PATCH")):
            return "SERVICE_RENEWED"
        return "THERMAL_CYCLED"
    return None


site_collection_names = [
    "90_X100_SITE_INTEGRATION",
    "91_X100_SITE_REFUGE_SERVICE",
    "91_X100_SITE_REFLECTOR02",
    "91_X100_SITE_REFLECTOR03",
    "91_X100_SITE_M03_ARCHIVE",
    "91_X100_SITE_CARAVAN_REPAIR_HISTORY",
    "94_X100_REFUGE_HABITATION_ANNEX",
]

site_objects = set()
for name in site_collection_names:
    collection = bpy.data.collections.get(name)
    if collection:
        site_objects.update(collection.objects)

# Include descendants whose semantic parent belongs to one of the bounded site collections.
for obj in list(bpy.data.objects):
    parent = obj.parent
    for _ in range(8):
        if parent is None:
            break
        if parent in site_objects:
            site_objects.add(obj)
            break
        parent = parent.parent

assignments = []
by_state = {state: 0 for state in states}
by_role = {role: 0 for role in base_roles.values()}

for obj in sorted(site_objects, key=lambda item: item.name):
    if obj.type != "MESH" or not obj.material_slots:
        continue
    context = root_context(obj)
    state = state_for(context)
    if state is None:
        continue

    for index, slot in enumerate(obj.material_slots):
        current = slot.material
        if current is None:
            continue
        base_name = current.name.split("__X100_")[0]
        if base_name not in base_roles:
            continue
        target = variants.get((base_name, state))
        if target is None:
            continue

        # Object-level material override preserves shared mesh datablocks.
        slot.link = "OBJECT"
        slot.material = target
        assignments.append((obj.name, index, base_name, state, context.name if context else ""))
        by_state[state] += 1
        by_role[base_roles[base_name]] += 1
        obj["x100_material_state"] = state
        obj["x100_material_context_root"] = context.name if context else ""

scene["x100_material_history_checkpoint"] = "X100_MATERIAL_CAUSALITY_FOUNDATION_001"
scene["checkpoint"] = "X100_MATERIAL_CAUSALITY_FOUNDATION_001"
scene["x100_material_history_variant_count"] = len(variants)
scene["x100_material_history_assignments"] = len(assignments)
scene["x100_material_history_scope"] = "site-integrated X100 objects only; catalogs remain neutral; final directional masks/UV/PBR blocked by runtime target"
scene["x100_material_history_states"] = "COLD_ABRADED|THERMAL_CYCLED|SERVICE_RENEWED|FIELD_REPAIRED"

bpy.context.view_layer.update()
