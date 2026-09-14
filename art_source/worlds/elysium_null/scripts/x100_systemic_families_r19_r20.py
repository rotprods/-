"""EXOVANT-X100 reproducibility contract for ELYSIUM R19/R20.

The committed Blender World Master contains the executed geometry at revisions 19/20.
This source records the deterministic semantic axes and validation formulas used by
those passes. It intentionally avoids network access and never promotes proposals to canon.

For full scene reconstruction run the earlier foundation/W1 scripts first, then use this
module's constants/helpers when rebuilding the domestic and maintenance-root families.
"""

from itertools import product, combinations

WORLD = "ELYSIUM NULL"
DOMESTIC_PRIMARY_BAY_M = 4.0
DOMESTIC_ROOM_M = (8.0, 8.0, 3.2)
PLAYER_CAPSULE_M = (0.76, 1.85)
DOMESTIC_DOOR_CLEAR_M = (2.2, 2.72)

WALL_TYPES = ("SOLID", "WINDOW", "SERVICE", "STORAGE", "NICHE")
FURNITURE_TYPES = ("REST", "WORK", "LOUNGE", "STORAGE", "HORTI", "CRAFT")
DOMESTIC_PROFILES = {
    "CONTEMPLATIVE": ("REST", "STORAGE", "LOUNGE"),
    "SOCIAL": ("LOUNGE", "WORK", "STORAGE"),
    "MAKER": ("WORK", "CRAFT", "STORAGE"),
    "HORTICULTURAL": ("HORTI", "WORK", "REST"),
}
TEMPORAL_STATES = ("PRISTINE", "OCCUPIED", "REPAIRED", "ABANDONED")
LIGHTING_MODES = ("AMBIENT", "TASK", "GUIDE")
CLIMATE_MODES = ("SEALED", "OPEN")


def valid_wall_configurations():
    out = []
    for seq in product(WALL_TYPES, repeat=3):
        if "SERVICE" not in seq:
            continue
        if seq.count("WINDOW") > 2:
            continue
        if len(set(seq)) == 1:
            continue
        out.append(seq)
    return out


def domestic_combinatorics():
    walls = valid_wall_configurations()
    furniture_sets = list(combinations(FURNITURE_TYPES, 3))
    conservative = len(walls) * len(furniture_sets) * len(DOMESTIC_PROFILES) * len(TEMPORAL_STATES)
    full = conservative * len(LIGHTING_MODES) * len(CLIMATE_MODES)
    return {
        "valid_wall_configs": len(walls),
        "furniture_sets": len(furniture_sets),
        "credible_lower_bound": conservative,
        "full_recombination_bound": full,
    }

ROOT_SIZES = ("SMALL", "MEDIUM", "LARGE")
ROOT_STATES = ("PRISTINE", "ACTIVE", "REPAIRED", "DEGRADED")
ROOT_ROUTES = ("DIRECT", "BRANCHED", "RING")
ROOT_ATTACHMENTS = ("GARDEN", "SERVICE_WALL", "NUTRIENT_SPINE", "FLOOR_HATCH")


def maintenance_root_combinatorics():
    return len(ROOT_SIZES) * len(ROOT_STATES) * len(ROOT_ROUTES) * len(ROOT_ATTACHMENTS)


def validation_receipt():
    return {
        "world": WORLD,
        "domestic": domestic_combinatorics(),
        "maintenance_root_configurations": maintenance_root_combinatorics(),
        "door_width_slack_m": DOMESTIC_DOOR_CLEAR_M[0] - PLAYER_CAPSULE_M[0],
        "door_height_slack_m": DOMESTIC_DOOR_CLEAR_M[1] - PLAYER_CAPSULE_M[1],
        "anti_slop_rule": "variation must be semantic/causal; random cosmetic noise is invalid",
    }


if __name__ == "__main__":
    print(validation_receipt())
