from __future__ import annotations

import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PyQt5.QtWidgets import QApplication

from stone_detection.services.user_action_log import log_user_action
from stone_detection.ui.dialogs.tip_window import TipWin
from stone_detection.ui.runtime_paths import CONFIG_PATH
from stone_detection.ui.windows.login_window import LoginWindow
from stone_detection.ui.windows.main_window import Window

DEFAULT_USER = "local_admin"
DEFAULT_ROLE = "superadmin"


def _load_startup_config() -> dict:
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _create_main_window_from_config() -> Window:
    cfg = _load_startup_config()
    return Window(
        current_user=cfg.get("default_user", DEFAULT_USER),
        current_user_role=cfg.get("default_role", DEFAULT_ROLE),
    )


def main():
    app = QApplication.instance() or QApplication(sys.argv)
    mywindow = _create_main_window_from_config()
    mywindow.showMaximized()
    return app.exec_()


def login_main():
    app = QApplication.instance() or QApplication(sys.argv)
    cfg = _load_startup_config()
    if cfg.get("auto_login", False):
        mywindow = _create_main_window_from_config()
        mywindow.showMaximized()
        return app.exec_()

    login = LoginWindow()
    login.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(login_main())


__all__ = ["Window", "TipWin", "LoginWindow", "log_user_action", "main", "login_main"]
