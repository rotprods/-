#!/usr/bin/env python3
"""Generate the canonical target asset registry for the VANTA art cell.

Rows are production targets, not completion claims. This script is intentionally
stdlib-only so a cold clone can regenerate CSV/JSON without Blender.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

OWNER_BRANCH = "art/world-vanta-001"
WORLD = "vanta"
OUT_DIR = Path(__file__).resolve().parents[1] / "registry"

FIELDS = [
    "id", "category", "subsystem", "region", "name", "kind", "hero_tier",
    "scale_m", "material_family", "lod_strategy", "collision", "rig",
    "animation", "uv", "textures", "target_instances", "priority", "status",
    "dod_gate", "owner_branch"
]

rows: list[dict[str, str]] = []


def add(asset_id: str, category: str, subsystem: str, region: str, name: str,
        kind: str = "static_mesh", hero_tier: str = "B", scale_m: str = "TBD",
        material_family: str = "industrial", lod_strategy: str = "LOD0-3",
        collision: str = "simple", rig: str = "none", animation: str = "none",
        uv: str = "trim_or_atlas", textures: str = "PBR", target_instances: str = "1",
        priority: str = "P2", status: str = "PLANNED", dod_gate: str = "STATIC_DOD") -> None:
    rows.append({
        "id": asset_id,
        "category": category,
        "subsystem": subsystem,
        "region": region,
        "name": name,
        "kind": kind,
        "hero_tier": hero_tier,
        "scale_m": scale_m,
        "material_family": material_family,
        "lod_strategy": lod_strategy,
        "collision": collision,
        "rig": rig,
        "animation": animation,
        "uv": uv,
        "textures": textures,
        "target_instances": target_instances,
        "priority": priority,
        "status": status,
        "dod_gate": dod_gate,
        "owner_branch": OWNER_BRANCH,
    })


# ---------------------------------------------------------------------------
# ENVIRONMENT — 84
# ---------------------------------------------------------------------------
for x in range(6):
    for y in range(6):
        add(
            f"VAN_ENV_TERRAIN_CELL_{x:02d}_{y:02d}", "environment", "terrain",
            "district", f"Terrain Cell {x:02d}-{y:02d}", "terrain_cell", "C",
            "4000x4000", "ground_oxide", "HLOD_CELL", "heightfield_or_proxy",
            uv="tiling", target_instances="1", priority="P1",
            status="BLOCKOUT", dod_gate="ENVIRONMENT_DOD"
        )

PORT = [
    "UNION_HALL", "WORKSHOP_A", "WORKSHOP_B", "WORKSHOP_C", "CANTINA",
    "INFIRMARY", "SUPPLY_DEPOT", "DOCK_DECK", "DOCK_RIB", "CRANE_MAST",
    "CRANE_ARM", "CRANE_CAB", "CARGO_LIFT", "REFUGE_A", "REFUGE_B",
    "STRIKE_BARRICADE", "MEDICINE_LOCKER", "PORT_BEACON"
]
for n in PORT:
    tier = "A" if n in {"UNION_HALL", "DOCK_DECK", "CRANE_MAST", "CRANE_ARM"} else "B"
    add(f"VAN_ENV_PORT_{n}", "environment", "port_of_hands", "port_of_hands", n,
        hero_tier=tier, priority="P1", status="BLOCKOUT" if n in {"UNION_HALL", "DOCK_DECK", "DOCK_RIB", "CRANE_MAST", "CRANE_ARM"} else "PLANNED",
        dod_gate="ENVIRONMENT_DOD")

RAIN = [
    "RAILBED", "SLEEPER", "MAG_ARCH", "FIELD_CORE", "STORM_BEACON",
    "SCRAP_BANK_A", "SCRAP_BANK_B", "SCRAP_BANK_C", "ANCHOR_PAD",
    "CABLE_TRENCH", "SCRAP_CHUTE", "SHELTER_RIB", "WEATHER_MAST", "MAGNETIC_GATE"
]
for n in RAIN:
    add(f"VAN_ENV_RAIN_{n}", "environment", "iron_rain", "iron_rain", n,
        hero_tier="A" if n in {"MAG_ARCH", "FIELD_CORE", "STORM_BEACON"} else "B",
        material_family="magnetic_infrastructure" if "MAG" in n or "FIELD" in n else "industrial",
        priority="P1", status="BLOCKOUT" if n in {"RAILBED", "SLEEPER", "MAG_ARCH", "FIELD_CORE", "STORM_BEACON", "SCRAP_BANK_A"} else "PLANNED",
        dod_gate="ENVIRONMENT_DOD")

RING = [
    "DRYDOCK_SPINE", "HULL_RIB_L", "HULL_RIB_R", "RIB_BRIDGE", "MAGNET_TOWER",
    "MAGNET_COIL", "SHIP_HULL_A", "SHIP_HULL_B", "TUG_GRAVE_A", "TUG_GRAVE_B",
    "GANTRY_A", "GANTRY_B", "CONTROL_NODE", "MEMORY_CASK", "POLARITY_SWITCH", "ANCHOR_STATION"
]
for n in RING:
    add(f"VAN_ENV_RING_{n}", "environment", "fallen_ring", "fallen_ring", n,
        hero_tier="A" if n in {"DRYDOCK_SPINE", "MAGNET_TOWER", "MEMORY_CASK"} else "B",
        material_family="magnetic_infrastructure" if "MAGNET" in n or "POLARITY" in n else "industrial",
        priority="P1", status="BLOCKOUT" if n in {"DRYDOCK_SPINE", "HULL_RIB_L", "HULL_RIB_R", "RIB_BRIDGE", "MAGNET_TOWER", "MAGNET_COIL"} else "PLANNED",
        dod_gate="ENVIRONMENT_DOD")

# ---------------------------------------------------------------------------
# MODULAR CONSTRUCTION KIT — 61
# ---------------------------------------------------------------------------
MODULAR = [
    "beam_I_1m", "beam_I_2m", "beam_I_4m", "beam_I_8m", "pipe_050", "pipe_100", "pipe_200",
    "pipe_elbow_050", "pipe_elbow_100", "pipe_T_100", "catwalk_2m", "catwalk_4m",
    "catwalk_corner", "catwalk_stairs", "ladder_2m", "ladder_4m", "railing_1m", "railing_2m",
    "railing_corner", "wall_panel_A", "wall_panel_B", "wall_panel_C", "floor_plate_A",
    "floor_grate_A", "floor_grate_B", "ceiling_panel_A", "door_worker", "door_airlock", "door_cargo",
    "window_small", "window_strip", "vent_small", "vent_large", "fan_industrial", "cable_bundle_S",
    "cable_bundle_M", "cable_bundle_L", "chain_S", "chain_M", "chain_L", "hook_S", "hook_L", "winch",
    "pulley", "bolted_plate_A", "bolted_plate_B", "gusset_A", "gusset_B", "hatch_round", "hatch_rect",
    "service_box", "junction_box", "transformer_box", "magnet_block_S", "magnet_block_M", "magnet_block_L",
    "coil_S", "coil_M", "coil_L", "anchor_clamp", "track_switch"
]
for n in MODULAR:
    add(f"VAN_KIT_{n.upper()}", "modular_kit", "construction_kit", "shared_vanta", n,
        hero_tier="B", material_family="industrial", target_instances="many", priority="P1",
        dod_gate="MODULAR_DOD")

# ---------------------------------------------------------------------------
# PROPS / DRESSING — 61
# ---------------------------------------------------------------------------
PROPS = [
    "cargo_container_A", "cargo_container_B", "cargo_container_C", "tool_cart", "welding_cart", "gas_bottle",
    "parts_bin", "scrap_pallet", "worker_locker", "bench", "canteen_table", "canteen_stool", "medical_case",
    "supply_crate", "medicine_crate", "water_tank", "coolant_tank", "lubricant_drum", "cable_reel", "chain_reel",
    "magnet_clamp", "torque_tool", "plasma_cutter", "welding_mask", "helmet_worker", "helmet_pilot", "union_flag",
    "union_banner", "strike_sign", "shift_board", "time_clock", "manifest_terminal", "dock_terminal",
    "handheld_scanner", "radio_unit", "portable_light", "warning_cone", "barrier", "bollard", "fire_suppression",
    "first_aid_station", "stretcher", "sleep_pod", "heater", "coffee_unit", "food_tray", "personal_photo_frame",
    "memorial_tag", "lost_ship_plate", "evacuation_marker", "cargo_label_set", "serial_plate_set", "rivets_set",
    "bolts_set", "weld_decal_set", "oil_leak_decal", "rust_streak_decal", "impact_decal", "frost_decal",
    "magnetic_dust_decal", "worker_graffiti_set"
]
for n in PROPS:
    is_decal_prop = "decal" in n or "graffiti" in n or "label" in n or "plate_set" in n
    add(f"VAN_PROP_{n.upper()}", "props", "set_dressing", "shared_vanta", n,
        kind="decal_or_prop" if is_decal_prop else "static_mesh", hero_tier="C" if is_decal_prop else "B",
        collision="none" if is_decal_prop else "simple", target_instances="many", priority="P2",
        dod_gate="PROP_DOD")

# ---------------------------------------------------------------------------
# CHARACTERS / ENEMIES / BOSS — 7
# ---------------------------------------------------------------------------
CHARACTERS = [
    ("NPC_MIKA_DRAV", "Mika Drav", "npc", "A"),
    ("NPC_CIRO_FENN", "Ciro Fenn", "npc", "A"),
    ("NPC_BEL_ORTA", "Bel Orta", "npc", "A"),
    ("ENEMY_COLLECTOR", "Cobrador de astillero", "enemy", "A"),
    ("ENEMY_RIVET_SWARM", "Enjambre de remaches", "enemy_swarm", "B"),
    ("ENEMY_AUTO_TUG", "Remolcador automatizado", "enemy_vehicle", "A"),
    ("BOSS_FERRUM", "FERRUM, coloso de chatarra", "boss", "S"),
]
for aid, name, kind, tier in CHARACTERS:
    is_boss = aid == "BOSS_FERRUM"
    add(f"VAN_{aid}", "characters", kind, "fallen_ring" if is_boss else "shared_vanta", name,
        kind="skinned_mesh" if kind in {"npc", "enemy", "boss"} else "multi_part_actor",
        hero_tier=tier, uv="unique", textures="unique_PBR", collision="capsule_plus_hitboxes" if kind in {"npc", "enemy", "boss"} else "multi_shape",
        rig="required", animation="required", priority="P0" if is_boss else "P1",
        status="BLOCKOUT", dod_gate="BOSS_DOD" if is_boss else "CHARACTER_DOD")

# ---------------------------------------------------------------------------
# BIOTA — 4
# ---------------------------------------------------------------------------
BIOTA = [
    ("MAG_LITHOPHAGE", "Litófago magnético", "crawler"),
    ("FILINGS_RAY", "Raya de limaduras", "glider"),
    ("RIVET_CROW", "Cuervo de remache", "avian"),
    ("SLAG_BIOFILM", "Bacteria de escoria", "surface_ecology"),
]
for aid, name, kind in BIOTA:
    surface = aid == "SLAG_BIOFILM"
    add(f"VAN_BIOTA_{aid}", "biota", kind, "shared_vanta", name,
        kind="instanced_surface" if surface else "skinned_mesh", hero_tier="B",
        collision="none" if surface else "simple_or_capsule", rig="none" if surface else "required",
        animation="shader_or_state" if surface else "required", uv="tiling" if surface else "unique",
        target_instances="many", priority="P2", status="BLOCKOUT", dod_gate="BIOTA_DOD")

# ---------------------------------------------------------------------------
# VEHICLE — 1
# ---------------------------------------------------------------------------
add("VAN_VEH_DRAV_TUG", "vehicles", "heavy_tug", "shared_vanta", "Remolcador Drav",
    kind="rigged_vehicle", hero_tier="S", scale_m="22x8.5xTBD", material_family="industrial_vehicle",
    collision="multi_shape", rig="required", animation="thrusters_clamp_doors", uv="unique",
    textures="unique_PBR", priority="P1", status="BLOCKOUT", dod_gate="VEHICLE_DOD")

# ---------------------------------------------------------------------------
# FERRUM PART BREAKDOWN — 43
# ---------------------------------------------------------------------------
FERRUM_PARTS = [
    "pelvis_carriage", "polarity_core", "torso_main", "torso_armor_L", "torso_armor_R", "memory_cabin", "sensor_head",
    "leg_upper_LF", "leg_upper_RF", "leg_upper_LR", "leg_upper_RR", "shin_LF", "shin_RF", "shin_LR", "shin_RR",
    "foot_LF", "foot_RF", "foot_LR", "foot_RR", "shoulder_girder", "arm_L_upper", "arm_L_joint", "hammer_handle",
    "hammer_quill", "arm_R_upper", "arm_R_joint", "claw_forearm", "claw_tine_A", "claw_tine_B", "claw_tine_C",
    "torso_coil_A", "torso_coil_B", "torso_coil_C", "cable_set", "hydraulic_set", "armor_scrap_set", "memory_window_set",
    "sensor_cluster", "anchor_socket_set", "damage_state_01", "damage_state_02", "damage_state_03", "wreck_state"
]
for n in FERRUM_PARTS:
    interactive = any(k in n for k in ["core", "cabin", "joint", "hammer", "claw", "foot", "socket", "sensor"])
    add(f"VAN_FERRUM_{n.upper()}", "boss_parts", "ferrum", "ferrum_arena", n,
        kind="mechanical_part", hero_tier="S", material_family="ferrum_hero", lod_strategy="BOSS_LOD",
        collision="part_hitbox" if interactive else "simple", rig="socketed", animation="boss_rig",
        uv="unique_or_trim", textures="hero_PBR", priority="P0", status="BLOCKOUT", dod_gate="BOSS_PART_DOD")

# ---------------------------------------------------------------------------
# VFX — 20
# ---------------------------------------------------------------------------
VFX = [
    "metal_rain_far", "metal_rain_mid", "metal_rain_near", "magnetic_field_volume", "magnetic_field_arcs",
    "scrap_attraction", "scrap_repulsion", "polarity_warning", "anchor_lock", "ferrum_core_glow",
    "ferrum_pressure_sparks", "welding_sparks", "grinder_sparks", "dust_gust", "ferrous_dust_alignment",
    "cold_breath", "frost_vent", "thruster_exhaust", "impact_metal", "boss_scrap_assembly"
]
for n in VFX:
    add(f"VAN_VFX_{n.upper()}", "vfx", "weather_magnetism_industry", "shared_vanta", n,
        kind="vfx_system", hero_tier="B", lod_strategy="VFX_DISTANCE_TIER", collision="none", rig="none",
        animation="system", uv="n/a", textures="vfx_atlas", target_instances="bounded", priority="P1",
        dod_gate="VFX_DOD")

# ---------------------------------------------------------------------------
# MATERIAL MASTERS — 16
# ---------------------------------------------------------------------------
MATERIALS = [
    "ground_oxide", "slag_black", "rolled_steel", "rust_ferric", "union_yellow_paint", "magnet_coil",
    "field_emissive", "warning_red", "smoked_glass", "softgoods_worker", "ceramic_medical", "rubber_cable",
    "lubricant_wet", "frost_ice", "biofilm_slag", "ferrous_dust"
]
for n in MATERIALS:
    add(f"VAN_MAT_{n.upper()}", "materials", "material_master", "shared_vanta", n,
        kind="material", hero_tier="A", lod_strategy="shader_lod", collision="none", uv="n/a",
        textures="PBR_master", target_instances="many", priority="P1", dod_gate="MATERIAL_DOD")

# ---------------------------------------------------------------------------
# DECALS — 30
# ---------------------------------------------------------------------------
DECALS = [
    "dock_numbers", "shift_numbers", "union_marks", "hazard_magnetic", "hazard_metal_rain", "hazard_crush",
    "hazard_pressure", "escape_routes", "medical_wayfinding", "supply_wayfinding", "ferrum_warning",
    "polarity_sector_A", "polarity_sector_B", "polarity_sector_C", "polarity_sector_D", "worker_memorial",
    "ship_registry", "lost_cargo_registry", "strike_messages", "cooperative_marks", "corporate_marks",
    "free_port_marks", "maintenance_symbols", "floor_chevrons", "crane_load_limits", "anchor_status",
    "storm_status", "restricted_zone", "airlock_state", "evacuation_state"
]
for n in DECALS:
    add(f"VAN_DECAL_{n.upper()}", "decals", "signage_state", "shared_vanta", n,
        kind="decal", hero_tier="C", lod_strategy="distance_fade", collision="none", uv="atlas",
        textures="decal_atlas", target_instances="many", priority="P2", dod_gate="DECAL_DOD")


def validate() -> dict:
    ids = [r["id"] for r in rows]
    duplicates = sorted(k for k, v in Counter(ids).items() if v > 1)
    category_counts = Counter(r["category"] for r in rows)
    expected = {
        "environment": 84,
        "modular_kit": 61,
        "props": 61,
        "characters": 7,
        "biota": 4,
        "vehicles": 1,
        "boss_parts": 43,
        "vfx": 20,
        "materials": 16,
        "decals": 30,
    }
    assert len(rows) == 327, f"Expected 327 target rows, got {len(rows)}"
    assert not duplicates, f"Duplicate asset IDs: {duplicates}"
    assert dict(category_counts) == expected, (dict(category_counts), expected)
    assert all(r["owner_branch"] == OWNER_BRANCH for r in rows)
    return {
        "world": WORLD,
        "owner_branch": OWNER_BRANCH,
        "row_count": len(rows),
        "category_counts": expected,
        "note": "Targets only. A row is not produced until its DoD gate passes with evidence."
    }


def main() -> None:
    summary = validate()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUT_DIR / "vanta_asset_registry.csv"
    json_path = OUT_DIR / "vanta_asset_registry.json"
    summary_path = OUT_DIR / "vanta_asset_registry.summary.json"

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
