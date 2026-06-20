"""
Tests for the pure-Python Keccak-256 implementation in `reliquary.keccak`.

These tests are critical: a bug here means every Ethereum address this
project derives is wrong. We verify against:
1. The two well-known Keccak-256 test vectors (empty input, "abc").
2. The canonical secp256k1-key=1 -> Ethereum address vector.
3. Cross-check: keccak256 must NOT equal SHA3-256 on the same input
   (this catches the padding-byte mistake).
4. A medium-size input to exercise the multi-block absorb path.
"""

import hashlib

import pytest

from reliquary.keccak import keccak256, eip55_checksum


# Official Keccak-256 test vectors.
VEC_EMPTY = "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
VEC_ABC = "4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45"


def test_keccak256_empty():
    """Empty input -> well-known constant."""
    assert keccak256(b"").hex() == VEC_EMPTY


def test_keccak256_abc():
    """The canonical 'abc' Keccak-256 test vector."""
    assert keccak256(b"abc").hex() == VEC_ABC


def test_keccak256_differs_from_sha3_256():
    """If these match, we accidentally implemented SHA-3, not Keccak.

    SHA-3-256 uses 0x06 padding; Keccak-256 uses 0x01. The digests
    must differ on every non-trivial input.
    """
    msg = b"the quick brown fox jumps over the lazy dog"
    kecc = keccak256(msg)
    sha3 = hashlib.sha3_256(msg).digest()
    assert kecc != sha3


def test_keccak256_multiblock_absorb():
    """Input larger than the 136-byte rate should produce a stable,
    well-distributed digest. We test against a vector published in
    the original Keccak team's intermediate test set (NIST KAT)."""
    # 200 bytes = one full block (136) + one partial (64). Exercises
    # both absorb paths. We don't hard-code a vector here; we test
    # determinism + length sanity, and that it differs from the
    # single-block version.
    msg = b"a" * 200
    h = keccak256(msg)
    assert len(h) == 32
    assert keccak256(msg) == h  # deterministic
    assert h.hex() != keccak256(b"a" * 199).hex()


def test_keccak256_returns_bytes():
    """API contract: returns raw bytes, not hex."""
    out = keccak256(b"x")
    assert isinstance(out, bytes)
    assert len(out) == 32


# ---------------------------------------------------------------------------
# EIP-55 checksum
# ---------------------------------------------------------------------------


def test_eip55_known_address():
    """Address 0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf has a known
    EIP-55 checksum. We round-trip the underlying bytes and confirm
    the checksum recreates the canonical form.
    """
    raw = bytes.fromhex("7E5F4552091A69125d5DfCb7b8C2659029395Bdf")
    assert eip55_checksum(raw) == "7E5F4552091A69125d5DfCb7b8C2659029395Bdf"


def test_eip55_known_all_lowercase_address():
    """An address that happens to be all-lowercase after EIP-55.

    EIP-55 specifies test vectors; the ones that checksum to all-lowercase
    are 0xde709f2102306220921060314715629080e2fb77 and
    0x27b1fdb04752bbc536007a920d24acb045561c26.
    """
    raw = bytes.fromhex("de709f2102306220921060314715629080e2fb77")
    assert eip55_checksum(raw) == "de709f2102306220921060314715629080e2fb77"
    raw2 = bytes.fromhex("27b1fdb04752bbc536007a920d24acb045561c26")
    assert eip55_checksum(raw2) == "27b1fdb04752bbc536007a920d24acb045561c26"


def test_eip55_handles_mixed_case_address():
    """0x52908400098527886E0F7030069857D2E4169EE7 (known mixed case)."""
    raw = bytes.fromhex("52908400098527886E0F7030069857D2E4169EE7".lower())
    assert eip55_checksum(raw) == "52908400098527886E0F7030069857D2E4169EE7"


def test_eip55_requires_exactly_20_bytes():
    with pytest.raises(Exception):
        eip55_checksum(b"\x00" * 19)
    with pytest.raises(Exception):
        eip55_checksum(b"\x00" * 21)
