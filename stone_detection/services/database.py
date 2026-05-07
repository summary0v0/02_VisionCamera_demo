from __future__ import annotations

from .reference_imports import import_reference_module


_EXPORTED_FUNCTIONS = [
    "process_stone_item_from_url",
    "get_box_number_by_composite",
    "update_cutting_status",
    "query_stone_measurements",
    "get_cutting_records",
    "query_image_urls",
    "query_measurements",
    "get_scan_counts",
    "get_scan_areas",
    "query_cutting_records",
    "get_latest_defect_info",
    "delete_user",
    "get_all_users",
    "update_user",
    "hash_password",
    "check_login",
    "get_user_role",
    "register_user",
    "change_password",
]


def _db_module():
    return import_reference_module("common.dbFunction")


def _call(name: str, *args, **kwargs):
    return getattr(_db_module(), name)(*args, **kwargs)


def __getattr__(name: str):
    if name.startswith("__"):
        raise AttributeError(name)
    return getattr(_db_module(), name)


def process_stone_item_from_url(*args, **kwargs):
    return _call("process_stone_item_from_url", *args, **kwargs)


def get_box_number_by_composite(*args, **kwargs):
    return _call("get_box_number_by_composite", *args, **kwargs)


def update_cutting_status(*args, **kwargs):
    return _call("update_cutting_status", *args, **kwargs)


def query_stone_measurements(*args, **kwargs):
    return _call("query_stone_measurements", *args, **kwargs)


def get_cutting_records(*args, **kwargs):
    return _call("get_cutting_records", *args, **kwargs)


def query_image_urls(*args, **kwargs):
    return _call("query_image_urls", *args, **kwargs)


def query_measurements(*args, **kwargs):
    return _call("query_measurements", *args, **kwargs)


def get_scan_counts(*args, **kwargs):
    return _call("get_scan_counts", *args, **kwargs)


def get_scan_areas(*args, **kwargs):
    return _call("get_scan_areas", *args, **kwargs)


def query_cutting_records(*args, **kwargs):
    return _call("query_cutting_records", *args, **kwargs)


def get_latest_defect_info(*args, **kwargs):
    return _call("get_latest_defect_info", *args, **kwargs)


def delete_user(*args, **kwargs):
    return _call("delete_user", *args, **kwargs)


def get_all_users(*args, **kwargs):
    return _call("get_all_users", *args, **kwargs)


def update_user(*args, **kwargs):
    return _call("update_user", *args, **kwargs)


def hash_password(*args, **kwargs):
    return _call("hash_password", *args, **kwargs)


def check_login(*args, **kwargs):
    return _call("check_login", *args, **kwargs)


def get_user_role(*args, **kwargs):
    return _call("get_user_role", *args, **kwargs)


def register_user(*args, **kwargs):
    return _call("register_user", *args, **kwargs)


def change_password(*args, **kwargs):
    return _call("change_password", *args, **kwargs)


__all__ = _EXPORTED_FUNCTIONS
