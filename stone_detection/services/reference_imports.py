from __future__ import annotations

import importlib
import sys
from pathlib import Path


def reference_root() -> Path:
    """Locate the original reference implementation without hard-coding locale text."""
    for parent in Path(__file__).resolve().parents:
        resource_dir = parent / "resource"
        if not resource_dir.exists():
            continue
        for candidate in resource_dir.glob("*/stone_detection"):
            if (candidate / "application.py").exists():
                return candidate
    raise FileNotFoundError("Could not locate resource/*/stone_detection reference code.")


def ensure_reference_on_path() -> Path:
    root = reference_root()
    root_str = str(root)
    common_str = str(root / "common")
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    if common_str not in sys.path:
        sys.path.insert(0, common_str)
    return root


def import_reference_module(module_name: str):
    ensure_reference_on_path()
    return importlib.import_module(module_name)
