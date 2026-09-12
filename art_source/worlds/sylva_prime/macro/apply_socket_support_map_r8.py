"""SYLVA PRIME r8 — semantic support map for root-kit consumer sockets.

This pass assigns intended support objects/roles but deliberately does NOT snap transforms.
Provider pivot normalization and art review are prerequisites for final placement.
"""
from __future__ import annotations

import bpy

SUPPORT_MAP = {
    "SYLVA_SOCKET_PUERTO_EXIT_A1": ("SYLVA_ROOT_PRIMARY_R01", "TRAVERSABLE_NETWORK_EXIT"),
    "SYLVA_SOCKET_PUERTO_MEMBRANE_C3": ("SYLVA_PUERTO_LivingArch_B", "MEMBRANE_ATTACHMENT_ON_LIVING_ARCH"),
    "SYLVA_SOCKET_BOSQUE_APPROACH_A2": ("SYLVA_ROOT_PRIMARY_R02", "TRAVERSABLE_NETWORK_APPROACH"),
    "SYLVA_SOCKET_BOSQUE_FORK_B1": ("SYLVA_ROOT_SECONDARY_03", "TRAVERSABLE_JUNCTION_BRANCH"),
    "SYLVA_SOCKET_BOSQUE_RISE_A3": ("SYLVA_ROOT_PRIMARY_R02", "TRAVERSABLE_RISE_BRANCH"),
    "SYLVA_SOCKET_VESPER_APPROACH_A2": ("SYLVA_ROOT_PRIMARY_R03", "TRAVERSABLE_VESPER_APPROACH"),
    "SYLVA_SOCKET_VESPER_BUTTRESS_C1": ("SYLVA_VESPER_Buttress_02", "STRUCTURAL_BUTTRESS_ATTACHMENT"),
    "SYLVA_SOCKET_VESPER_MEMBRANE_C3": ("SYLVA_ROOT_SECONDARY_07", "MEMBRANE_ATTACHMENT_ON_SECONDARY_ROOT"),
}


def apply() -> dict:
    missing = []
    for socket_name, (support_name, support_role) in SUPPORT_MAP.items():
        socket = bpy.data.objects.get(socket_name)
        support = bpy.data.objects.get(support_name)
        if socket is None or support is None:
            missing.append({"socket": socket_name, "support": support_name})
            continue
        socket["support_object"] = support_name
        socket["support_role"] = support_role
        socket["support_assignment_status"] = "PROPOSAL_EXPLICIT_NOT_SNAPPED"
        socket["support_contact_status"] = "PENDING_PROVIDER_PIVOT_AND_ART_REVIEW"
        socket["transform_frozen"] = True

    meta = bpy.data.objects.get("SYLVA_META_RootKitSocketConsumerContract")
    if meta:
        meta["support_map_version"] = "SYLVA_SOCKET_SUPPORT_MAP_V1"
        meta["support_assignments"] = len(SUPPORT_MAP) - len(missing)
        meta["support_transforms_snapped"] = 0
        meta["support_assignment_truth"] = "PROPOSAL"

    root = bpy.data.objects.get("SYLVA_WORLD_ROOT")
    if root:
        root["rootkit_socket_support_map"] = "SYLVA_SOCKET_SUPPORT_MAP_V1"
        root["rootkit_socket_support_snapped"] = 0

    return {"assigned": len(SUPPORT_MAP) - len(missing), "missing": missing, "snapped_transforms": 0}


if __name__ == "__main__":
    print(apply())
