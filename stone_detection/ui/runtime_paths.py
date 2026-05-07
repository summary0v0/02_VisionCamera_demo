from __future__ import annotations

from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PACKAGE_ROOT / "configs" / "cfg.json"
TEMP_IMAGE_DIR = PACKAGE_ROOT / "ui" / "assets" / "temp_images"

