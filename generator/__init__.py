"""Clean-slate DIS 7 code generator for open-dis-python.

Architecture (ruled 2026-10-14; split into its own repo 2026-10-18):
XML → typed IR → semantic resolution → static explicit-body emission
(pure-Python, stdlib-only) → black post-pass → behavioral verification
(the verification/ scripts prove generated output behaves identically
to the reviewed exemplar before it replaces hand-written modules).
This repo is pinned as a submodule of open-dis-python and owns its own
inputs: submodules/open-dis-spec-xml/xml (the corrected spec — the
final word on DIS 7 wire discrepancies) and submodules/
siso-ref-010-python (REF-010 layouts, enum table names, dispatch
labels).

Stdlib-only by ruling so the generator runs from any checkout of this
repo with nothing but a Python interpreter (siso_ref010 is consumed
straight from its submodule checkout); black is a dev-time post-pass
invoked via the running interpreter, not a runtime dependency.
"""

import sys
from pathlib import Path

# REF-010 comes from the pinned submodule checkout — no pip install of
# siso-ref-010-python needed. Inserted at sys.path[0] so the pinned copy
# wins over any site-packages copy in the invoking environment.
_SISO_SRC = (
    Path(__file__).resolve().parents[1] / "submodules" / "siso-ref-010-python" / "src"
)
if (_SISO_SRC / "siso_ref010").is_dir():
    sys.path.insert(0, str(_SISO_SRC))

__version__ = "0.1.1"
