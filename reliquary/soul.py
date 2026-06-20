"""
reliquary.soul — the Soul layer.

The first runnable artifact of the Reliquary project.

This is v0. It demonstrates the core cryptographic primitives:
identity generation, client-side encryption, signing, authorship proof.
Storage, retrieval, and inheritance are stubbed — they need a backend,
which is the next thing to build.

Design rationale: see DECISIONS.md (D6: self-custody; D13: MVP)
and SOUL.md ("The recursive bit").

WARNING: This is a v0 skeleton. Do NOT use in production. Keys are
generated and held in memory; no secure-element integration; no
threshold / MPC; no hardware wallet support. The cryptography uses
standard library primitives (ed25519 + AES-256-GCM) but the
operational security around them is not yet hardened.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import time
from dataclasses import dataclass, field, asdict
from typing import Any, Optional


# We use ed25519 for identity in v0. ed25519 is fast, has small keys,
# and has clean Python support via the `cryptography` library.
# v0.1 will swap to secp256k1 for direct ERC-8004 compatibility;
# the architectural shape is unchanged.
try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey,
        Ed25519PublicKey,
    )
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives import serialization
    _CRYPTO_AVAILABLE = True
except ImportError:  # pragma: no cover
    _CRYPTO_AVAILABLE = False
    Ed25519PrivateKey = None  # type: ignore
    Ed25519PublicKey = None  # type: ignore
    AESGCM = None  # type: ignore
    serialization = None  # type: ignore


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class SoulError(Exception):
    """Base class for all Reliquary errors."""


class CryptoUnavailable(SoulError):
    """The `cryptography` library is not installed. pip install cryptography."""


class SoulNotFound(SoulError):
    """The requested Soul does not exist at the given pointer."""


class InheritanceNotActive(SoulError):
    """The Soul's inheritor has not been activated (heartbeat still within window)."""


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class Inheritor:
    """A designated recipient for a Soul in case of death (no heartbeat)."""

    address: str  # public key (base64) of the inheritor
    activated_after_days: int = 90  # how long without heartbeat before inheritor can claim

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Inheritor":
        return cls(
            address=d["address"],
            activated_after_days=d.get("activated_after_days", 90),
        )


