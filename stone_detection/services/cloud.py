from __future__ import annotations

from .reference_imports import import_reference_module


def upload(*args, **kwargs):
    return getattr(import_reference_module("common.cloud_sever"), "upload")(*args, **kwargs)


__all__ = ["upload"]

