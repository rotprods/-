# AURORA VEIL — CAMP SERVICE ROUTING CONTRACT r19

**Task:** `AUR/PROC/027`  
**Owner:** `AGENT-02-AURORA` / `CLM-AURORA-WORLD-001`  
**Remote proof:** Blender rev 19  
**Status:** `REVIEW_TECHNICAL`; final electrical class, cable bend geometry, engine interaction and human art review remain open.

## Purpose

Convert the Campamento modular proof from disconnected architectural shells into a physically traceable service system. Routing is derived from current asset interfaces, terrain and sockets; it is not decorative spline dressing.

## Foundation/contact prerequisite

Terrain r14 revealed that the r10/r15 proof assembly had not been re-grounded. r18 attempted a fix but moved both the parent root and its parented children, causing a double +17.112 m shift. r19 explicitly repairs this hierarchy mistake before rebuilding power routing.

Final r19 contact strategy:

- refuge root is the level **pad-center plane** at Z 9.632 m;
- terrain under 20 pad centers spans 8.426–9.438 m;
- highest pad embeds 0.08 m;
- remaining support gaps are bridged by 19 adjustable galvanized steel piers;
- pier lengths: 0.109–0.982 m;
- pier ground start embeds 0.05 m;
- floor bottom sits 0.710–1.427 m above terrain across sampled corners;
- clock base embeds 0.08 m;
- route beacons embed 0.05 m individually.

This creates a plausible level service platform over gently varying terrain instead of conforming the building floor to the landscape.

## Stable socket contract

Version: `AUR-SOCKET-SERVICE-v1-r19`.

Sockets are metadata on functional objects, not debug empties:

- `AUR_PROOF_SERVICE_TRAY_3.socket_service_out_world`;
- `AUR_CLOCK_SYNC_PROOF_BASE.socket_power_in_world`;
- `AUR_CLOCK_SYNC_PROOF_BASE.socket_data_out_world`;
- `AUR_ROUTE_BEACON_PROOF_0..3.socket_data_in_world`.

## Power route

Object: `AUR_ROUTE_POWER_TRAY_TO_CLOCK`.

Path:

1. service tray exit;
2. high accessible junction box;
3. vertical riser to low service level;
4. clock-side junction/socket.

Measured:

- length: **14.155 m**;
- cable radius: 0.045 m;
- terrain clearance at control points: 0.65–2.951 m;
- material: `AUR_MAT_CABLE_POWER_JACKET`;
- minimum bend radius target: 0.22 m;
- voltage/electrical class: **UNSPECIFIED_PENDING_ELECTRICAL_CANON**.

Final swept elbows are not claimed: current proof uses explicit polyline bends to prove topology and service path.

## Redundant data route

Objects:

- `AUR_ROUTE_DATA_A_CLOCK_TO_BEACONS`;
- `AUR_ROUTE_DATA_B_CLOCK_TO_BEACONS`.

Measured:

- A length: 77.621 m;
- B length: 77.549 m;
- 14 authored terrain-sampled control points each;
- cable radius: 0.022 m;
- terrain clearance: **0.45 m at every control point**;
- paired paths offset laterally ±0.065 m;
- material: `AUR_MAT_CABLE_DATA_JACKET`;
- final cable class/protocol remains unspecified.

The two lines share a local corridor but remain visually/physically separate. Redundancy semantics are a proposal until runtime/network design exists.

## Supports

Four `AUR_CABLE_STAKE_*` instances use one shared mesh datablock: `AUR_CABLE_STAKE_SHARED_MESH_R18`.

- approximate blockout spacing: ~18 m;
- no hidden source object exists in the routing collection;
- GLB may log the shared mesh primitive once, which is expected for instanced objects and does not imply an extra library object.

## Junction boxes

- `AUR_ROUTING_JBOX_TRAY_EXIT`;
- `AUR_ROUTING_JBOX_GROUND_RISER`;
- `AUR_ROUTING_JBOX_CLOCK`.

Construction intent: folded zinc-coated enclosures with removable covers and front service access.

## Material roles

- `AUR_MAT_CABLE_POWER_JACKET`: extruded polymer jacket, nonmetallic, roughness ~0.72;
- `AUR_MAT_CABLE_DATA_JACKET`: extruded polymer jacket, nonmetallic, roughness ~0.76;
- cable wear is limited to clamp/contact polish, UV chalking on exposed runs and ground-adjacent dust; random scratches/metal response are forbidden.

## QA receipt

r19 technical audit:

- 20 pads;
- pad-bottom offsets −0.08 to +0.932 m;
- 19 foundation piers;
- pier length 0.109–0.982 m;
- power clearance 0.65–2.951 m;
- data A/B clearance exactly 0.45 m;
- clock and all 4 beacons have terrain-contact embed contracts;
- no AREA lights;
- no accidental `LIB_*`, `DEBUG`, or hidden objects inside `23_CAMP_SERVICE_ROUTING`.

Render evidence:

- `aurora_r19_service_routing.png` / artifact `f02832c9aff87f1e8adccdd9d1f86faa`;
- 480×270;
- mean 0.1982;
- p01 0.0104;
- p50 0.1979;
- p99 0.3615;
- black clip 0.0088;
- white clip 0.

Human visual approval remains open.

## Open gates

- final electrical/load/data classes;
- final elbow/bend geometry and clamp details;
- electrical safety separation/EMI rules if the game ever exposes them;
- runtime interaction/repair gameplay;
- collision/interactable proxies where gameplay requires them;
- final PBR texture detail;
- LOD/HLOD/performance;
- human GATE-ART.
