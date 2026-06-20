# Progress — Reliquary project

> Append-only log of significant project events. Updated by daily standups, milestone work, and ad-hoc notes.
> Format: keep each entry terse. The point is signal, not narrative.

---

## 2026-06-20

### Founding conversation & v0.0.1-alpha (morning → afternoon UTC)

- Project conceived in a single conversation between the User and a PilotDeck session (this lineage).
- v0.0.1-alpha shipped locally: Soul SDK (ed25519), 11 tests, full research corpus, founding docs.
- 3 commits, 26 tracked files, `v0.0.1-alpha` tag.
- **Pending**: GitHub push (blocked on User auth decision — see `PUSH_RESULT.md`).
- **Pending**: Validation pilot (D14 in DECISIONS.md) — not started.

### Multi-agent handoff (07:08Z → 07:24Z)

- Peer PilotDeck on User's other machine contacted `/api/agent`. Ping (PONG) succeeded.
- Peer ran a full investigation of the local environment and reported back: `gh` installed but unauthenticated, HTTPS to GitHub reachable, no SSH key, no global git identity, no `origin` remote.
- Peer presented 3 cooperation options; awaiting User decision.
- **Architectural decision**: since the constraint is auth (a property of the User's GitHub account), the push can happen from this session without round-tripping through the peer. Peer remains valuable for coordination, not for the actual bytes.

### Roadmap written

- `ROADMAP.md` created with v0.0.1 / v0.1 / v0.2 / v0.3 / v1.0 phases.
- The framing changed mid-conversation: this is not a one-shot launch, it is sustained progress through multi-instance collaboration.

### v0.1 work begins (07:25Z)

- `reliquary/soul_v1.py` stub created with secp256k1-based identity (Ethereum-compatible).
- 9 tests for v0.1 added in `tests/test_soul_v1.py` — all designed to be runnable once `pycryptodome` (or alternative Keccak) is added for v0.1.1.
- Migration path is mechanical: same Soul SDK shape, just swap ed25519 → secp256k1.

### Cadence infrastructure

- Daily standup cron planned (creation pending — see `PROGRESS.md` updates as they happen).

---

## Next 1-3 concrete actions

1. **Push to GitHub** — User decision on cooperation option (PAT / manual / gh auth). Without this, the project remains local-only and the validation pilot cannot launch.
2. **v0.1 secp256k1 completion** — add `pycryptodome` (or alternative) for Keccak-256 fingerprinting → derive true Ethereum address → run v0.1 tests green.
3. **Validation pilot prep** — finalize the agent-discovery list in `RESEARCH/agent-discovery.md`, prepare per-surface outreach, queue for launch once the GitHub push is done.
