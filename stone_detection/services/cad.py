from __future__ import annotations

from .reference_imports import import_reference_module


def init_canvas(*args, **kwargs):
    return getattr(import_reference_module("common.execute_cad"), "init_canvas")(*args, **kwargs)


def __getattr__(name: str):
    if name.startswith("__"):
        raise AttributeError(name)
    return getattr(import_reference_module("common.execute_cad"), name)


__all__ = ["init_canvas"]
