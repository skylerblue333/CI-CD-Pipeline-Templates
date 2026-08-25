#!/usr/bin/env python3
"""Lightweight structural checks for the shipped GitHub Actions templates."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "templates" / "github-actions"
REQUIRED = {"node-ci.yml", "python-ci.yml", "go-ci.yml", "docker-ci.yml"}
FORBIDDEN = (
    "contents: write",
    "pull-requests: write",
    "packages: write",
    "id-token: write",
    "push: true",
)


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for marker in ("permissions:\n  contents: read", "runs-on: ubuntu-latest", "timeout-minutes:"):
        if marker not in text:
            errors.append(f"{path.name}: missing required marker {marker!r}")
    for marker in FORBIDDEN:
        if marker in text:
            errors.append(f"{path.name}: forbidden default {marker!r}")
    if "actions/checkout@v4" not in text:
        errors.append(f"{path.name}: checkout action must use v4")
    return errors


def main() -> int:
    found = {path.name for path in TEMPLATE_DIR.glob("*.yml")}
    errors = [f"missing template: {name}" for name in sorted(REQUIRED - found)]
    for path in sorted(TEMPLATE_DIR.glob("*.yml")):
        errors.extend(validate(path))

    if errors:
        print("\n".join(errors))
        return 1
    print(f"validated {len(found)} CI templates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
