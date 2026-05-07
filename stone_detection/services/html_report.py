from __future__ import annotations

from .reference_imports import import_reference_module


class _LazyReferenceClass:
    def __init__(self, module_name: str, class_name: str):
        self.module_name = module_name
        self.class_name = class_name

    def _resolve(self):
        return getattr(import_reference_module(self.module_name), self.class_name)

    def __call__(self, *args, **kwargs):
        return self._resolve()(*args, **kwargs)

    def __getattr__(self, name: str):
        return getattr(self._resolve(), name)


HtmlTableApi = _LazyReferenceClass("common.my_html", "HtmlTableApi")

__all__ = ["HtmlTableApi"]

