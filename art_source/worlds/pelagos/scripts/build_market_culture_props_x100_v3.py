"""PEL/CIV/PROP-X100-007 — deterministic floor-closing cultural-prop contract.

Authoritative World Master history:
- WEST batch -> rev42
- EAST batch -> rev43
- transform-only grounding correction -> rev44
- final structural + normalized coverage QA -> rev44

The current 3D worker checkpoints/exports the entire World Master and has a 300 s hard
deadline. Keep this claim staged in WEST/EAST mutations rather than rebuilding all nine
families monolithically.
"""

CLAIM_ID = "PEL/CIV/PROP-X100-007"
COLLECTION = "17_MERCADO_CULTURE_X100_V3"
DECK_Z = 13.5
STATES = ("pristine", "used", "damaged_repaired", "abandoned")
VARIANTS = ("compact", "standard", "communal")
DIRECT_CONFIGURATIONS = 9 * len(STATES) * len(VARIANTS)  # 108
COLLISION_POLICY = "query_only_until_gameplay_binding"

FAMILIES = {
    "REST": dict(asset_id="PEL-PROP-REST-SLING-003", purpose="rest_sling_berth_roll", position=(-548.5,-105.0,13.42), current="used", variant="standard"),
    "RINSE": dict(asset_id="PEL-PROP-RINSE-BASIN-003", purpose="rinse_wash_basin", position=(-548.5,-97.0,13.46), current="used", variant="standard"),
    "SPLICE": dict(asset_id="PEL-PROP-LINE-SPLICE-JIG-003", purpose="line_splicing_jig", position=(-548.5,-89.0,13.5), current="damaged_repaired", variant="standard"),
    "SEAL": dict(asset_id="PEL-PROP-SEALANT-CADDY-003", purpose="sealant_repair_consumables", position=(-548.5,-81.0,13.46), current="used", variant="compact"),
    "SALVAGE": dict(asset_id="PEL-PROP-SALVAGE-SORT-003", purpose="salvage_sorting_tray", position=(-548.5,-73.0,13.5), current="used", variant="communal"),
    "KNEEL": dict(asset_id="PEL-PROP-MAINT-KNEELER-003", purpose="maintenance_kneeler_low_step", position=(-491.5,-105.0,13.5), current="used", variant="compact"),
    "CRADLE": dict(asset_id="PEL-PROP-FRAGILE-CRADLE-003", purpose="fragile_wet_goods_transport_cradle", position=(-491.5,-97.0,13.5), current="used", variant="communal"),
    "SLATE": dict(asset_id="PEL-PROP-WORK-SLATE-003", purpose="waterproof_temporary_work_route_slate", position=(-491.5,-89.0,13.5), current="damaged_repaired", variant="compact"),
    "HARNESS": dict(asset_id="PEL-PROP-TETHER-HARNESS-003", purpose="personal_tether_harness_rack", position=(-491.5,-81.0,13.5), current="used", variant="communal"),
}

WEST = ("REST", "RINSE", "SPLICE", "SEAL", "SALVAGE")
EAST = ("KNEEL", "CRADLE", "SLATE", "HARNESS")
GROUNDING_OFFSETS_FROM_INITIAL_BUILD = {"REST": -0.080, "RINSE": -0.040, "SEAL": -0.040}

CULTURE_DNA = (
    "repair-first marine construction",
    "wet/gloved ergonomics",
    "tethering and drainage",
    "corrosion resistance",
    "low/heavy mass distribution",
    "replaceable parts",
    "storm stowage",
    "causal wear without unsupported faction iconography",
)

QA_CONTRACT = {
    "families": 9,
    "state_roots": 36,
    "one_visible_state_per_family": True,
    "one_current_state_marker_per_family": True,
    "lod1_roots": 9,
    "visible_technical_geometry": 0,
    "missing_uv": 0,
    "missing_materials": 0,
    "nonunit_visible_mesh_scales": 0,
    "platform_overflow": 0,
    "command_shell_hits": 0,
    "inter_family_overlaps": 0,
    "ground_tolerance_m": 0.031,
    "min_route_clearance_target_m": 3.5,
}

NORMALIZED_CULTURAL_FLOOR = {
    "PROP-X100-001": 9,
    "PROP-X100-006": 12,
    "PROP-X100-007": 9,
    "total": 30,
    "planning_floor": 30,
}

if __name__ == "__main__":
    raise SystemExit(
        "Replay/spec contract only. Execute WEST then EAST as bounded 3D-worker mutations, "
        "apply the grounding offsets, enforce QA_CONTRACT, then prove normalized 9+12+9=30."
    )
