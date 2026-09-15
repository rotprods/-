"""KHEPRI X100 Material Lab orchestration wrapper.

Identity authority lives exclusively in `compile_material_library.py`.
Presentation authority lives exclusively in `present_material_lab.py`.
This wrapper composes both stages; it contains no material-generation math.

Run inside Blender 5.2+ with bpy available.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build():
    compiler = _load("khepri_material_identity", "compile_material_library.py")
    presenter = _load("khepri_material_presentation", "present_material_lab.py")
    identity = compiler.build()
    presentation = presenter.present()
    return {
        "contract": identity["contract"],
        "identity": identity,
        "presentation": presentation,
        "identity_authority": "compile_material_library.py",
        "presentation_authority": "present_material_lab.py",
    }


if __name__ == "__main__":
    print(build())