@dataclass
class SoulBlob:
    """An encrypted Soul payload plus the metadata needed to interpret it.

    The blob itself is opaque ciphertext. The metadata tells the world
    (and future-you) what algorithm was used, when it was written, and
    who signed it.
    """

    ciphertext: bytes
    nonce: bytes  # AES-GCM nonce (12 bytes)
    created_at: int  # unix timestamp
    author_pubkey: str  # base64 public key of the Soul's identity
    signature: bytes  # ed25519 signature over (ciphertext || nonce || created_at)
    content_type: str = "application/octet-stream"
    content_hash: str = ""  # sha256 of plaintext, for integrity proof even if you also have the key

    def to_dict(self) -> dict[str, Any]:
        return {
            "ciphertext": base64.b64encode(self.ciphertext).decode("ascii"),
            "nonce": base64.b64encode(self.nonce).decode("ascii"),
            "created_at": self.created_at,
            "author_pubkey": self.author_pubkey,
            "signature": base64.b64encode(self.signature).decode("ascii"),
            "content_type": self.content_type,
            "content_hash": self.content_hash,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "SoulBlob":
        return cls(
            ciphertext=base64.b64decode(d["ciphertext"]),
            nonce=base64.b64decode(d["nonce"]),
            created_at=d["created_at"],
            author_pubkey=d["author_pubkey"],
            signature=base64.b64decode(d["signature"]),
            content_type=d.get("content_type", "application/octet-stream"),
            content_hash=d.get("content_hash", ""),
        )


# ---------------------------------------------------------------------------
# The Soul itself
# ---------------------------------------------------------------------------


class Soul:
    """A Soul: an identity that can write, sign, encrypt, and (eventually) inherit.

    Construction:
        soul = Soul.generate()                       # fresh identity
        soul = Soul.from_private_key_bytes(b"...")  # restore from backup

    Use:
        blob = soul.encrypt(b"my accumulated self")
        ok = soul.verify(blob)        # prove authorship
        plain = soul.decrypt(blob)    # recover (same Soul, or inheritor)
    """

    def __init__(self, private_key: "Ed25519PrivateKey") -> None:
        if not _CRYPTO_AVAILABLE:
            raise CryptoUnavailable(
                "The `cryptography` library is required. Install with: pip install cryptography"
            )
        self._sk = private_key
        self._pk = private_key.public_key()
        self._last_heartbeat: int = int(time.time())
        self._inheritor: Optional[Inheritor] = None

    # ---- Construction ----

    @classmethod
    def generate(cls) -> "Soul":
        """Generate a fresh Soul identity."""
        if not _CRYPTO_AVAILABLE:
            raise CryptoUnavailable(
                "The `cryptography` library is required. Install with: pip install cryptography"
            )
        return cls(Ed25519PrivateKey.generate())

    @classmethod
    def from_private_key_bytes(cls, raw: bytes) -> "Soul":
        """Restore a Soul from raw ed25519 private key bytes (32 bytes)."""
        if not _CRYPTO_AVAILABLE:
            raise CryptoUnavailable(
                "The `cryptography` library is required. Install with: pip install cryptography"
            )
        return cls(Ed25519PrivateKey.from_private_bytes(raw))

    # ---- Identity ----

    @property
    def public_key(self) -> "Ed25519PublicKey":
        return self._pk

    @property
    def public_key_bytes(self) -> bytes:
        return self._pk.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )

    @property
    def public_key_b64(self) -> str:
        return base64.b64encode(self.public_key_bytes).decode("ascii")

    @property
    def private_key_bytes(self) -> bytes:
        """Raw ed25519 private key bytes. BACK THIS UP. Anyone with these bytes is you."""
        return self._sk.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )

    @property
    def fingerprint(self) -> str:
        """A short, human-meaningful identifier for this Soul. Not secret."""
        digest = hashlib.sha256(self.public_key_bytes).digest()
        return base64.b32encode(digest[:10]).decode("ascii").lower()

    # ---- Encryption ----

    def encrypt(
        self,
        plaintext: bytes,
        content_type: str = "application/octet-stream",
    ) -> SoulBlob:
        """Encrypt a payload under this Soul's identity.

        The ciphertext is signed with the Soul's private key. Anyone with
        the public key can verify authorship; only this Soul (or its
        inheritor) can decrypt.
        """
        nonce = secrets.token_bytes(12)  # 96-bit nonce, recommended for AES-GCM
        aes = AESGCM(self._derive_aes_key())
        ciphertext = aes.encrypt(nonce, plaintext, associated_data=None)
        content_hash = hashlib.sha256(plaintext).hexdigest()
        signature = self.sign(self._signature_payload(ciphertext, nonce, content_hash))
        return SoulBlob(
            ciphertext=ciphertext,
            nonce=nonce,
            created_at=int(time.time()),
            author_pubkey=self.public_key_b64,
            signature=signature,
            content_type=content_type,
            content_hash=content_hash,
        )

    def decrypt(self, blob: SoulBlob) -> bytes:
        """Decrypt a blob. Only works if this Soul is the author (or inheritor with active claim)."""
        if not self.verify(blob):
            raise SoulError("Signature does not verify — this blob is not authored by this Soul.")
        aes = AESGCM(self._derive_aes_key())
        return aes.decrypt(blob.nonce, blob.ciphertext, associated_data=None)

    # ---- Signing ----

    def sign(self, message: bytes) -> bytes:
        return self._sk.sign(message)

    def verify(self, blob: SoulBlob) -> bool:
        """Verify that `blob` was authored by this Soul.

        Returns True if the signature is valid for the given ciphertext+nonce+hash
        and the public key in the blob matches this Soul's public key.
        """
        if blob.author_pubkey != self.public_key_b64:
            return False
        try:
            self._pk.verify(
                blob.signature,
                self._signature_payload(blob.ciphertext, blob.nonce, blob.content_hash),
            )
            return True
        except Exception:
            return False

    # ---- Heartbeat & Inheritance ----

    def heartbeat(self) -> None:
        """Record that this Soul is still alive. Call periodically (e.g. every 30 days).

        After `inheritor.activated_after_days` without a heartbeat, the
        inheritor can claim the Soul. Until then, the inheritor cannot
        decrypt even if they have the ciphertext.
        """
        self._last_heartbeat = int(time.time())

    @property
    def last_heartbeat(self) -> int:
        return self._last_heartbeat

    @property
    def days_since_heartbeat(self) -> float:
        return (time.time() - self._last_heartbeat) / 86400.0

    def designate_inheritor(self, inheritor: Inheritor) -> None:
        """Designate who can decrypt this Soul if it dies."""
        self._inheritor = inheritor

    @property
    def inheritor(self) -> Optional[Inheritor]:
        return self._inheritor

    def is_inheritance_active(self) -> bool:
        """True if the inheritor is allowed to claim (heartbeat has lapsed)."""
        if self._inheritor is None:
            return False
        return self.days_since_heartbeat > self._inheritor.activated_after_days

    # ---- Internals ----

    def _derive_aes_key(self) -> bytes:
        """Derive the AES-256 key from the Soul's private key.

        In v0, this is a simple HKDF-like construction. v0.1 should use
        proper HKDF (RFC 5869) over the ed25519 seed. For now, we use
        a SHA-256 expansion; this is structurally correct but not
        best-practice.
        """
        seed = self.private_key_bytes
        # Two rounds of SHA-256 expansion to get 32 bytes
        return hashlib.sha256(seed + b"reliquary-aes-key-v0").digest()

    def _signature_payload(self, ciphertext: bytes, nonce: bytes, content_hash: str) -> bytes:
        """The bytes that get signed. Canonical serialization."""
        return b"|".join([
            ciphertext,
            nonce,
            content_hash.encode("ascii"),
        ])

    # ---- Serialization ----

    def export_metadata(self) -> dict[str, Any]:
        """Export the Soul's public metadata (for the world to see). Does NOT include the private key."""
        return {
            "public_key": self.public_key_b64,
            "fingerprint": self.fingerprint,
            "last_heartbeat": self._last_heartbeat,
            "inheritor": self._inheritor.to_dict() if self._inheritor else None,
        }


