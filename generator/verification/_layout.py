"""Locate this generator repo and the target open-dis-python checkout.

Layout contract (ruled 2026-10-18): this repo is pinned as a submodule
of open-dis-python at submodules/open-dis-python-generator, so the
canonical way to run anything here is from inside that checkout — the
target is then an ancestor of this repo. Standalone clones fall back to
a sibling ../open-dis-python checkout, then to $OPENDIS_TARGET.

Importing this module also puts both roots on sys.path: the generator
repo (``from generator import ...``) and the target (``import opendis``).
Staging always lives target-side at <target>/generated so the converge
step (cp generated/... opendis/...) runs from the target root; the
generator itself never writes opendis/ (transition-oracle ruling).
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

GENREPO = Path(__file__).resolve().parents[2]
XML_DIR = GENREPO / "submodules" / "open-dis-spec-xml" / "xml"


def _is_target_checkout(path: Path) -> bool:
    return (path / "opendis" / "__init__.py").is_file() and (path / ".git").exists()


def _find_target() -> Path:
    override = os.environ.get("OPENDIS_TARGET")
    if override:
        candidate = Path(override).resolve()
        if not _is_target_checkout(candidate):
            raise SystemExit(
                f"OPENDIS_TARGET={override!r} is not an open-dis-python checkout"
            )
        return candidate
    for candidate in GENREPO.parents:
        if _is_target_checkout(candidate):
            return candidate
    sibling = GENREPO.parent / "open-dis-python"
    if _is_target_checkout(sibling):
        return sibling
    raise SystemExit(
        "target open-dis-python checkout not found: run from the pinned "
        "submodule layout, place a sibling open-dis-python checkout, or "
        "set OPENDIS_TARGET"
    )


TARGET = _find_target()
STAGING = TARGET / "generated"

sys.path.insert(0, str(GENREPO))
sys.path.insert(0, str(TARGET))


def generator_env() -> dict[str, str]:
    """Environment with this repo importable (``python -m generator``)."""
    env = dict(os.environ)
    parts = [str(GENREPO)]
    if env.get("PYTHONPATH"):
        parts.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(parts)
    return env


def run_generator(out: Path | None = None) -> int:
    """Regenerate the full module set into staging (never opendis/)."""
    return subprocess.call(
        [
            sys.executable,
            "-m",
            "generator",
            "--xml-dir",
            str(XML_DIR),
            "--out",
            str(out or STAGING),
        ],
        env=generator_env(),
    )
