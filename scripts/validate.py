"""Validate registry.json against registry.schema.json.

Run with:
    uv run scripts/validate.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "registry.json"
SCHEMA = ROOT / "registry.schema.json"


def main() -> int:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))

    if errors:
        for err in errors:
            location = "/".join(str(p) for p in err.absolute_path) or "<root>"
            print(f"FAIL [{location}]: {err.message}", file=sys.stderr)
        return 1

    print(f"OK: {REGISTRY.name} is valid against {SCHEMA.name} ({len(data['entries'])} entries).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
