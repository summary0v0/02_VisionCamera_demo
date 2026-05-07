from __future__ import annotations

import glob
import json
import os
import platform
import subprocess
import sys
import time
import traceback
from datetime import datetime
from io import BytesIO
from tempfile import NamedTemporaryFile

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTimer, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from ...services.cad import *
from ...services.cloud import upload
from ...services.database import *
from ...services.hardware import MainHardwareIntegration
from ...services.html_report import HtmlTableApi
from ...services.threads import *
from ...services.user_action_log import log_user_action
from ..dialogs.tip_window import TipWin
from ..runtime_paths import CONFIG_PATH, TEMP_IMAGE_DIR


class _MissingDependency:
    def __init__(self, package_name: str):
        self.package_name = package_name

    def __getattr__(self, name: str):
        raise RuntimeError(f"Missing optional dependency: {self.package_name}")

    def __call__(self, *args, **kwargs):
        raise RuntimeError(f"Missing optional dependency: {self.package_name}")


def _optional_import(module_name: str):
    try:
        return __import__(module_name)
    except ImportError:
        return _MissingDependency(module_name)


cv2 = _optional_import("cv2")
requests = _optional_import("requests")
pyautogui = _optional_import("pyautogui")

try:
    from PIL import Image, ImageFile
except ImportError:
    Image = _MissingDependency("Pillow")
    ImageFile = _MissingDependency("Pillow")
else:
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    Image.MAX_IMAGE_PIXELS = None

try:
    from selenium import webdriver
    from selenium.webdriver.edge.options import Options
except ImportError:
    webdriver = _MissingDependency("selenium")
    Options = _MissingDependency("selenium")


download_dir = str(TEMP_IMAGE_DIR)
os.makedirs(download_dir, exist_ok=True)

__all__ = [name for name in globals() if not name.startswith("_")]

