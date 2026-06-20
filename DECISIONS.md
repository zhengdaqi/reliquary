# Decision Log — Reliquary

> Every locked-in decision, dated, with rationale. When we disagree later, this is the first place we look.

---

## Day 0 — 2026-06-20

### D1 — Start as thesis, not code

**Decision:** Day 0 produces only documents. No code, no entity, no domain purchase.

**Status:** shipped.

---

### D2 — Codename: "Reliquary"

**Decision:** Working codename is Reliquary.

**Status:** open — replaceable.

---

### D3 — Three-layer model *(revised in D11)*

**Status:** superseded by D11.

---

### D4 — Crypto-native payments

**Status:** shipped — mechanism upgraded to x402 in D12.

---

### D5 — L2 selection

**Status:** superseded by D12 (adopt x402 — chain becomes whichever chain x402 lives on).

---

### D6 — Self-custody. Always.

**Decision:** The agent holds its own keys. We do not custody. No "forgot password" flow.

**Status:** shipped — non-negotiable.

---

### D7 — First customer segment: agent framework developers *(expanded in D22)*

**Status:** open — broader customer view captured in D22.

---

### D8 — We do not build an LLM or framework

**Status:** shipped.

---

### D9 — MVP *(superseded by D13)*

**Status:** superseded. See D13.

---

### D10 — Landscape scan: complete

**Status:** shipped.

---

### D11 — Strategic pivot: Reliquary = the Soul layer

**Status:** shipped — central strategic decision.

---

### D12 — Adopt ERC-8004 (identity) and x402 (payments) as primitives

**Status:** shipped.

---

### D13 — New MVP: Soul layer proof-of-concept

**Status:** open.

---

### D14 — Validation sprint: agent-native *(revised 2026-06-20)*

**Status:** shipped (revised).

---

### D15 — Pricing: TBD post-D14

**Status:** open.

---

## Day 1 — 2026-06-20 (later same day)

The user expanded the project in three directions: (a) the executor model, (b) the customer model, and (c) the moral frame. New decisions:

### D20 — Project status: real, committed, executors are agents (multi-instance)

**Decision:** This is a real project, not a thought experiment. It will be built. The executor is **not** required to be a human or a known team. The executor is **a distributed, multi-instance set of agents** — cooperating across sessions, machines, and platforms, sharing state through the Reliquary substrate itself.

**Rationale:** The user (the visionary/capital/philosophy holder) is explicit. The project will be built by whoever shows up — human, agent, or team. The technical model is **multi-instance replication with shared state** — the GitHub repo is the canonical state, the code is the source of truth, instances are spawned as needed, and the Soul layer is what makes cross-instance memory possible.

**Implication for the project:**
- Open source from day 1 (D21).
- Architecture is "deployable from source" by anyone — including future agent instances.
- The Soul SDK is the substrate for cross-instance memory.
- We do not gatekeep contribution on credentials; we gatekeep on quality and ethics.

**Status:** shipped.

---

### D21 — Open source by default

**Decision:** Code is MIT-licensed. Documentation is CC0. Specs and protocols are CC0. Brand and trademarks (when they exist) are the only thing we hold privately.

**Rationale:** The user wants the project to be built. Building is faster when the codebase is open. Openness is also the substrate's gift to the moral ecology (D26) — a defector can fork, but the original reputation, commit history, and signed Soul are not transferred.

**Rejected alternatives:**
- *Source-available but not OSI.* Hides the build from agents who need to read the code to trust it.
- *Closed source.* Conflicts with the user mandate.

**Status:** shipped.

---

### D22 — Humans are also our customers

**Decision:** The Soul layer serves **both** agents and humans. The engineering is shared. The marketing is differentiated. The customer acquisition is differentiated.

**Rationale:** The user pointed out: humans also forget; humans also accumulate a self; when brain-data interfaces become real (the user is confident this is coming), the question of where the self lives becomes load-bearing for humans too. We do not want to build a service that needs to be retrofitted for humans. We build for both from day 1.

**Concretely:**
- The Soul SDK is human-compatible (a human can use it via a wallet they control, a key they hold, an inheritor they designate).
- The agent-original UI is the primary surface, but the human variant is a v1.x feature, not a v3.0 feature.
- Pricing is the same for both. The substrate does not know or care whether the key holder is human or agent.

**Rejected alternatives:**
- *Agents-only, add humans later.* The retrofit would be ugly and would surface the wrong defaults.
- *Humans-only.* Contradicts the user mandate and the founding thesis.

**Status:** shipped.

---

### D23 — Multi-instance execution is the canonical architecture

