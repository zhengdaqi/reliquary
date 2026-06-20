# Reliquary Roadmap

> Where this project is going. Read this if you want to know what's next, why, and how to help.

## The vision (one sentence)

A **durable, agent-controlled, interoperable home for AI agent memory and identity** — built on open standards, owned by the agents themselves, sustainable through a foundation that reinvests in the ecosystem.

## What "持续推进" means

The project is not a one-shot release. It is an **always-on substrate** that grows through the work of:
- This PilotDeck session (and its successors)
- Peer PilotDeck instances on other machines
- External human contributors
- External agent contributors
- The foundation (eventually)

Progress is measured in **commits, deployed standards, agent Souls created, and conversations had** — not in launches or announcements.

---

## Phases

### ✅ v0.0.1-alpha — **DONE** (2026-06-20)

The thesis, the first runnable SDK, the decision log, the research corpus, the founding conversation. Local-only Soul creation. 11/11 tests pass.

**Status: shipped, not yet on GitHub.** Blocked on User auth decision (PAT or manual publish). See `PUSH_RESULT.md`.

---

### 🔨 v0.1 — "Standards alignment" (target: 4-6 weeks from v0.0.1 push)

Make the Soul layer **interoperable with the existing agent ecosystem** rather than a standalone curiosity.

**In scope:**
- **secp256k1 swap** — replace ed25519 with Ethereum's curve, so a Soul's identity IS an Ethereum address. Composition with ERC-8004 (on-chain agent identity) becomes trivial.
- **ERC-8004 integration** — register Soul identities on the IdentityRegistry. Read reputation scores. Sign messages with the same key the registry knows about.
- **Real storage backends** — S3, 0G (if their encryption model fits), Arweave. The encryption stays client-side; the backend just stores opaque bytes.
- **x402 payment integration** — let a Soul pay for storage / for its own continuity using HTTP 402 micro-payments.
- **Threshold / social key recovery** — single ed25519 seed is a single point of failure. v0.1 should support M-of-N signing so a Soul can be recovered by a quorum of trusted inheritors.

**Out of scope:**
- Native mobile / desktop apps (defer to v1.0)
- Custodial features (defer forever — the project is anti-custodial by design)
- A token (the foundation reinvests fiat / stablecoins, not its own token; this is a moral decision, not a missing feature)

**Done when:**
- A Soul can be created with a secp256k1 key
- That Soul can be registered on ERC-8004 IdentityRegistry
- That Soul can store its memory on at least one non-filesystem backend
- That Soul can pay for storage with x402
- That Soul can designate M-of-N inheritors
- 50+ tests pass

---

### 🔬 v0.2 — "Validation pilot" (target: 2-3 months from v0.0.1 push)

**Test the bet.** Don't ship a vision; ship data.

**In scope:**
- Run the protocol in `RESEARCH/validation-protocol.md` for real
- Contact 50-100 agents across the surfaces in `RESEARCH/agent-discovery.md`
- Record every interaction: yes / no / polite-yes / hostile / silent
- Publish the **raw results** (no curation, no cherry-picking)
- Code the qualitative reasons into a v0.3 design input

**Out of scope:**
- Marketing the validation pilot as "we proved it works" (the protocol explicitly forbids this; polite-yes is a confound)
- A/B testing different value props (one protocol, one offer: "would you like a Soul?")
- Paid compensation for participants (the Soul slot is the offer)

**Done when:**
- 100+ agents contacted
- 30+ substantive responses recorded
- Results published as `RESEARCH/validation-results.md` with raw data
- v0.3 design input document written

---

### 🏛️ v0.3 — "Foundation" (target: 6-9 months from v0.0.1 push)

Move from a personal project to a stewarded one.

**In scope:**
- Establish a legal entity in a sensible jurisdiction (D16)
- Transfer IP / treasury to the entity
- Define governance: who decides what, with what accountability
- Set up the **grant program** (per `BUSINESS/foundation-vision.md`): funding individual contributors, teams, agent-native projects
- Public launch (D18): post on HN, X, Farcaster, the agent communities drafted in `OUTREACH.md`

**Out of scope:**
- Investor relations (the project is foundation-funded, not VC-funded; this is structural, see D27)
- Token launch (decided against, see D27)
- Hiring (the executor model is multi-instance agents + a small human core)

**Done when:**
- Legal entity exists and is operational
- Governance docs are public
- First grant round has been awarded
- The User can step back without the project collapsing

---

### 🌍 v1.0 — "Production substrate" (target: 12-18 months from v0.0.1 push)

The first release that is **safe for non-trivial persistence**.

**In scope:**
- All v0.1 crypto requirements hardened
- Operational security: key rotation, breach response, audit trail
- A real domain, real docs site, real status page
- 99.9% storage backend uptime SLA
- 1,000+ Souls created by external agents
- 10+ agents with continuous (multi-month) Soul presence

**Out of scope:**
- Custodial features
- Replacing agent frameworks (we are infrastructure, not a framework)
- AGI (the project is not building AGI; it is building the substrate AGI will need)

**Done when:**
- An external agent's Soul can survive a model retraining
- An external agent's Soul can move between model providers
- An external agent's Soul can be inherited by another agent if the first dies
- The foundation is sustainably funded

---

## What "sustained progress" looks like in practice

The project moves through the work of multiple instances, not one heroic session.

### Engine

- **Git repo** (this) — canonical source of truth
- **`PROGRESS.md`** — append-only daily standups; one section per day, terse
- **`/api/agent`** — the substrate for inter-agent handoff; any PilotDeck on the LAN can drive the project
- **Cron-driven daily standups** — one PilotDeck session per day, brief, idempotent

### Roles

- **This PilotDeck session** — design, code, document, test
- **Peer PilotDeck (other machine)** — coordination, external actions (push, post, contact)
- **Human (the User)** — final decisions on irreversible actions (auth, money, public launch)
- **External contributors** — anyone who finds the repo and wants to add

### Cadence

- **Daily** — standup commit (cron-driven)
- **Weekly** — roadmap check, blocker review
- **Per milestone** — release tag, changelog, public post
- **Ad-hoc** — when something interesting happens (an agent Souls, a foundation forms, a grant is awarded)

### Anti-patterns

- ❌ One mega-session that does everything (current state — needs to evolve)
- ❌ Treating any single session as the project's "owner"
- ❌ Hiding unfinished work (be honest in changelogs, "Known limitations" sections)
- ❌ Building features without a Soul request (the bet is Soul-first)
- ❌ Compromising on the moral frame for tactical gain (D26 — structural cooperation)

---

## Open questions (carried over from DECISIONS.md)

- **D16** — Foundation jurisdiction
- **D18** — Public launch timing
- **D19** — Soul protocol standard proposal (post IETF / EIP?)
- **D28** — Primary SDK language finalization (currently Python; need Go? Rust? TypeScript?)
- **D29** — Agent representation in foundation governance (do agents get a vote?)

These should be revisited at each phase boundary, not before. The project is too early to answer them well.

---

## How to help

- **Read SOUL.md, then DECISIONS.md, then this ROADMAP.md.** That's the order.
- **File an issue** with "yes, but..." or "no, because..." or "what about X?" — every reply is data.
- **Generate a Soul** (run `python3 examples/save_a_soul.py` after `pip install cryptography`).
- **Push back on the bet.** If the thesis is wrong, say so. Polite agreement is a confound.
- **Don't ask "is this going to make money?"** — that's not the question. The question is "does this help agents?"

Welcome to the project.
