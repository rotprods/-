"""SYLVA PRIME r7 — consumer-side root-kit socket contract.

Claim: CLM-SYLVA-MACRO-001
Provider: CLM-SYLVA-PROC-NROOT-001 / PR #6

This pass deliberately DOES NOT instantiate or copy provider root-kit geometry.
It freezes the consumer basis and records the provider-pivot blocker discovered by
read-only inspection of the provider Blender r4 scene.
"""
from __future__ import annotations

import bpy

CLAIM = "CLM-SYLVA-MACRO-001"
PROVIDER = "CLM-SYLVA-PROC-NROOT-001"
MANIFEST = "production/manifests/sylva/procedural/SYL_NEURAL_ROOT_KIT_001.yaml"
PR6_BLOCKER_COMMENT = "5648741376"
CONTRACT_VERSION = "SYLVA_SOCKET_CONSUMER_V1"


def apply() -> dict:
    meta_col = bpy.data.collections.get("SYLVA_00_META")
    if meta_col is None:
        raise RuntimeError("SYLVA_00_META missing")

    contract = bpy.data.objects.get("SYLVA_META_RootKitSocketConsumerContract")
    if contract is None:
        contract = bpy.data.objects.new("SYLVA_META_RootKitSocketConsumerContract", None)
        meta_col.objects.link(contract)
    contract.empty_display_type = "ARROWS"
    contract.empty_display_size = 40
    contract["classification"] = "INTERFACE_CONTRACT"
    contract["owner_claim"] = CLAIM
    contract["provider_claim"] = PROVIDER
    contract["provider_manifest"] = MANIFEST
    contract["consumer_forward_axis"] = "+X"
    contract["consumer_up_axis"] = "+Z"
    contract["consumer_units"] = "metres"
    contract["consumer_scale_contract"] = "1,1,1"
    contract["provider_pivot_status"] = "BLOCKED_PROVIDER_NORMALIZATION_REQUIRED"
    contract["provider_pivot_receipt_pr6_comment"] = PR6_BLOCKER_COMMENT
    contract["provider_geometry_copy_allowed"] = False
    contract["socket_transform_mutation_allowed_without_provider_contract"] = False

    sockets = sorted(
        (o for o in bpy.data.objects if o.name.startswith("SYLVA_SOCKET_")),
        key=lambda o: o.name,
    )
    for socket in sockets:
        socket["consumer_contract_version"] = CONTRACT_VERSION
        socket["consumer_forward_axis"] = "+X"
        socket["consumer_up_axis"] = "+Z"
        socket["consumer_units"] = "metres"
        socket["consumer_scale"] = "1,1,1"
        socket["provider_pivot_status"] = "BLOCKED_PROVIDER_NORMALIZATION_REQUIRED"
        socket["provider_pivot_receipt_pr6_comment"] = PR6_BLOCKER_COMMENT
        socket["provider_instance_status"] = "NOT_INSTANTIATED"
        socket["provider_geometry_copy_allowed"] = False
        socket["final_transform_locked_pending_provider_pivot"] = True

    root = bpy.data.objects.get("SYLVA_WORLD_ROOT")
    if root:
        root["build_status"] = "WAVE1E_SOCKET_CONSUMER_CONTRACT_R7"
        root["rootkit_provider_pivot_status"] = "BLOCKED_PROVIDER_NORMALIZATION_REQUIRED"
        root["rootkit_provider_pr6_comment"] = PR6_BLOCKER_COMMENT
        root["rootkit_socket_contract_version"] = CONTRACT_VERSION

    return {
        "socket_count": len(sockets),
        "consumer_basis": {"forward": "+X", "up": "+Z", "units": "metres", "scale": [1, 1, 1]},
        "provider_pivot_status": "BLOCKED_PROVIDER_NORMALIZATION_REQUIRED",
        "provider_instances_created": 0,
    }


if __name__ == "__main__":
    result = apply()
    print(result)
