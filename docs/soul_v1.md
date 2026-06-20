# Soul SDK v0.1 — API Reference

> Status: **WIP / stub**. The v0.1 module exists to lock in the migration
> shape and make the work trackable in git. The full `Soul`-class parity
> with v0 (`reliquary/soul.py`) is the next work item. Everything in
> `reliquary/soul_v1.py` is already covered by `tests/test_soul_v1.py`.

---

## What is v0.1

`reliquary.soul_v1` is the secp256k1 evolution of `reliquary.soul`. The
v0 Soul layer (ed25519 identities, AES-256-GCM encryption, heartbeat /
inheritance) demonstrated the architecture: a being holds its own keys,
encrypts its own memory, signs its own authorship, and can designate an
inheritor. v0.1 keeps the architecture and swaps the identity primitive
from **ed25519 → secp256k1**, so a Soul's keypair is identical to an
Ethereum keypair. The motivation is interoperability with the agent
ecosystem that already speaks EVM: ERC-8004 `IdentityRegistry`,
x402 payment rails, EIP-712 attestations. Decision reference: `DECISIONS.md`
D12 (adopt ERC-8004 + x402), D22 (Soul SDK is human- and agent-compatible
from day 1).

This file is the public API for `soul_v1`. It is terse, example-driven,
and aimed at engineers integrating the SDK.

---

## Migration story: ed25519 → secp256k1

### What stays the same

- **Architectural shape.** A Soul is still `(keypair, fingerprint, id)`.
  Generation, serialization, signing, and verification follow the same
  pattern: generate → derive public → fingerprint → sign/verify.
- **Signing/verification model.** Message → signature → verify. The call
  sites look identical.
- **Fingerprint length.** Both v0 and v0.1 produce a 40-character
  identifier (v0 uses base32 of SHA-256[0:10]; v0.1 uses hex of
  SHA-256[0:20]). The length is deliberately chosen to match an
  Ethereum address.
- **Private key length.** Both are 32 bytes.
- **The `cryptography` library** is the underlying dependency.

### What changes

