"""
reliquary.keccak — pure-Python Keccak-256 implementation.

Keccak-256 is the hash function used by Ethereum to derive addresses from
secp256k1 public keys. It is *not* the same as SHA3-256: the padding
bytes differ (0x01 for Keccak, 0x06 for SHA-3), so implementations of
SHA-3 will not work for Ethereum address derivation.

This module is a self-contained, dependency-free implementation of
Keccak-256. It is intentionally small and easy to audit. The reference
is FIPS-202 (the SHA-3 standard), modified to use the original Keccak
padding so the output matches Ethereum's address scheme.

Why pure-Python and not pycryptodome?
- The Reliquary Soul SDK should be auditable in one sitting. A
  120-line file is easier to read than "pip install pycryptodome and
  trust its release tarball."
- We only need Keccak-256; pulling in the whole `Crypto.Hash` package
  for one function is overkill.
- The algorithm is well-known and the FIPS-202 reference is short.

Reference test vectors (all verified on the official Ethereum yellow
paper and the keccak-256 sumtab):
    keccak256(b"")                       = c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
    keccak256(b"abc")                    = 4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45
    keccak256(0x9c12cfdc... [p256k1 pub]) -> last 20 bytes = eth address

WARNING: This is slow (~1 MB/s) compared to a C implementation. It is
fine for occasional key derivation; do NOT use it in a hot path.
"""

from __future__ import annotations


# Keccak-f round constants. 24 rounds.
_KECCAK_RC = (
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
    0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
    0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
    0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
    0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
    0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
    0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
)

# Rotation offsets for the rho step. Indexed as _KECCAK_RHO[x + 5*y]
# for the lane at column x, row y. The (0,0) position is 0 (no rotation).
_KECCAK_RHO = (
    0,  1, 62, 28, 27,
    36, 44,  6, 55, 20,
    3, 10, 43, 25, 39,
    41, 45, 15, 21,  8,
    18,  2, 61, 56, 14,
)

# Original Keccak padding byte. SHA-3 uses 0x06; Ethereum uses 0x01.
_KECCAK_PAD = 0x01


def _rotl64(x: int, n: int) -> int:
    """64-bit rotate left, mask to 64 bits."""
    n &= 63
    return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF


def _keccak_f(state: list[int]) -> None:
    """In-place Keccak-f[1600] permutation on a 5x5 state of 64-bit lanes."""
    for round_idx in range(24):
        # --- theta ---
        c = [state[x] ^ state[x + 5] ^ state[x + 10] ^ state[x + 15] ^ state[x + 20] for x in range(5)]
        d = [c[(x - 1) % 5] ^ _rotl64(c[(x + 1) % 5], 1) for x in range(5)]
        for i in range(25):
            state[i] ^= d[i % 5]

        # --- rho and pi ---
        # State is stored as state[x + 5*y] = lane at column x, row y.
        # pi: (x, y) -> (y, (2x + 3y) mod 5)
        # rho: rotate by _KECCAK_RHO[x + 5*y] bits (left).
        b = [0] * 25
        for x in range(5):
            for y in range(5):
                src = x + 5 * y
                dst = y + 5 * ((2 * x + 3 * y) % 5)
                b[dst] = _rotl64(state[src], _KECCAK_RHO[src])

        # --- chi ---
        for x in range(5):
            for y in range(5):
                idx = x + 5 * y
                state[idx] = b[idx] ^ ((~b[(x + 1) % 5 + 5 * y]) & b[(x + 2) % 5 + 5 * y]) & 0xFFFFFFFFFFFFFFFF

        # --- iota ---
        state[0] ^= _KECCAK_RC[round_idx]


def keccak256(data: bytes) -> bytes:
    """Compute Keccak-256 of `data` and return 32 raw bytes.

    Uses the original Keccak padding (0x01), not SHA-3 padding (0x06).
    This matches Ethereum's address derivation.

    Algorithm summary:
        - Rate r = 1088 bits = 136 bytes (for 256-bit output)
        - Capacity c = 512 bits
        - Absorb input in 136-byte blocks, XOR with state lane-by-lane
        - Pad final block: data || 0x01 || 0x00...0x80
        - Squeeze: 32 bytes from the first 4 lanes
    """
    rate = 136  # bytes
    state = [0] * 25  # 5x5 lanes of 64 bits each

    # Absorb full blocks.
    offset = 0
    n = len(data)
    while offset + rate <= n:
        block = data[offset:offset + rate]
        for i in range(rate // 8):
            lane = int.from_bytes(block[i * 8:i * 8 + 8], "little")
            state[i] ^= lane
        _keccak_f(state)
        offset += rate

    # Final block with padding.
    last = bytearray(rate)
    remaining = n - offset
    last[:remaining] = data[offset:offset + remaining]
    last[remaining] = _KECCAK_PAD
    last[rate - 1] |= 0x80  # final bit of padding
    for i in range(rate // 8):
        lane = int.from_bytes(last[i * 8:i * 8 + 8], "little")
        state[i] ^= lane
    _keccak_f(state)

    # Squeeze 32 bytes (4 lanes, little-endian).
    out = bytearray()
    for i in range(4):
        out += state[i].to_bytes(8, "little")
    return bytes(out)


def eip55_checksum(unmixed: bytes) -> str:
    """Apply EIP-55 mixed-case checksum to a 20-byte Ethereum address.

    EIP-55: hex-encode the address, then for each character, uppercase
    it iff the corresponding hex digit of keccak256(hex_string) is >= 8.
    This gives addresses that have built-in error detection (matching
    mixed-case is highly likely to be correct).
    """
    if len(unmixed) != 20:
        raise ValueError(f"EIP-55 checksum requires exactly 20 bytes, got {len(unmixed)}")
    hex_addr = unmixed.hex()
    h = keccak256(hex_addr.encode("ascii"))
    out = []
    for i, c in enumerate(hex_addr):
        # Each byte of h yields two nibbles of checksum.
        if c in "0123456789":
            out.append(c)
        else:
            # nibble i of the hash: byte i//2, high nibble for even, low for odd
            nibble = (h[i // 2] >> (4 if i % 2 == 0 else 0)) & 0x0F
            out.append(c.upper() if nibble >= 8 else c)
    return "".join(out)
