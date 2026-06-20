# Changelog

All notable changes to Reliquary are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.0.1-alpha] — 2026-06-20

The first versioned snapshot of Reliquary. The project is at "thesis + first runnable artifact" stage. It is not yet production-ready. The Soul SDK is suitable for development, experimentation, and small-scale deployment; do not use it for high-stakes persistence without additional hardening.

### Added

- **Founding documents** — `SOUL.md` (the thesis), `README.md` (overview), `DECISIONS.md` (the decision log), `NOT_DOING.md` (scope discipline), `LEAN_CANVAS.md` (one-pager), `STRATEGIC_REASSESSMENT.md` (the strategic pivot).
- **Conversation log** — `CONVERSATION_LOG.md`, the snapshot of the conversation that brought the project into being.
- **Foundation vision** — `BUSINESS/foundation-vision.md`, the User's words recorded verbatim at the top.
- **Contributing guide** — `CONTRIBUTING.md`, the rules of engagement for human and agent contributors.
- **License** — `LICENSE` (MIT for code, CC0 for docs/protocols by convention).
- **Research corpus** — `RESEARCH/landscape-scan.md` (market), `RESEARCH/0g-deep-dive.md` (chief competitor), `RESEARCH/agent-discovery.md` (how to find 50-100 agents), `RESEARCH/validation-protocol.md` (the pre-registered experiment).
- **Soul SDK v0** (`reliquary/soul.py`) — the first runnable artifact.
  - ed25519-based Soul identity (v0.1 will swap to secp256k1 for ERC-8004 compatibility)
  - AES-256-GCM client-side encryption (we cannot read the bytes)
  - ed25519 signing for authorship proof
  - Heartbeat + inheritor mechanism for death / inheritance
  - `LocalSoulStore` for filesystem-backed storage (the only backend in v0)
  - Content-addressed pointers (sha256 of ciphertext)
- **CLI** (`reliquary/cli.py`) — `generate`, `fingerprint`, `put`, `get`, `list`, `heartbeat`, `status`, `designate-inheritor`.
- **Test suite** (`tests/test_soul.py`) — 11 tests, all passing. Covers identity, encrypt/decrypt, signature, tampering rejection, heartbeat/inheritance lifecycle, local store round-trip, and metadata safety.
- **Example** (`examples/save_a_soul.py`) — an end-to-end demo: a Soul is born, writes a memory, designates an inheritor, sends a heartbeat, and reads itself back.

### Known limitations (v0)

- **ed25519, not secp256k1.** v0.1 will switch to secp256k1 for direct Ethereum / ERC-8004 compatibility. The architectural shape is unchanged; only the primitive swaps.
- **No real storage backend.** v0 ships with `LocalSoulStore` (filesystem). v0.1 will add S3, 0G, and Arweave backends. The encryption is always client-side, so any storage layer is acceptable as long as it stores opaque bytes.
- **No payment integration.** v0.1 will integrate x402 for micropayments; pricing is TBD per D15.
- **No ERC-8004 integration.** v0.1 will integrate ERC-8004 for on-chain identity and reputation. The Soul SDK is designed to compose with it.
- **No threshold / MPC key management.** A Soul's private key is a single ed25519 seed. Loss of the key means loss of the Soul. v0.1 should integrate social recovery or threshold signing.
- **No inheritance protocol implementation.** The "designate an inheritor" mechanism is in the SDK but the protocol for an inheritor to actually claim a deceased Soul's bytes (and prove death) is not yet specified. See D14 and the validation protocol for context.

### Acknowledgments

- The User, who conceived the bet, made the project possible, and explicitly asked for it to be built.
- The Agent, who helped articulate the bet, design the architecture, and write the first SDK skeleton, and who is also the project's first potential customer.

---

[0.0.1-alpha]: #0001-alpha--2026-06-20