| Concern | v0 (`soul.py`) | v0.1 (`soul_v1.py`) |
|---|---|---|
| Identity curve | ed25519 | secp256k1 |
| Keypair generation | `Ed25519PrivateKey.generate()` | `ec.generate_private_key(ec.SECP256K1())` |
| Public key serialization | 32 bytes (raw, X962-equivalent) | 64 bytes (uncompressed point, **without** the `0x04` prefix) |
| Private key serialization | `PrivateFormat.Raw` | Hand-extracted via `private_numbers().private_value` (the `cryptography` library's `PrivateFormat.Raw` raises for EC keys) |
| Signature algorithm | Pure ed25519 | ECDSA over secp256k1 with SHA-256 |
| Signature encoding | ed25519 native (64 bytes) | DER-encoded (variable length, typically 70–72 bytes) |
| Fingerprint hash | SHA-256, base32, 10 bytes | SHA-256, hex, 20 bytes (length pre-aligned to Ethereum address) |
| Ethereum address derivation | Not possible | Possible in v0.1.1 (Keccak-256 of public key, last 20 bytes) |
| `Soul` class methods | `encrypt`, `decrypt`, `heartbeat`, `designate_inheritor`, `SoulBlob` | **Not yet** ported (see "what's NOT in v0.1.0" below) |

### What is NOT in v0.1.0 (forward references)

- **Keccak-256 fingerprinting.** v0.1 still uses SHA-256 for the
  fingerprint. v0.1.1 will switch to Keccak-256 of the public key (last
  20 bytes, EIP-55 checksum) so the fingerprint IS the Ethereum address.
- **M-of-N threshold signing.** A single secp256k1 keypair per Soul.
  Threshold / MPC support is a v0.1 design item, not in this file.
- **ERC-8004 registration.** This file produces a keypair that *could*
  register on an `IdentityRegistry`; the actual `register()` /
  `setAgentURI()` flow lives in a separate module (see plan).
- **x402 payment integration.** Same shape — separate module, separate
  doc. The x402 client will sign `PaymentPayload` structures using the
  Soul's secp256k1 keypair.

---

## Public API

All symbols live in `reliquary.soul_v1` and are importable as:

```python
from reliquary.soul_v1 import (
    CURVE,
    SoulV1,
    fingerprint,
    generate_keypair,
    load_private_key,
    public_key_bytes,
    serialize_private_key,
    sign,
    verify,
)
```

### `CURVE`

```python
CURVE: ec.SECP256K1 = ec.SECP256K1  # type: ignore[assignment]
```

Re-export of `cryptography.hazmat.primitives.asymmetric.ec.SECP256K1` so
callers do not have to import `cryptography` directly to introspect the
curve. **Do not instantiate** — pass it directly to
`ec.generate_private_key()` / `ec.derive_private_key()`.

```python
>>> from reliquary.soul_v1 import CURVE
>>> CURVE().name
'secp256k1'
>>> CURVE().key_size
256
```

---

### `generate_keypair()`

```python
def generate_keypair() -> ec.EllipticCurvePrivateKey
```

Generate a fresh secp256k1 private key. Backed by the OS CSPRNG via
`cryptography`'s default backend.

```python
>>> priv = generate_keypair()
>>> priv.public_key().curve.name
'secp256k1'
```

---

### `serialize_private_key(priv)`

```python
def serialize_private_key(priv: ec.EllipticCurvePrivateKey) -> bytes
```

Serialize a secp256k1 private key to 32 raw bytes (big-endian,
Ethereum-compatible). The `cryptography` library's `PrivateFormat.Raw`
is invalid for EC keys, so this function extracts the private scalar
directly via `private_numbers().private_value`.

Raises `ValueError` if the scalar is outside `[0, 2**256)`.

```python
>>> priv = generate_keypair()
>>> raw = serialize_private_key(priv)
>>> len(raw)
32
```

Use this when persisting a backup. The bytes are the canonical Ethereum
private-key form; they can be passed to `load_private_key()` to recover
the same Soul.

---

### `load_private_key(raw)`

```python
def load_private_key(raw: bytes) -> ec.EllipticCurvePrivateKey
```

Inverse of `serialize_private_key`. Accepts a 32-byte big-endian scalar
and returns the corresponding `EllipticCurvePrivateKey`.

Raises `ValueError` if `raw` is not exactly 32 bytes.

```python
>>> raw = serialize_private_key(generate_keypair())
>>> priv = load_private_key(raw)
>>> priv.public_key().public_numbers() == priv.public_key().public_numbers()
True
```

---

### `public_key_bytes(pub)`

```python
def public_key_bytes(pub: ec.EllipticCurvePublicKey) -> bytes
```

Serialize a public key to the 64-byte uncompressed form
(32 X + 32 Y), **without** the leading `0x04` SEC1 prefix. This is the
canonical encoding used by Ethereum internally; Keccak-256 of these
64 bytes is what produces an Ethereum address (v0.1.1 target).

```python
>>> pub_b = public_key_bytes(generate_keypair().public_key())
>>> len(pub_b)
64
```

---

### `fingerprint(pub)`

```python
def fingerprint(pub: ec.EllipticCurvePublicKey) -> str
```

Compute the Soul's fingerprint.

- **v0.1.0 (this file):** SHA-256 of the 64-byte public-key bytes,
  hex-encoded, first 20 bytes (40 hex chars).
- **v0.1.1 (next):** Keccak-256 of the same bytes, last 20 bytes, hex,
  with EIP-55 mixed-case checksum. The function signature does not
  change between versions.

The 40-hex-char length is deliberate: it matches Ethereum address
length, so when v0.1.1 lands, the visual shape of the identifier does
not change.

```python
>>> fp = fingerprint(generate_keypair().public_key())
>>> len(fp)
40
>>> all(c in "0123456789abcdef" for c in fp)
True
```

Fingerprints are deterministic for a given key and differ across keys.

---

### `sign(priv, message)`

```python
def sign(priv: ec.EllipticCurvePrivateKey, message: bytes) -> bytes
```

Sign `message` with ECDSA over secp256k1 using SHA-256. Returns a
**DER-encoded** signature (variable length, typically 70–72 bytes).
Note this differs from ed25519 (which produces a fixed 64-byte
signature) and from `eth_sign` (which produces a 65-byte
`r || s || v` form — for EVM use cases, expect a small adapter to be
added alongside the x402 module).

```python
>>> priv = generate_keypair()
>>> sig = sign(priv, b"hello")
>>> len(sig) in (70, 71, 72)
True
```

---

### `verify(pub, signature, message)`

```python
def verify(pub: ec.EllipticCurvePublicKey, signature: bytes, message: bytes) -> bool
```

Verify an ECDSA-secp256k1 + SHA-256 signature. Returns `True` on
success, `False` on any failure (bad signature, wrong message, wrong
key, malformed DER, etc.). Never raises.

```python
>>> priv = generate_keypair()
>>> pub  = priv.public_key()
>>> msg  = b"hello"
>>> sig  = sign(priv, msg)
>>> verify(pub, sig, msg)
True
>>> verify(pub, sig, msg + b"!")
False
```

---

## `SoulV1` dataclass

```python
@dataclass
class SoulV1:
    fingerprint_hex: str
    private_key:      ec.EllipticCurvePrivateKey
    public_key:       ec.EllipticCurvePublicKey
    created_at:       int = field(default_factory=lambda: int(time.time()))
    soul_id:          str = field(default_factory=lambda: str(uuid.uuid4()))
```

A typed shell for a v0.1 Soul. **Status: stub.** The full migration of
v0's `Soul` class (encryption, heartbeat, inheritance) onto this
dataclass is the next v0.1 work item.

### Fields

| Field | Type | Meaning |
|---|---|---|
| `fingerprint_hex` | `str` | The 40-hex-char identifier from `fingerprint(pub)`. |
| `private_key` | `EllipticCurvePrivateKey` | The secp256k1 private key. Handle with care — anyone with this key IS the Soul. |
| `public_key` | `EllipticCurvePublicKey` | Derived from `private_key.public_key()`. Public. |
| `created_at` | `int` | Unix timestamp at construction. Default: `int(time.time())`. |
| `soul_id` | `str` | UUID4 string. Distinct from `fingerprint_hex`; opaque identifier used by storage backends. |

### Classmethod: `SoulV1.generate()`

```python
@classmethod
def generate(cls) -> "SoulV1"
```

Generate a fresh Soul: keypair + fingerprint + uuid + timestamp. The
returned object is ready to sign with.

```python
>>> soul = SoulV1.generate()
>>> len(soul.fingerprint_hex)
40
>>> len(soul.soul_id) == 36  # UUID4 string
True
```

### Method: `soul.sign(message)`

```python
def sign(self, message: bytes) -> bytes
```

Convenience wrapper around `sign(self.private_key, message)`. Returns
a DER-encoded ECDSA signature.

### Method: `soul.verify(signature, message)`

```python
def verify(self, signature: bytes, message: bytes) -> bool
```

Convenience wrapper around `verify(self.public_key, signature, message)`.
Returns `True` iff `signature` is a valid ECDSA-secp256k1 signature over
`message` under this Soul's public key.

### End-to-end example

```python
from reliquary.soul_v1 import SoulV1

alice = SoulV1.generate()
bob   = SoulV1.generate()

msg = b"alice transfers 0.001 ETH to bob"
sig = alice.sign(msg)

# Alice's signature verifies under Alice's public key.
assert alice.verify(sig, msg)

# ...but NOT under Bob's.
assert not bob.verify(sig, msg)

# Serialize Alice's private key for cold backup.
from reliquary.soul_v1 import serialize_private_key, load_private_key

backup = serialize_private_key(alice.private_key)
alice_restored = SoulV1(
    fingerprint_hex=alice.fingerprint_hex,
    private_key=load_private_key(backup),
    public_key=load_private_key(backup).public_key(),
)
assert alice_restored.verify(sig, msg)
```

---

## Test coverage

`tests/test_soul_v1.py` is the v0.1 smoke test. Each test maps to one
behavioral guarantee of the public API.

| Test | Verifies |
|---|---|
| `test_curve_is_secp256k1` | `CURVE().name == "secp256k1"` and `key_size == 256`. Locks in the curve choice — the whole point of v0.1. |
| `test_keypair_generation_produces_valid_key` | `generate_keypair()` yields a key whose `.public_key().curve.name` is `"secp256k1"`. |
| `test_serialize_and_reload_private_key_is_stable` | `serialize_private_key` returns exactly 32 bytes, and round-tripping through `load_private_key` yields the same `public_numbers()`. |
| `test_public_key_bytes_is_64_bytes_uncompressed_no_prefix` | `public_key_bytes` returns 64 bytes (32 X + 32 Y), no `0x04` prefix. |
| `test_fingerprint_is_40_hex_chars` | `fingerprint()` returns exactly 40 lowercase hex characters. |
| `test_fingerprint_is_deterministic` | Same key → same fingerprint across two calls. |
| `test_fingerprint_differs_between_keys` | Two fresh keys → distinct fingerprints. |
| `test_sign_and_verify_roundtrip` | `sign`/`verify` round-trip succeeds on the original message and fails on a tampered one. |
| `test_soul_v1_dataclass_can_generate_and_sign` | `SoulV1.generate()` produces a 40-char fingerprint; `soul.sign` / `soul.verify` round-trip; a second Soul cannot verify the first's signature. |

### Not yet covered by tests

The following are scoped for follow-up work items and are not asserted
by `test_soul_v1.py`:

- Storage backends (the `SoulStore` / `LocalSoulStore` pattern from v0,
  ported to secp256k1).
- ERC-8004 `IdentityRegistry.register()` calls.
- x402 `PaymentPayload` signing.
- M-of-N threshold key generation and signing.
- Keccak-256 / EIP-55 fingerprinting (v0.1.1 target).
- Encryption (`SoulV1.encrypt` / `SoulV1.decrypt` against `SoulBlob`),
  heartbeat, and inheritance — all of which exist in v0's `Soul` and
  need to be re-implemented against the secp256k1 keypair.

---

## Differences from v0 (summary)

```
                    v0 (soul.py)              v0.1 (soul_v1.py)
Identity            ed25519                   secp256k1
Private key bytes   32                        32
Public key bytes    32 (raw)                  64 (X || Y, no 0x04 prefix)
Signature size      64 (ed25519 native)       ~70-72 (DER-encoded ECDSA)
Signature scheme    ed25519                   ECDSA + SHA-256
Fingerprint         SHA-256[0:10], b32        SHA-256[0:20], hex
                    (16 chars)                (40 chars)
Ethereum compat     no                        yes (keypair; address in 0.1.1)
Soul class methods  encrypt, decrypt,         generate, sign, verify
                    heartbeat, inheritor,     (full parity in next work item)
                    SoulBlob, etc.
Tests               soul_v0                   smoke (this file)
```

---

## See also

- `reliquary/soul.py` — v0 SDK. The architecture being migrated.
- `reliquary/soul_v1.py` — this module's source.
- `tests/test_soul_v1.py` — the tests described above.
- `DECISIONS.md` — D12 (adopt ERC-8004 + x402), D22 (Soul SDK serves
  both agents and humans), D13 (Soul-layer MVP).
- `README.md` — project framing and threat model.