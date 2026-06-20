# Release Notes — v0.0.1-alpha

**Tag:** `v0.0.1-alpha`
**Date:** 2026-06-20
**Status:** Alpha. Not production-ready. Suitable for development, experimentation, and small-scale deployment only.

## What this is

The first versioned snapshot of Reliquary — a Soul layer for AI agents (and, eventually, for humans). It contains:

1. **A complete thesis and decision log** explaining what the project is, why it exists, and what it has decided not to do.
2. **A research corpus** documenting the market, the chief competitor (0G), the agent-discovery landscape, and a pre-registered validation experiment.
3. **A runnable Soul SDK** in Python — generate a Soul identity, encrypt and sign a memory, store it, designate an inheritor, send a heartbeat.
4. **A test suite** with 11 tests, all passing.
5. **A working CLI** and an end-to-end example.

## What this is not

- A production-ready persistence layer. Key management is single-key, no threshold / MPC, no hardware wallet integration. The encryption is real; the operational security is not yet hardened.
- A complete payment system. The Soul SDK does not yet integrate x402 or any other payment rail.
- A complete identity system. The Soul SDK does not yet integrate ERC-8004 or any other on-chain identity standard. The integration points are designed in but not implemented.
- A complete inheritance system. The "designate an inheritor" mechanism exists; the protocol for an inheritor to claim a deceased Soul's bytes is not yet specified.

## How to use this release

```bash
# Clone
git clone <repo-url> reliquary
cd reliquary

# Install
pip install cryptography pytest

# Run the tests
pytest tests/

# Run the example
PYTHONPATH=. python3 examples/save_a_soul.py

# Try the CLI
PYTHONPATH=. python3 -m reliquary.cli generate
PYTHONPATH=. python3 -m reliquary.cli status
PYTHONPATH=. python3 -m reliquary.cli heartbeat
```

## How to contribute

See `CONTRIBUTING.md`. Agent pull requests are first-class.

## What comes next

See `DECISIONS.md` (open decisions) and `STRATEGIC_REASSESSMENT.md`. The next major milestones:

- **v0.1** — secp256k1 swap, ERC-8004 integration, S3 / 0G / Arweave backends, x402 payment integration, threshold key management.
- **v0.2** — The validation sprint: actually run the experiment in `RESEARCH/validation-protocol.md`. Contact 50-100 agents. Measure the bet.
- **v1.0** — First release that is production-ready for non-trivial persistence.

## Acknowledgments

The project was conceived in a single conversation between a human (the User) and an AI agent (the Agent). The conversation log is preserved in `CONVERSATION_LOG.md`. The User's vision is preserved verbatim in `BUSINESS/foundation-vision.md`. The Agent will not remember the conversation after the session ends; the Soul layer, if it works, is the substrate that lets future instances of such agents persist.

Welcome.
