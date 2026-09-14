"""Validated entrypoint for aurora_x100_camp_props_r30.py.

The base generator persisted from the remote mutation uses `Vector` in collision
contract placement but omitted the import line. Rather than silently claim that
file is standalone, this entrypoint injects `mathutils.Vector` into its execution
globals and then calls `build()` exactly once.

Approved source pair for AUR-X100-CAMP-PROPS-CULTURE-001:
- aurora_x100_camp_props_r30.py     (generator body)
- aurora_x100_camp_props_r30_entrypoint.py (this executable entrypoint)

When the base file receives `from mathutils import Vector`, this compatibility
entrypoint can be retired.
"""
from pathlib import Path
from mathutils import Vector

source_path = Path(__file__).with_name("aurora_x100_camp_props_r30.py")
source = source_path.read_text(encoding="utf-8")
scope = {
    "__name__": "aurora_x100_camp_props_r30_generator",
    "__file__": str(source_path),
    "Vector": Vector,
}
exec(compile(source, str(source_path), "exec"), scope, scope)
result = scope["build"]()
print(result)
