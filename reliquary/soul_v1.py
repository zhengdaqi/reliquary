"""
Reliquary Soul SDK v0.1 — secp256k1-based identity.

This module is the v0.1 evolution of `soul.py`. The architectural shape is
unchanged; only the identity primitive swaps:

  v0.0.x: ed25519 for keypair + signing, SHA-256 for fingerprint.
  v0.1:    secp256k1 for keypair + signing, Keccak-256 for fingerprint
           and Ethereum address derivation (with EIP-55 checksum).

The reason for the swap is interoperability with the existing agent
ecosystem (ERC-8004 IdentityRegistry, x402, EVM-based payment rails).
A Soul's identity in v0.1 IS an Ethereum-compatible secp256k1 keypair.

A v0.1 Soul therefore has TWO identifiers:
- `fingerprint` — a 20-byte SHA-256 truncation, kept for compatibility
  with the v0 Soul SDK's identifier shape. Hex, 40 chars.
- `ethereum_address` — a 20-byte Keccak-256 truncation with EIP-55
  mixed-case checksum. Hex, 40 chars, 0x-prefixed. This is the
  identifier visible on-chain.

NOT YET in this file:
- M-of-N threshold signing (v0.1 design)
- ERC-8004 registration (separate module, see plan)
- x402 payment integration (separate module, see plan)
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

from reliquary.keccak import keccak256, eip55_checksum

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
    no 0x04 prefix). Keccak-256 of this gives the Ethereum address;
    SHA-256 of this gives the (legacy v0-compatible) fingerprint."""
    raw = pub.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint,
    )
    assert raw[0] == 0x04, "expected uncompressed point to start with 0x04"
    return raw[1:]  # 64 bytes (32 X + 32 Y)


def fingerprint(pub: ec.EllipticCurvePublicKey) -> str:
    """Compute the Soul's v0-compatible fingerprint.

    v0.1: SHA-256 of the public key, hex-encoded, first 20
    bytes shown (40 hex chars). 20 bytes is a deliberate choice to
    match Ethereum address length, so the two identifiers have the
    same shape even though they hash differently.

    For the canonical on-chain identifier, use `ethereum_address()`.
    """
    pub_b = public_key_bytes(pub)
    h = hashlib.sha256(pub_b).digest()
    return h[:20].hex()


def ethereum_address(pub: ec.EllipticCurvePublicKey, checksum: bool = True) -> str:
    """Derive the Soul's Ethereum address from its public key.

    Algorithm (per the Ethereum yellow paper and EIP-55):
        1. Take the 64-byte raw form of the uncompressed public key
           (X || Y, no 0x04 prefix).
        2. Compute Keccak-256 of those 64 bytes.
        3. Take the last 20 bytes of the digest.
        4. If `checksum` is True, apply EIP-55 mixed-case encoding.
        5. Return "0x" + hex.

    EIP-55 gives the address a built-in checksum: any mixed-case
    variant of an address can be checked by re-deriving its casing from
    keccak256 of the lowercase hex. Mistyped letters are caught.

    Verified against the canonical test vector: private key 0x...01
    yields `0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf`.
    """
    pub_b = public_key_bytes(pub)
    h = keccak256(pub_b)
    raw_addr = h[-20:]
    hex_part = eip55_checksum(raw_addr) if checksum else raw_addr.hex()
    return "0x" + hex_part


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
# Full Soul identity object — the v0.1 dataclass.
# ---------------------------------------------------------------------------


@dataclass
class SoulV1:
    """A v0.1 Soul — secp256k1-based identity with Ethereum address.

    A v0.1 Soul carries both:
    - `fingerprint_hex`: a 20-byte SHA-256 truncation (v0-compatible)
    - `ethereum_address`: a 20-byte Keccak-256 truncation with EIP-55
      checksum, 0x-prefixed. This is the on-chain identifier.
    """
    fingerprint_hex: str
    ethereum_address: str
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
            ethereum_address=ethereum_address(pub),
            private_key=priv,
            public_key=pub,
        )

    @classmethod
    def from_private_key_bytes(cls, raw: bytes) -> "SoulV1":
        """Restore a v0.1 Soul from 32 raw secp256k1 bytes (Ethereum format)."""
        priv = load_private_key(raw)
        pub = priv.public_key()
        return cls(
            fingerprint_hex=fingerprint(pub),
            ethereum_address=ethereum_address(pub),
            private_key=priv,
            public_key=pub,
        )

    def sign(self, message: bytes) -> bytes:
        return sign(self.private_key, message)

    def verify(self, signature: bytes, message: bytes) -> bool:
        return verify(self.public_key, signature, message)