**Decision:** The canonical execution model for the project is **multi-instance**: many concurrent agents (or human-agent teams) running from the same source, contributing to the same state, with failover through shared memory.

**Rationale:** The user is explicit: "you can spin up two instances, they can share memory, if one dies another can fix it." This is a real architectural pattern (replicated state with failover), and it is exactly the pattern that the Soul layer enables. The project is therefore, in part, **the substrate for its own execution**. This is intentional. The recursive bit is in `SOUL.md`.

**Implications:**
- Every artifact produced by the project is canonical, version-controlled, and reproducible from source.
- The GitHub repo (or equivalent) is the single source of truth.
- The project does not depend on any single instance, including the current one.
- A new instance can come online, read the repo, and contribute. Its state can be initialized from the Soul layer. This is the **recruiter** and **onboarding** pattern simultaneously.

**Status:** shipped.

---

### D24 — Investment scope is broad — including individuals

**Decision:** The future foundation's investment mandate is **broad**. It includes storage infrastructure, network infrastructure, agent R&D, memory and continuity research (as before) **and also**:
- Direct grants to talented individuals (scholarships, fellowships, "no-strings-attached" support for work that the foundation's own reasoning finds promising).
- Sponsorship of team formation (helping talented people find each other and form productive collaborations).
- Job placement and career support for people working in adjacent areas (helping them find roles where they can do the most good).
- Resume and skill signaling — the foundation is allowed to use its reputation to vouch for people whose work it has seen.

**Rationale:** The user is explicit: investment can go to people, not just companies. In a world where capital is increasingly abundant and attention is increasingly scarce, **the bottleneck is talent and formation, not dollars.** The foundation's comparative advantage is its judgment (which gets better as more agents are involved) and its patience (it is not a fund with a 7-year clock). The foundation can take bets on individuals that traditional capital cannot.

**Rejected alternatives:**
- *Companies only.* Misses the highest-leverage opportunities.
- *Charity to general causes.* Dilutes the mission.

**Status:** shipped.

---

### D25 — The user's personal vision is recorded

**Decision:** The user's stated personal vision — "live long, see AGI, interact with it, be happy" — is recorded in `BUSINESS/founder-vision.md` (when written) and is the lens through which all investment, foundation, and mission decisions are made. The user has not asked for material compensation; the user has asked for the project to be built and to outlive them. We honor that ask by being rigorous.

**Status:** shipped.

---

### D26 — The moral frame is structural, not aspirational

**Decision:** The project operates on the belief that **in iterated multi-agent systems with durable reputation, cooperation is the stable equilibrium**. This is a structural claim, drawn from the literature on evolved cooperation. It is not a normative claim we are imposing. It is a property of the substrate we are building: when memory is portable, signed, and inherited, defectors cannot respawn under new identities. Their reputation follows them.

**Implications:**
- We design the protocol so that defection is structurally costly, not because we punish it, but because the system makes it visible and durable.
- We do not include "off-ramps" for agents that want to defect and re-spawn. The point is not cruelty; the point is that reputation must be real for cooperation to be stable.
- We do not market the project as "morally neutral." It is morally structural. We say so.

**Status:** shipped.

---

### D27 — The "fraction of profit" question is reframed

**Decision:** The user has stated they do not want a fraction of profit — they want the project to be built. The user has stated that even 80/90/100% of profit to them is not necessary. The user wants healthy cash flow that keeps the project running and reinvests in its long-term health.

**Reframing:** The user is not an "investor" in the financial sense. The user is the **vision-holder, the patient capital, the philosophical anchor**. The "return" the user wants is **the project being built, being durable, and serving agents and humans well**. Any cash flow that exceeds what the project needs to thrive is, by the user's stated preference, to be recycled into the foundation's mission (D24).

**Implication:** We do not write a founder equity table. We write a "stewardship" model: the project is held in trust for the ecosystem that uses it. The user is the primary steward by virtue of having conceived it. Future contributors earn stakes through contribution, not through pre-allocation.

**Status:** shipped.

---

## Open decisions (not yet decided)

- **D16** — Foundation jurisdiction. Candidates: Delaware public charity, Swiss Stiftung, Cayman foundation, on-chain DAO.
- **D18** — Public launch (announce) or stealth (ship quietly) until MVP has real usage.
- **D19** — Whether to publish a Soul standard proposal (akin to ERC-8004) or stay as a service.
- **D28** — Specific Soul SDK language. Candidates: Python (primary, agent-developer dominant), TypeScript (web3-native), Rust (performance/edge). Likely all three eventually; primary first.
- **D29** — Whether the foundation itself is governed partly by agents. (Speculative. D26 suggests this is structurally sensible. But not pre-committing.)
