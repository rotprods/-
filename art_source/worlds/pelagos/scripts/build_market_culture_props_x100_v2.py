"""PEL/CIV/PROP-X100-006 — deterministic authoring contract.

Authoritative scene checkpoints:
  west batch -> rev39
  east batch -> rev40
  grounding correction -> rev41

The 3D worker has a 300 s hard deadline, so this generator is intentionally staged.
Do not collapse WEST+EAST into one mutation on the current World Master: the monolithic
attempt timed out cleanly at rev38 without committing.
"""

CLAIM_ID = "PEL/CIV/PROP-X100-006"
COLLECTION = "16_MERCADO_CULTURE_X100_V2"
STATES = ("pristine", "used", "damaged_repaired", "abandoned")
VARIANTS = ("compact", "standard", "communal")
DIRECT_CONFIGURATIONS = 12 * len(STATES) * len(VARIANTS)  # 144
DECK_Z = 13.5
COLLISION_POLICY = "query_only_until_gameplay_binding"

FAMILIES = {
    "WORK":   dict(asset_id="PEL-PROP-WET-WORK-STATION-002", purpose="wet_work_surface_and_seating", position=(-553.5,-101.0,13.5), current="used", variant="standard"),
    "TOOLS":  dict(asset_id="PEL-PROP-TETHERED-TOOL-CADDY-002", purpose="tethered_hand_tools", position=(-553.5,-93.0,13.41), current="used", variant="compact"),
    "DRYBOX": dict(asset_id="PEL-PROP-DRY-LOCKBOX-002", purpose="dry_personal_lockbox", position=(-553.5,-85.0,13.32), current="pristine", variant="compact"),
    "MESS":   dict(asset_id="PEL-PROP-MESS-VESSEL-SET-002", purpose="food_water_service_vessels", position=(-553.5,-77.0,13.4525), current="used", variant="standard"),
    "MED":    dict(asset_id="PEL-PROP-MEDICAL-WETKIT-002", purpose="wet_first_aid_medical_kit", position=(-553.5,-69.0,13.32), current="damaged_repaired", variant="compact"),
    "TRADE2": dict(asset_id="PEL-PROP-TRADE-MEASURE-002", purpose="trade_measurement_exchange", position=(-553.5,-61.0,13.45), current="used", variant="standard"),
    "LAMP":   dict(asset_id="PEL-PROP-REFUGE-LAMP-002", purpose="portable_refuge_lighting", position=(-486.5,-109.0,13.45), current="pristine", variant="compact"),
    "TEXTILE":dict(asset_id="PEL-PROP-TEXTILE-REPAIR-FRAME-002", purpose="textile_drying_repair", position=(-486.5,-101.0,13.225), current="used", variant="communal"),
    "WASTE":  dict(asset_id="PEL-PROP-WASTE-SORTER-002", purpose="waste_sorting_biosafe_disposal", position=(-486.5,-93.0,13.5), current="damaged_repaired", variant="standard"),
    "STORM":  dict(asset_id="PEL-PROP-STORM-STOWAGE-002", purpose="weather_screen_storm_stowage", position=(-486.5,-85.0,13.455), current="damaged_repaired", variant="communal"),
    "NAV":    dict(asset_id="PEL-PROP-NAV-ACOUSTIC-MARKER-002", purpose="portable_navigation_acoustic_marker", position=(-486.5,-77.0,13.5), current="used", variant="standard"),
    "GOODS":  dict(asset_id="PEL-PROP-GOODS-BIN-002", purpose="market_display_modular_goods_bin", position=(-486.5,-69.0,13.46), current="used", variant="communal"),
}

WEST = ("WORK", "TOOLS", "DRYBOX", "MESS", "MED", "TRADE2")
EAST = ("LAMP", "TEXTILE", "WASTE", "STORM", "NAV", "GOODS")

# Durable geometry contract — implementations may change topology while preserving these roles.
PART_ROLES = {
    "WORK": ("drained_wet_work_surface", "wet_perch", "tether_rail", "service_legs"),
    "TOOLS": ("tool_tray", "glove_handle", "tethered_tools"),
    "DRYBOX": ("sealed_body", "service_lid", "gasket", "latch", "wet_feet"),
    "MESS": ("drained_rack", "service_vessels", "grip_geometry"),
    "MED": ("sealed_case", "gasket", "grab_handle", "field_repair_surface"),
    "TRADE2": ("measure_base", "balance_pivot", "beam", "pans", "weights"),
    "LAMP": ("wet_base", "protected_light_core", "cage", "grab_ring"),
    "TEXTILE": ("repair_frame", "drying_textiles", "repair_tray"),
    "WASTE": ("sorted_bins", "sealed_lids", "wet_feet", "tether_rail"),
    "STORM": ("storm_screen_roll", "frame", "restraint_straps", "anchors"),
    "NAV": ("portable_base", "mast", "acoustic_resonator", "beacon"),
    "GOODS": ("drained_pallet", "modular_bins", "restraint_bar"),
}

GROUNDING_OFFSETS_FROM_INITIAL_BUILD = {
    "TOOLS": -0.090, "DRYBOX": -0.180, "MESS": -0.0475, "MED": -0.180,
    "TRADE2": -0.050, "LAMP": -0.050, "TEXTILE": -0.275,
    "STORM": -0.045, "GOODS": -0.040,
}

QA_CONTRACT = {
    "families": 12,
    "state_roots": 48,
    "one_visible_state_per_family": True,
    "one_current_state_marker_per_family": True,
    "lod1_roots": 12,
    "visible_tech": 0,
    "missing_uv": 0,
    "missing_materials": 0,
    "nonunit_visible_mesh_scales": 0,
    "command_shell_hits": 0,
    "physical_family_overlaps": 0,
    "platform_overflow": 0,
    "ground_tolerance_m": 0.031,
}

if __name__ == "__main__":
    raise SystemExit(
        "This file is the deterministic replay/spec contract. Execute WEST then EAST as bounded "
        "3D-worker mutations, apply GROUNDING_OFFSETS_FROM_INITIAL_BUILD, then enforce QA_CONTRACT."
    )
