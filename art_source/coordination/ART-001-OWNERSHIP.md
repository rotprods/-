# ART-001 · ownership and integration handoff

User directive (12 September 2026): this agent owns remote Blender asset design; another agent owns gameplay. Base 4c2fa044080004609ea6df45f34b2a784536507a.

Owned paths: art_source/terra_reliquary_kit/, art_source/production_catalog/, art_source/coordination/. Runtime scripts/scenes/controls and the existing portal files are outside this edit scope. Shared project state changes are proposed in this branch and must be reconciled with newer main before integration.

Remote Blender project: 710b21ea-a09a-4f3c-b3a4-ca446ec58bc8. Independent scene; no changes to previous project 989aa82f-9eb8-4fd9-b475-87347ce834f9. Linear issue ROT-98 / UUID 67cb3534-bd03-48de-9e86-68c14f24588d tracks the art handoff.

No acknowledgment from the external gameplay agent has been observed. This branch/PR makes ownership discoverable; local studio locks are not distributed locks. Please integrate by reviewed fast-forward/merge after checking current main; never force refs.
