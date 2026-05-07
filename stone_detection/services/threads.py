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


WatchDogThread = _LazyReferenceClass("my_thread", "WatchDogThread")
InitThread = _LazyReferenceClass("my_thread", "InitThread")
CadThread = _LazyReferenceClass("my_thread", "CadThread")
QRThread1 = _LazyReferenceClass("my_thread", "QRThread1")
QRThread2 = _LazyReferenceClass("my_thread", "QRThread2")
QRThread3 = _LazyReferenceClass("my_thread", "QRThread3")
QRThread4 = _LazyReferenceClass("my_thread", "QRThread4")
QRThread5 = _LazyReferenceClass("my_thread", "QRThread5")

__all__ = [
    "WatchDogThread",
    "InitThread",
    "CadThread",
    "QRThread1",
    "QRThread2",
    "QRThread3",
    "QRThread4",
    "QRThread5",
]

