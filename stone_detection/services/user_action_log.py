from __future__ import annotations

from datetime import datetime
from pathlib import Path


LOG_FILE_PATH = "log"
LOG_USER_PATH = "log_user_management.txt"


def log_user_action(username: str, action_type: str, target_user: str = None, result: str = None):
    Path(LOG_FILE_PATH).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    target_info = f"Target: {target_user}" if target_user else "Target: None"
    log_line = f"[{timestamp}] User: {username}, Action: {action_type}, {target_info}, Result: {result}\n"
    with open(Path(LOG_FILE_PATH) / LOG_USER_PATH, "a", encoding="utf-8") as f:
        f.write(log_line)

