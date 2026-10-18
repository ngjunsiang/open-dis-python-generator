# open-dis-python-generator

DIS 7 code generator for the
[open-dis-python](https://github.com/open-dis/open-dis-python) `dis7-ng`
line (maintained at [ngjunsiang/open-dis-python](https://github.com/ngjunsiang/open-dis-python)):
corrected spec XML + REF-010 data → typed IR → semantic resolution →
static explicit-body emission (pure Python, stdlib-only) → black
post-pass → acceptance harnesses.

Split out of `ngjunsiang/open-dis-python@dis7-ng` on 2026-10-18 (commit
`766e73e`); the generator's own history starts here.

## Pin chain

    open-dis-python (dis7-ng)                  ← generator target: opendis/ + hand kernel + tests
      └── submodules/open-dis-python-generator ← this repo, pinned per generator version
            ├── submodules/open-dis-spec-xml     @ v0.12.9  (DIS 7 XML, corrected — final word on wire discrepancies)
            └── submodules/siso-ref-010-python   @ 0.10.1   (REF-010 data, pure Python)

A generator version bump (which may carry spec / REF-010 pin advances)
is consumed by the target by advancing its submodule pin and
regenerating.

The generator is stdlib-only: `siso_ref010` is imported straight from
its submodule checkout (no pip install), and `black` is a dev-time
post-pass invoked via the running interpreter — any venv that has it
works (the target's dev group does).

## Setup

    git clone https://github.com/ngjunsiang/open-dis-python-generator.git
    cd open-dis-python-generator
    git submodule update --init

Non-recursive `--init` is enough: `siso-ref-010-python` carries a
private vendor submodule used only to regenerate that package.

## Regenerating the target

Canonical flow, run in the target checkout after bumping the generator
pin:

    # in open-dis-python @ dis7-ng
    git submodule update --init --recursive
    PYTHONPATH=submodules/open-dis-python-generator \
        .venv/bin/python -m generator        # writes ./generated (staging only)

    # converge after reviewing the diff (the generator never writes opendis/)
    cp generated/record/common.py opendis/record/
    cp -r generated/record/*/ opendis/record/
    cp generated/bitfields/*.py opendis/bitfields/

## Acceptance harnesses

`generator/verification/` — run each with an interpreter that has black
(the target's `.venv`); the target checkout is auto-discovered
(ancestor when run from the pinned submodule layout, sibling
`../open-dis-python`, or `$OPENDIS_TARGET`):

| harness | pins |
| --- | --- |
| `byte_identity.py` | every generated module byte-identical to regeneration |
| `parity_common.py` | common records: serialization, cross-parse, sizes, policy |
| `parity_entity_information.py` | entity_information family behavior |
| `parity_families.py` | all families: identity constants, factory, size oracle |
| `parity_bitfields.py` | bitfield views: layout + seeded get/set behavior |
| `stamps_and_corpus.py` | stamp-manifest sync + golden `.raw` corpus decode |

## License

BSD 2-Clause — see [LICENSE](LICENSE).
