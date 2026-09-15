"""Compile one KHEPRI material application key into a systemic source/runtime recipe.

This prevents the 139 application matrix from becoming 139 independent texture sets. The recipe
keeps family base, manufacturing finish, causal state and scale policy explicit. Portable glTF is
currently the verified adapter, so the default output requests a baked BC/MR/N consumer set while
preserving the source StateMask separately.
"""
from __future__ import annotations

import argparse
import json

from compile_application_matrix import compile_matrix

CONTRACT = "KHP_MATERIAL_RECIPE_X100_V1"


def index() -> dict[str, dict]:
    return {row["application_id"]: row for row in compile_matrix()}


def compile_recipe(application_id: str) -> dict:
    rows = index()
    if application_id not in rows:
        raise KeyError(f"unknown or invalid KHEPRI material application: {application_id}")
    row = rows[application_id]
    return {
        "contract": CONTRACT,
        "application_id": application_id,
        "family": row["family"],
        "asset_id": row["asset_id"],
        "source_layers": {
            "family_base": f"{row['asset_id']}::BASE",
            "manufacturing_finish": row["finish"],
            "causal_state": row["state"],
            "causal_mask_role": row["cause"],
            "application_scale": row["scale"],
            "authoring_px_per_m_proposal": row["authoring_px_per_m"],
        },
        "portable_output": {
            "strategy": "BAKE_CONSUMER_BC_MR_N",
            "base_color": True,
            "metallic_roughness": True,
            "normal": True,
            "state_mask": "SOURCE_ONLY",
            "emission": False,
        },
        "engine_native_optimization": {
            "status": "DEFERRED_UNTIL_ENGINE_AND_TARGET_HARDWARE_QUALIFIED",
            "candidates": ["shared_base_tiles", "trim_sheets", "decal_masks", "material_instances", "texture_arrays_if_supported"],
        },
        "forbidden": [
            "unique_texture_set_per_application_by_default",
            "random_grunge",
            "global_edge_wear",
            "unmotivated_emission",
            "atmospheric_corrosion_without_canon",
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("application_id")
    args = parser.parse_args()
    print(json.dumps(compile_recipe(args.application_id), indent=2, sort_keys=True))
