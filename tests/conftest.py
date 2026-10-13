"""Delay gltest's POSIX-style temp unlink on Windows without changing VM behavior."""
import atexit
import os
from gltest.direct import loader

_original = loader._inject_message_to_fd0
_paths = []


def _safe(vm):
    unlink = os.unlink
    os.unlink = lambda path: _paths.append(path)
    try:
        _original(vm)
    finally:
        os.unlink = unlink


def _cleanup():
    for path in _paths:
        try: os.unlink(path)
        except OSError: pass


if os.name == "nt":
    loader._inject_message_to_fd0 = _safe
    atexit.register(_cleanup)
