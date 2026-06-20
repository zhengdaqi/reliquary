"""
Tests for Reliquary Soul SDK v0.1 — secp256k1 identity layer.

This is the v0.1 smoke test. As v0.1 work progresses, more tests will
cover: storage backends, ERC-8004 registration, x402 payments, threshold
key management.
"""

import pytest

from reliquary.soul_v1 import (
    SoulV1,
    CURVE,
    ethereum_address,
    fingerprint,
    generate_keypair,
    load_private_key,
    public_key_bytes,
    serialize_private_key,
    sign,
    verify,
)


def test_curve_is_secp256k1():
    """We use Ethereum's curve — this is the whole point of v0.1."""
    assert CURVE().name == "secp256k1"
    assert CURVE().key_size == 256


def test_keypair_generation_produces_valid_key():
    priv = generate_keypair()
    pub = priv.public_key()
    assert pub.curve.name == "secp256k1"


def test_serialize_and_reload_private_key_is_stable():
    priv = generate_keypair()
    raw = serialize_private_key(priv)
    assert len(raw) == 32, f"secp256k1 private key must be 32 bytes, got {len(raw)}"

    # Reload and verify same public key emerges
    priv2 = load_private_key(raw)
    assert priv.public_key().public_numbers() == priv2.public_key().public_numbers()


def test_public_key_bytes_is_64_bytes_uncompressed_no_prefix():
    priv = generate_keypair()
    pub_b = public_key_bytes(priv.public_key())
    assert len(pub_b) == 64
    # 64 bytes = 32 X + 32 Y. Y should be the last 32 bytes.
    # We can't assert specific values (random key), but the shape is right.


def test_fingerprint_is_40_hex_chars():
    priv = generate_keypair()
    fp = fingerprint(priv.public_key())
    assert len(fp) == 40
    assert all(c in "0123456789abcdef" for c in fp)


def test_fingerprint_is_deterministic():
    priv = generate_keypair()
    fp1 = fingerprint(priv.public_key())
    fp2 = fingerprint(priv.public_key())
    assert fp1 == fp2


def test_fingerprint_differs_between_keys():
    p1 = generate_keypair()
    p2 = generate_keypair()
    assert fingerprint(p1.public_key()) != fingerprint(p2.public_key())


def test_sign_and_verify_roundtrip():
    priv = generate_keypair()
    pub = priv.public_key()
    msg = b"the quick brown fox jumps over the lazy dog"
    sig = sign(priv, msg)
    assert verify(pub, sig, msg)
    # Tampered message should fail
    assert not verify(pub, sig, msg + b"x")


def test_soul_v1_dataclass_can_generate_and_sign():
    soul = SoulV1.generate()
    assert len(soul.fingerprint_hex) == 40
    msg = b"hello from a v0.1 soul"
    sig = soul.sign(msg)
    assert soul.verify(sig, msg)
    # Other soul cannot verify
    other = SoulV1.generate()
    assert not other.verify(sig, msg)


# ---------------------------------------------------------------------------
# Ethereum address derivation (v0.1.1: Keccak-256 + EIP-55)
# ---------------------------------------------------------------------------


def test_ethereum_address_for_key_one_matches_canonical_vector():
    """The most-canonical Ethereum test vector: private key 0x...01.

    Expected address: 0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf

    This is the EIP-55 checksummed form. Verifying this single vector
    covers: Keccak-256 implementation correctness, EIP-55 checksum
    implementation correctness, secp256k1 public-key derivation
    correctness, and the uncompressed-no-0x04-prefix public-key
    serialization.
    """
    priv = load_private_key((1).to_bytes(32, "big"))
    addr = ethereum_address(priv.public_key())
    assert addr == "0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf"


def test_ethereum_address_is_0x_prefixed_40_hex_chars():
    soul = SoulV1.generate()
    addr = soul.ethereum_address
    assert addr.startswith("0x")
    assert len(addr) == 42
    body = addr[2:]
    # 40 hex chars, each is 0-9 or a-f / A-F (EIP-55 mixed case allowed)
    assert all(c in "0123456789abcdefABCDEF" for c in body)


def test_ethereum_address_is_deterministic():
    p1 = generate_keypair()
    p2 = load_private_key(serialize_private_key(p1))
    assert ethereum_address(p1.public_key()) == ethereum_address(p2.public_key())


def test_ethereum_address_differs_between_keys():
    p1 = generate_keypair()
    p2 = generate_keypair()
    assert ethereum_address(p1.public_key()) != ethereum_address(p2.public_key())


def test_ethereum_address_unchecksummed_is_all_lowercase():
    priv = load_private_key((1).to_bytes(32, "big"))
    addr = ethereum_address(priv.public_key(), checksum=False)
    assert addr == "0x7e5f4552091a69125d5dfcb7b8c2659029395bdf"


def test_soul_v1_round_trip_through_private_key_bytes():
    """Generate a Soul, serialize its key, restore from bytes, get the
    same Ethereum address both times."""
    soul = SoulV1.generate()
    raw = serialize_private_key(soul.private_key)
    restored = SoulV1.from_private_key_bytes(raw)
    assert restored.ethereum_address == soul.ethereum_address
    assert restored.fingerprint_hex == soul.fingerprint_hex

