# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 0.0.1-alpha | in development   |

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security-sensitive bugs.

Report privately via GitHub Security Advisories:
https://github.com/zhengdaqi/reliquary/security/advisories/new

Or by email to the maintainer (see the commit history). We will acknowledge
within 72 hours and aim to ship a fix or coordinated disclosure within 30 days.

## Key-Handling Warnings (Read Before Using)

Reliquary v0.0.1-alpha generates and uses private keys (`soul.key`,
`*.soul.key`). These keys are the sole proof of authorship for a Soul —
loss of a key means loss of the Soul. The current v0 implementation:

- Holds keys in memory while the process runs.
- Does **not** integrate with hardware wallets, secure elements, or
  threshold / MPC schemes. (See `DECISIONS.md` — D6, D13.)
- Does **not** provide key-rotation, recovery-from-share, or guardian
  social-recovery primitives. (See `NOT_DOING.md` — soft not-yets.)
- Persists nothing by itself. If the operator wants durability, they
  must export the key bytes and store them somewhere safe (encrypted
  disk, password manager, hardware wallet once supported). The bytes
  themselves are sensitive material — handle accordingly.

## What This Project Will Never Do

To be explicit, Reliquary will not:

- Custody your private key. Ever. (See `SOUL.md`, `NOT_DOING.md`.)
- Transmit plaintext memory to any server. (Encryption happens
  client-side.)
- Add KYC / identity-collection features. (`NOT_DOING.md`.)

If a future version appears to do any of these, treat it as a fork,
not Reliquary, and verify against `SOUL.md` and `NOT_DOING.md`.
