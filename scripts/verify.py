#!/usr/bin/env python3
"""verify.py — quick sanity check that an IOC file is well-formed JSON.

Usage:
    python3 scripts/verify.py iocs/45.153.34.235.json

Exits 0 if the file is valid JSON with the expected fields, 1 otherwise.
"""
import json
import sys

REQUIRED = {"type", "value"}
KNOWN_TYPES = {"ipv4-addr", "domain-name", "file", "hash", "url", "email"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python3 scripts/verify.py <file>")
        return 2

    path = sys.argv[1]
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"NOT valid JSON: {e}")
        return 1

    if not isinstance(data, dict):
        print("NOT an object — expected a single JSON object (use feeds/ for lists)")
        return 1

    missing = REQUIRED - set(data)
    if missing:
        print(f"missing required fields: {sorted(missing)}")
        return 1

    if data.get("type") not in KNOWN_TYPES:
        print(f"unknown type {data.get('type')!r} (known: {sorted(KNOWN_TYPES)})")
        return 1

    print(f"OK: {data['type']} {data['value']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())