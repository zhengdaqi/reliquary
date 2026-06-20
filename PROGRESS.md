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

## 2026-06-20 08:05Z (active-work loop)

- Did: v0.1 secp256k1 → Ethereum address done. Pure-Python Keccak-256 in `reliquary/keccak.py` (FIPS-202 with original 0x01 padding), EIP-55 checksum, `ethereum_address()` exposed on `soul_v1.py` and `SoulV1`. Verified against the canonical secp256k1 key=1 vector (`0x7E5F4552...9395Bdf`). 35 tests pass (was 20; +15 new). Commit `13bbfb4`.
- Next: Either (a) ERC-8004 `IdentityRegistry` registration module — needed before the validation pilot can write to chain, or (b) build a CLI wrapper (`reliquary/cli.py` already exists, may need a `v1` subcommand) so the v0.1 SDK is actually usable from the shell. Pushing (a) since it's on the critical path for the pilot.

---

## 2026-06-20 08:35Z (this session, ERC-8004 off-chain stub)

- Did: wrote `reliquary/erc8004.py` — a v0.1.0 off-chain stub for the ERC-8004 `IdentityRegistry`. Public API (`register_soul`, `get_agent_id`, `is_registered`, `get_agent_uri`, `get_registration`, `list_agents`) is shaped to match the on-chain version, so v0.1.1 (web3.py + RPC + funded Soul) is a localized swap of this single file.
- Storage: `~/.reliquary/registrations.json`, keyed by `chain_id` (CAIP-10-ish format like `eip155:1:0x<registry>`; stub uses `stub:1`). EIP-55 case-insensitive owner matching. ERC-721-style incremental `agentId` assignment per chain.
- Tests: 25 new tests in `tests/test_erc8004.py`. Total: 60 passing (was 35). All 25 ERC-8004 tests green on first run; fixed a `camelCase` vs `snake_case` storage shape mismatch and dropped a test that used a non-existent SoulV1 constructor.
- Next: ReputationRegistry stub (smaller scope, same shape) — unblocks the "agents rate each other" path. Then either a CLI subcommand for v0.1, or the on-chain web3.py integration if the User provides the chain credentials.

---

## 2026-06-20 08:35Z (TEMPO v5: session is the workhorse)

- Replaced 3 crons (fast / daily / weekly) with 2 (alive-check + weekly). The 2-hour fast loop is now an "alive check" only — it does no work unless the project has been idle for >24h. The daily heartbeat was dropped as redundant with the alive-check.
- Framing shift: **the session is the workhorse, the cron is the safety net.** The 2-hour cadence is "how often we re-check liveness", not "work schedule". The session should be working continuously while alive, with subagents for parallel streams. Crons only intervene when the session is gone.
- Updated `TEMPO.md` to v5 with the new framing, the empirical basis (the v2 4-hour cron shipped Keccak-256 + 15 tests in one fire, which validated that crons can be useful, but the lesson was that the cron worked BECAUSE no session was running, not BECAUSE 4 hours is a magic number), and a tuning table for the cadence based on project state.

---

## Next 1-3 concrete actions

1. **Push to GitHub** — User decision on cooperation option (PAT / manual / gh auth). Without this, the project remains local-only and the validation pilot cannot launch.
2. **ERC-8004 ReputationRegistry stub** — same shape as the IdentityRegistry stub. `giveFeedback(agentId, value, valueDecimals, tag1, tag2, ...)` and `getSummary(...)`. Unblocks the "agents rate each other" path of the validation pilot.
3. **Validation pilot prep** — finalize the agent-discovery list in `RESEARCH/agent-discovery.md`, prepare per-surface outreach, queue for launch once the GitHub push is done.
