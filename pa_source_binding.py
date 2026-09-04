"""Load PA Research publication modules from one immutable source snapshot.

The loader is intentionally small and dependency-free. It is the trust root
for publication entry points: source bytes are read from one open descriptor,
compiled from those exact bytes, and registered against the exact module object
and global namespace created by this loader. A conventionally imported module
therefore cannot transplant a source snapshot and claim publication provenance.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import stat
import sys
import threading
from types import ModuleType
from weakref import WeakKeyDictionary


_BOUND_MODULES: WeakKeyDictionary[ModuleType, "SourceSnapshot"] = WeakKeyDictionary()
_BOUND_MODULES_LOCK = threading.RLock()


@dataclass(frozen=True)
class SourceSnapshot:
    path: Path
    content: bytes
    sha256: str
    identity: tuple[int, int]
    size: int
    mtime_ns: int


def read_source_snapshot(path: Path, label: str) -> SourceSnapshot:
    """Read a regular source file and its identity through one descriptor."""

    resolved = path.resolve(strict=True)
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
    descriptor = os.open(resolved, flags)
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise RuntimeError(f"{label} is not a regular file")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    content = b"".join(chunks)
    identity = (before.st_dev, before.st_ino)
    if (
        (after.st_dev, after.st_ino) != identity
        or before.st_size != after.st_size
        or before.st_mtime_ns != after.st_mtime_ns
        or after.st_size != len(content)
    ):
        raise RuntimeError(f"{label} changed while its source snapshot was read")
    return SourceSnapshot(
        path=resolved,
        content=content,
        sha256=hashlib.sha256(content).hexdigest(),
        identity=identity,
        size=after.st_size,
        mtime_ns=after.st_mtime_ns,
    )


def require_source_snapshot(
    module: object,
    namespace: object,
    path: Path,
    label: str,
) -> SourceSnapshot:
    """Return the snapshot bound by the loader to this exact module namespace."""

    if not isinstance(module, ModuleType) or module.__dict__ is not namespace:
        raise RuntimeError(f"{label} must be executed through its source-bound launcher")
    if sys.modules.get(module.__name__) is not module:
        raise RuntimeError(f"{label} must be executed through its source-bound launcher")
    with _BOUND_MODULES_LOCK:
        snapshot = _BOUND_MODULES.get(module)
    if snapshot is None:
        raise RuntimeError(f"{label} must be executed through its source-bound launcher")
    if snapshot.path != path.resolve(strict=True):
        raise RuntimeError(f"{label} binding does not match the executing source path")
    return snapshot


def verify_source_snapshot(snapshot: SourceSnapshot, label: str) -> None:
    """Require the current path to remain the descriptor-bound snapshot."""

    current = read_source_snapshot(snapshot.path, label)
    if (
        current.identity != snapshot.identity
        or current.size != snapshot.size
        or current.mtime_ns != snapshot.mtime_ns
        or current.content != snapshot.content
    ):
        raise RuntimeError(f"{label} changed during run")


def load_source_module(path: Path, module_name: str, label: str) -> ModuleType:
    """Compile and execute a module from the exact bytes in its source binding."""

    snapshot = read_source_snapshot(path, label)
    module = ModuleType(module_name)
    module.__file__ = str(snapshot.path)
    module.__package__ = module_name.rpartition(".")[0]
    previous = sys.modules.get(module_name)
    sys.modules[module_name] = module
    try:
        code = compile(snapshot.content, str(snapshot.path), "exec", dont_inherit=True)
        exec(code, module.__dict__)
        with _BOUND_MODULES_LOCK:
            _BOUND_MODULES[module] = snapshot
    except BaseException:
        if previous is None:
            sys.modules.pop(module_name, None)
        else:
            sys.modules[module_name] = previous
        raise
    return module
