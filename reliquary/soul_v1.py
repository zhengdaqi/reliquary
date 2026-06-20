"""
Reliquary Soul SDK v0.1 — secp256k1-based identity (WIP).

This module is the v0.1 evolution of `soul.py`. The architectural shape is
unchanged; only the identity primitive swaps:

  v0.0.x: ed25519 for keypair + signing, SHA-256 for fingerprint.
  v0.1:    secp256k1 for keypair + signing, SHA-256 for fingerprint
           (Keccak-256 / Ethereum address is the v0.1.1 target — see below).

The reason for the swap is interoperability with the existing agent
ecosystem (ERC-8004 IdentityRegistry, x402, EVM-based payment rails).
A Soul's identity in v0.1 IS an Ethereum-compatible secp256k1 keypair.

NOT YET in this file:
- Keccak-256 fingerprinting (we use SHA-256 for now; v0.1.1 will add
  pycryptodome for true Ethereum address derivation)
- M-of-N threshold signing (v0.1 design)
- ERC-8004 registration (separate module, see plan)
- x402 payment integration (separate module, see plan)

This file is a stub. It exists to:
1. Show the migration is mechanical
2. Make the v0.1 work trackable in git
3. Establish the file structure v0.1 will fill in
"""

from __future__ import annotations

import hashlib
import os
import struct
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend

# Curve constant re-exported so callers don't import cryptography directly.
# Note: SECP256K1 is a class in modern `cryptography`; pass it directly
# to `ec.generate_private_key()` without instantiating.
CURVE = ec.SECP256K1  # type: ignore[assignment]


def generate_keypair() -> ec.EllipticCurvePrivateKey:
    """Generate a new secp256k1 private key."""
    return ec.generate_private_key(CURVE(), default_backend())


def serialize_private_key(priv: ec.EllipticCurvePrivateKey) -> bytes:
    """Serialize a private key to 32-byte raw form (Ethereum-compatible).

    The `cryptography` library's `PrivateFormat.Raw` is not valid for EC
    keys (it raises ValueError), so we extract the private scalar directly
    via `private_numbers()`. This gives us the canonical 32-byte big-endian
    representation, identical to what Ethereum uses internally.
    """
    d = priv.private_numbers().private_value
    if d < 0 or d >= 2**256:
        raise ValueError("private scalar is out of range for secp256k1")
    return d.to_bytes(32, "big")


def load_private_key(raw: bytes) -> ec.EllipticCurvePrivateKey:
    """Load a 32-byte raw secp256k1 private key."""
    if len(raw) != 32:
        raise ValueError(f"secp256k1 private key must be 32 bytes, got {len(raw)}")
    return ec.derive_private_key(int.from_bytes(raw, "big"), CURVE(), default_backend())


def public_key_bytes(pub: ec.EllipticCurvePublicKey) -> bytes:
    """Serialize a public key to 64-byte raw form (Ethereum-compatible,
    no 0x04 prefix). For v0.1.1, Keccak-256 of this gives the Ethereum
    address; for now, SHA-256 of this gives the fingerprint."""
    raw = pub.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint,
    )
    assert raw[0] == 0x04, "expected uncompressed point to start with 0x04"
    return raw[1:]  # 64 bytes (32 X + 32 Y)


def fingerprint(pub: ec.EllipticCurvePublicKey) -> str:
    """Compute the Soul's fingerprint.

    v0.1.0 (this file): SHA-256 of the public key, hex-encoded, first 20
        bytes shown (40 hex chars). 20 bytes is a deliberate choice to
        match Ethereum address length.
    v0.1.1 (next): Keccak-256 of the public key, last 20 bytes, hex, with
        EIP-55 checksum.
    """
    pub_b = public_key_bytes(pub)
    h = hashlib.sha256(pub_b).digest()
    return h[:20].hex()


def sign(priv: ec.EllipticCurvePrivateKey, message: bytes) -> bytes:
    """Sign a message with ECDSA-secp256k1 + SHA-256.

    Returns DER-encoded signature (variable length, typically 70-72 bytes).
    """
    return priv.sign(message, ec.ECDSA(hashes.SHA256()))


def verify(pub: ec.EllipticCurvePublicKey, signature: bytes, message: bytes) -> bool:
    """Verify an ECDSA-secp256k1 + SHA-256 signature."""
    try:
        pub.verify(signature, message, ec.ECDSA(hashes.SHA256()))
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# WIP: full Soul identity object modeled on v0's Soul dataclass.
# To be filled in as v0.1 work progresses.
# ---------------------------------------------------------------------------


@dataclass
class SoulV1:
    """A v0.1 Soul — secp256k1-based identity.

    Status: stub. The full migration from v0's Soul class to this is
    the v0.1 work item. For now this is a typed shell.
    """
    fingerprint_hex: str
    private_key: ec.EllipticCurvePrivateKey
    public_key: ec.EllipticCurvePublicKey
    created_at: int = field(default_factory=lambda: int(time.time()))
    soul_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def generate(cls) -> "SoulV1":
        priv = generate_keypair()
        pub = priv.public_key()
        return cls(
            fingerprint_hex=fingerprint(pub),
            private_key=priv,
            public_key=pub,
        )

    def sign(self, message: bytes) -> bytes:
        return sign(self.private_key, message)

    def verify(self, signature: bytes, message: bytes) -> bool:
        return verify(self.public_key, signature, message)
