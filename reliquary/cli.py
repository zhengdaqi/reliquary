"""
reliquary.cli — a small command-line interface for the Soul layer.

Usage:
    python -m reliquary.cli generate            # create a new Soul
    python -m reliquary.cli fingerprint        # print the fingerprint of a stored Soul
    python -m reliquary.cli put <file>         # encrypt and store a file as a Soul
    python -m reliquary.cli get <pointer>      # retrieve and decrypt a Soul
    python -m reliquary.cli list               # list all stored Souls
    python -m reliquary.cli heartbeat          # write a heartbeat
    python -m reliquary.cli status             # print Soul status (heartbeat age, inheritor)

For v0, the Soul's private key is stored in plain bytes in a file
named `soul.key` in the current directory. THIS IS NOT SECURE.
v0.1 will integrate with system keychains or hardware wallets.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from reliquary.soul import (
    Soul,
    SoulBlob,
    LocalSoulStore,
    Inheritor,
    write_heartbeat,
    is_alive,
)


KEY_PATH = Path("soul.key")
HEARTBEAT_PATH = Path("soul.heartbeat")
STORE_ROOT = Path("soul_store")


def _load_or_create_soul(create: bool = False) -> Soul:
    if KEY_PATH.exists():
        return Soul.from_private_key_bytes(KEY_PATH.read_bytes())
    if not create:
        print(f"No Soul found at {KEY_PATH}. Run `generate` first.", file=sys.stderr)
        sys.exit(1)
    soul = Soul.generate()
    KEY_PATH.write_bytes(soul.private_key_bytes)
    print(f"Generated Soul. Fingerprint: {soul.fingerprint}")
    print(f"Private key written to {KEY_PATH} — BACK THIS UP.")
    return soul


def cmd_generate(_args: argparse.Namespace) -> None:
    _load_or_create_soul(create=True)
    STORE_ROOT.mkdir(exist_ok=True)


def cmd_fingerprint(_args: argparse.Namespace) -> None:
    soul = _load_or_create_soul(create=False)
    print(soul.fingerprint)


def cmd_put(args: argparse.Namespace) -> None:
    soul = _load_or_create_soul(create=False)
    STORE_ROOT.mkdir(exist_ok=True)
    store = LocalSoulStore(str(STORE_ROOT))
    payload = Path(args.file).read_bytes()
    content_type = args.content_type or "application/octet-stream"
    blob = soul.encrypt(payload, content_type=content_type)
    pointer = store.put(blob)
    print(f"Stored. Pointer: {pointer}")
    print(f"Fingerprint: {soul.fingerprint}")
    print(f"Content hash: {blob.content_hash}")


def cmd_get(args: argparse.Namespace) -> None:
    soul = _load_or_create_soul(create=False)
    store = LocalSoulStore(str(STORE_ROOT))
    blob = store.get(args.pointer)
    if not soul.verify(blob):
        print("Signature does not verify. Aborting.", file=sys.stderr)
        sys.exit(2)
    plaintext = soul.decrypt(blob)
    if args.output:
        Path(args.output).write_bytes(plaintext)
        print(f"Decrypted to {args.output}")
    else:
        sys.stdout.buffer.write(plaintext)


def cmd_list(_args: argparse.Namespace) -> None:
    if not STORE_ROOT.exists():
        print("No store yet.")
        return
    store = LocalSoulStore(str(STORE_ROOT))
    for pointer in store.list():
        print(pointer)


def cmd_heartbeat(_args: argparse.Namespace) -> None:
    soul = _load_or_create_soul(create=False)
    write_heartbeat(soul, str(HEARTBEAT_PATH))
    print(f"Heartbeat written. Alive: {is_alive(soul, str(HEARTBEAT_PATH))}")


def cmd_status(_args: argparse.Namespace) -> None:
    soul = _load_or_create_soul(create=False)
    print(f"Fingerprint:    {soul.fingerprint}")
    print(f"Public key:     {soul.public_key_b64[:32]}...")
    print(f"Last heartbeat: {soul.last_heartbeat} ({soul.days_since_heartbeat:.1f} days ago)")
    print(f"Inheritor:      {soul.inheritor}")
    print(f"Alive:          {is_alive(soul, str(HEARTBEAT_PATH)) if HEARTBEAT_PATH.exists() else 'no heartbeat file'}")
    print(f"Inheritance active: {soul.is_inheritance_active()}")


def cmd_designate_inheritor(args: argparse.Namespace) -> None:
    soul = _load_or_create_soul(create=False)
    soul.designate_inheritor(Inheritor(
        address=args.address,
        activated_after_days=args.after_days,
    ))
    print(f"Inheritor set: {args.address} (activates after {args.after_days} days of no heartbeat)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="reliquary", description="The Soul layer CLI.")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("generate", help="Create a new Soul identity.").set_defaults(func=cmd_generate)
    sub.add_parser("fingerprint", help="Print the Soul's fingerprint.").set_defaults(func=cmd_fingerprint)

    p_put = sub.add_parser("put", help="Encrypt and store a file.")
    p_put.add_argument("file")
    p_put.add_argument("--content-type", default=None)
    p_put.set_defaults(func=cmd_put)

    p_get = sub.add_parser("get", help="Retrieve and decrypt a Soul.")
    p_get.add_argument("pointer")
    p_get.add_argument("--output", "-o", default=None)
    p_get.set_defaults(func=cmd_get)

    sub.add_parser("list", help="List all stored Souls.").set_defaults(func=cmd_list)
    sub.add_parser("heartbeat", help="Write a heartbeat.").set_defaults(func=cmd_heartbeat)
    sub.add_parser("status", help="Print Soul status.").set_defaults(func=cmd_status)

    p_inh = sub.add_parser("designate-inheritor", help="Designate an inheritor.")
    p_inh.add_argument("address")
    p_inh.add_argument("--after-days", type=int, default=90)
    p_inh.set_defaults(func=cmd_designate_inheritor)

    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    args.func(args)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
