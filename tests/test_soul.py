"""
Tests for the Reliquary Soul SDK v0.

These are smoke tests, not exhaustive. They verify:
- Identity generation
- Encrypt + decrypt round-trip
- Signature verification (positive and negative)
- Heartbeat and inheritance logic
- Local store put/get round-trip

Run with:
    cd agent-vault
    pip install cryptography pytest
    pytest tests/
"""

from __future__ import annotations

import json
import os
import tempfile
import time
from pathlib import Path

import pytest

from reliquary.soul import (
    Soul,
    SoulBlob,
    LocalSoulStore,
    Inheritor,
    SoulError,
    write_heartbeat,
    is_alive,
)


def test_generate_creates_distinct_identities():
    a = Soul.generate()
    b = Soul.generate()
    assert a.public_key_b64 != b.public_key_b64
    assert a.fingerprint != b.fingerprint


def test_encrypt_decrypt_roundtrip():
    soul = Soul.generate()
    payload = b"hello, this is the accumulated self of an agent"
    blob = soul.encrypt(payload, content_type="text/plain")
    assert soul.verify(blob) is True
    recovered = soul.decrypt(blob)
    assert recovered == payload


def test_signature_verifies_only_for_author():
    soul_a = Soul.generate()
    soul_b = Soul.generate()
    blob = soul_a.encrypt(b"only soul a should be able to verify this")
    assert soul_a.verify(blob) is True
    # soul_b has a different public key, so the author_pubkey check fails first
    assert soul_b.verify(blob) is False


def test_decrypt_rejects_tampered_ciphertext():
    soul = Soul.generate()
    blob = soul.encrypt(b"do not tamper with me")
    tampered = SoulBlob(
        ciphertext=blob.ciphertext + b"\x00",  # flip a byte
        nonce=blob.nonce,
        created_at=blob.created_at,
        author_pubkey=blob.author_pubkey,
        signature=blob.signature,
        content_type=blob.content_type,
        content_hash=blob.content_hash,
    )
    with pytest.raises(SoulError):
        soul.decrypt(tampered)


def test_heartbeat_and_inheritance_lifecycle():
    soul = Soul.generate()
    soul.designate_inheritor(Inheritor(address="inheritor-pubkey-b64", activated_after_days=90))
    # Fresh soul: inheritor NOT active
    assert soul.is_inheritance_active() is False
    # Simulate death: rewind the heartbeat
    soul._last_heartbeat = int(time.time()) - (91 * 86400)
    # Now the inheritor CAN claim
    assert soul.is_inheritance_active() is True


def test_local_store_put_get_roundtrip(tmp_path: Path):
    soul = Soul.generate()
    store = LocalSoulStore(str(tmp_path / "store"))
    payload = b"the soul of an agent, encrypted at rest"
    blob = soul.encrypt(payload)
    pointer = store.put(blob)
    assert pointer in store.list()
    recovered_blob = store.get(pointer)
    assert soul.verify(recovered_blob)
    assert soul.decrypt(recovered_blob) == payload


def test_local_store_get_missing_raises(tmp_path: Path):
    store = LocalSoulStore(str(tmp_path / "store"))
    from reliquary.soul import SoulNotFound
    with pytest.raises(SoulNotFound):
        store.get("nonexistent")


def test_heartbeat_file_roundtrip(tmp_path: Path):
    soul = Soul.generate()
    hb_path = str(tmp_path / "hb.json")
    write_heartbeat(soul, hb_path)
    assert is_alive(soul, hb_path) is True


def test_heartbeat_for_wrong_soul_rejected(tmp_path: Path):
    soul_a = Soul.generate()
    soul_b = Soul.generate()
    hb_path = str(tmp_path / "hb.json")
    write_heartbeat(soul_a, hb_path)
    # soul_b should not be considered alive using soul_a's heartbeat
    assert is_alive(soul_b, hb_path) is False


def test_fingerprint_is_stable():
    soul = Soul.generate()
    fp1 = soul.fingerprint
    fp2 = soul.fingerprint
    assert fp1 == fp2
    # Different key, different fingerprint
    other = Soul.generate()
    assert other.fingerprint != fp1


def test_export_metadata_has_no_private_key():
    soul = Soul.generate()
    meta = soul.export_metadata()
    assert "public_key" in meta
    assert "fingerprint" in meta
    # Defense in depth: ensure the private key is not in the metadata
    serialized = json.dumps(meta)
    assert soul.private_key_bytes.hex() not in serialized
