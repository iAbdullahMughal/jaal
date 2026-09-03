#!/usr/bin/env python3
"""sign.py — HMAC-sign a jaal evidence envelope.

Removes any stale signature, canonicalizes the JSON, HMAC-SHA256 signs the
canonical bytes, and writes the sig alongside the envelope.

Public-key validation counterpart: scripts/verify.py

Usage:
    python3 scripts/sign.py iocs/000/ev-000001.json              # reads key from env
    JAAL_HMAC_KEY='…' python3 scripts/sign.py <env> -o out.json
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys

DEFAULT_KEY_ID = "jaal-pub-2026"


def canonical_bytes(obj: dict) -> bytes:
    """Deterministic UTF-8 JSON (sorted keys, no whitespace) for stable HMAC."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sign(envelope: dict, key: bytes, key_id: str = DEFAULT_KEY_ID) -> dict:
    env = json.loads(json.dumps(envelope))  # deep copy
    env.pop("signature", None)
    sig = hmac.new(key, canonical_bytes(env), hashlib.sha256).hexdigest()
    env["signature"] = {"alg": "hmac-sha256", "key_id": key_id, "value": sig}
    return env


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("path")
    p.add_argument("--key", default=os.environ.get("JAAL_HMAC_KEY", ""))
    p.add_argument("--key-id", default=DEFAULT_KEY_ID)
    a = p.parse_args()

    if not a.key:
        print("JAAL_HMAC_KEY not set (env JAAL_HMAC_KEY or --key). Refusing to write.bsig.")
        return 2
    with open(a.path) as f:
        env = json.load(f)
    signed = sign(env, a.key.encode(), a.key_id)
    sig_path = a.path + ".hmac.sha256"
    with open(sig_path, "w") as f:
        f.write(signed["signature"]["value"] + "\n")
    with open(a.path, "w") as f:
        json.dump(signed, f, indent=2, ensure_ascii=False)
    print(f"signed {a.path} -> {sig_path} (key_id={a.key_id})")
    return 0


if __name__ == "__main__":
    sys.exit(main())