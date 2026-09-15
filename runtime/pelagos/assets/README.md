# Pelagos runtime binary slot

Expected binary: `pelagos_world_rev44.glb`

Authoritative source:
- Higgsfield 3D Jutsu project `39930c08-62bb-4034-b35d-70d0ce51c9d9`
- World Master revision `44`
- expected bytes `19524308`
- expected etag `4aa72fec83eca94619f1b0a761e28c1e`

The binary is intentionally not represented by a placeholder. Contract-only tests may run without it. Native import tests must fail/block when it is absent.

Do not copy a different revision under the rev44 filename. Any newer World Master requires a new manifest/evidence checkpoint and node-contract reconciliation before promotion.