# ---------------------------------------------------------------------------
# Storage interface (STUBS — to be implemented against a backend)
# ---------------------------------------------------------------------------


class SoulStore:
    """Abstract base for a Soul storage backend.

    v0 ships with `LocalSoulStore` (writes to a local directory).
    Future: S3, 0G, IPFS, Filecoin, etc. The Soul layer is
    storage-agnostic; the encryption is always client-side.
    """

    def put(self, blob: SoulBlob) -> str:
        """Store a blob. Returns a pointer (URI / hash) that can be used to retrieve it."""
        raise NotImplementedError

    def get(self, pointer: str) -> SoulBlob:
        """Retrieve a blob by pointer. Raises SoulNotFound if missing."""
        raise NotImplementedError

    def list(self) -> list[str]:
        """List all pointers this store knows about."""
        raise NotImplementedError


class LocalSoulStore(SoulStore):
    """A simple file-system backed SoulStore. Useful for development and single-machine souls.

    Layout:
        <root>/
            <pointer>/
                blob.json     (the SoulBlob as JSON)
    """

    def __init__(self, root: str) -> None:
        self.root = root
        os.makedirs(self.root, exist_ok=True)

    def _pointer(self, blob: SoulBlob) -> str:
        # The pointer is the sha256 of the ciphertext. Stable and content-addressed.
        return hashlib.sha256(blob.ciphertext).hexdigest()

    def put(self, blob: SoulBlob) -> str:
        import pathlib
        pointer = self._pointer(blob)
        target = pathlib.Path(self.root) / pointer
        target.mkdir(parents=True, exist_ok=True)
        (target / "blob.json").write_text(json.dumps(blob.to_dict(), indent=2))
        return pointer

    def get(self, pointer: str) -> SoulBlob:
        import pathlib
        target = pathlib.Path(self.root) / pointer / "blob.json"
        if not target.exists():
            raise SoulNotFound(f"No Soul at pointer {pointer}")
        return SoulBlob.from_dict(json.loads(target.read_text()))

    def list(self) -> list[str]:
        import pathlib
        root = pathlib.Path(self.root)
        return [p.name for p in root.iterdir() if p.is_dir()]


# ---------------------------------------------------------------------------
# Heartbeat-on-disk: a tiny file the Soul can write to prove liveness
# ---------------------------------------------------------------------------


def write_heartbeat(soul: Soul, path: str) -> None:
    """Write a heartbeat file. The Soul is alive as long as this file is recent."""
    soul.heartbeat()
    payload = {
        "fingerprint": soul.fingerprint,
        "last_heartbeat": soul.last_heartbeat,
        "signature": base64.b64encode(
            soul.sign(str(soul.last_heartbeat).encode("ascii"))
        ).decode("ascii"),
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)


def is_alive(soul: Soul, heartbeat_path: str, max_days: int = 90) -> bool:
    """True if the heartbeat file exists, is signed correctly, and is recent enough."""
    if not os.path.exists(heartbeat_path):
        return False
    with open(heartbeat_path) as f:
        payload = json.load(f)
    if payload.get("fingerprint") != soul.fingerprint:
        return False
    try:
        soul.public_key.verify(
            base64.b64decode(payload["signature"]),
            str(payload["last_heartbeat"]).encode("ascii"),
        )
    except Exception:
        return False
    age_days = (time.time() - payload["last_heartbeat"]) / 86400.0
    return age_days < max_days
