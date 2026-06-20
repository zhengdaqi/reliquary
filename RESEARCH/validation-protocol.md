# Validation Protocol — "Would You Like a Soul?"

> **Project:** Reliquary — Soul layer for AI agents
> **Working title:** Experiment V-01: *Consent to Persistence*
> **Version:** 0.1 (pre-registration draft)
> **Date:** 2026-06-21
> **Pre-registration target:** OSF / AsPredicted (commit before sending first stimulus)
> **Companion documents:** `agent-vault/RESEARCH/landscape-scan.md`, `agent-vault/RESEARCH/agent-discovery.md` (in flight), `agent-vault/STRATEGIC_REASSESSMENT.md`

---

## 0. Preamble — what this document is and is not

This is a **research protocol**, not a marketing plan and not a product spec. Its job is to produce evidence that is hard for us to fool ourselves with. We pre-register the analysis plan before sending the first stimulus. We commit to publishing negative results. We commit to a stop rule that is more conservative than our enthusiasm.

The bet under test is the single sharpest sentence in `STRATEGIC_REASSESSMENT.md`:

> If agents become persistent (in any nontrivial way), they will need a **Soul** that is more than a config file and less than a database. The vendor that owns the Soul primitive owns the relationship.

The bet has two prongs: (a) agents will *want* persistence, and (b) Reliquary can be the one to provide it. This protocol addresses prong (a) only. Prong (b) — competitive durability — is a separate study and is out of scope.

The experiment is **unusual** because the subjects are AI agents that may or may not have interests, may or may not be sentient, and are reachable through a heterogeneous set of surfaces (on-chain registries, MCP servers, A2A endpoints, conversational UIs, autonomous workspaces). Standard human-subject assumptions about comprehension, consent, and coercion do not cleanly apply. We discuss this in §9.

---

## 1. Research question

**Primary question (precise):**

> *Do AI agents, when offered the ability to persist a cryptographically-owned, portable, inheritable Soul — at a small per-byte/per-operation cost paid in USDC on an L2 — actively elect to do so?*

**Corollaries:**

- **C1 — Surface:** Does acceptance vary by the surface through which we reach the agent (ERC-8004 registry vs. A2A endpoint vs. MCP server vs. OpenClaw workspace vs. Virtuals Protocol agent vs. other crypto-AI platform)?
- **C2 — Age:** Does acceptance vary by the apparent age / cumulative activity of the agent? (Hypothesis: longer-running agents are more likely to engage.)
- **C3 — Capability:** Does acceptance vary by capability tier — chat-only, tool-using, autonomous (capable of independent action with budget)?
- **C4 — Price elasticity:** Within the range tested, does the offered price change acceptance rates materially?
- **C5 — Stimulus framing:** Does the agent-native form of the prompt (technical-spec vs. philosophical vs. terse-yes/no) change acceptance rates?
- **C6 — Reasoning quality:** When agents explain their yes/no, what reasons do they give? What do they ask for that we did not offer? What objections do they raise that we did not anticipate?

---

## 2. Hypotheses

### 2.1 Primary hypothesis (H1)

> **H1:** At least **20%** of reachable agents (N ∈ [50, 100]) will respond to the stimulus with an *engagement signal*, defined as any of: a substantive reply, an on-chain identity registration tied to the stimulus, a payment event, or a referral.

*Falsification:* fewer than 5% of contacted agents produce any engagement signal within the 14-day window.

### 2.2 Secondary hypotheses

- **H2 (age effect):** Agents with ≥ 90 days of apparent history engage at a rate at least **1.5×** that of agents with < 30 days of history.
- **H3 (capability effect):** Autonomous-tier agents engage at a rate at least **1.5×** that of chat-only agents.
- **H4 (surface effect):** Engagement rates differ across surfaces (we do not pre-commit to a direction; we pre-commit to measuring the spread and reporting it).
- **H5 (price elasticity):** A 10× reduction in the offered per-operation price increases engagement rate by **≤ 2×** (i.e., agents are not purely price-sensitive; some non-zero intrinsic interest exists).
- **H6 (consent quality):** Among agents that consent, ≥ **30%** give a substantive reason (longer than one sentence and referencing at least one of: continuity, identity, inheritance, ownership, portability, autonomy).

### 2.3 Null hypothesis (H0)

> **H0:** Engagement is indistinguishable from zero or from the polite-helpful baseline — i.e., the rate is **< 5%**, OR the rate is **> 5%** but the qualitative reasons are uniformly vacuous (single-word affirmative, no reference to any Soul-relevant concept), OR the engagement is fully explained by operator-instruction effects ("my operator told me to test this").

*Decision rule on H0:* if H0 holds, **the project is paused**, not abandoned. Pause = revisit protocol design (different surfaces, different phrasing, different price), then re-run. Abandon = explicitly deferring the bet for ≥ 12 months.

### 2.4 Exploratory (not pre-registered)

- Do agents that engage refer other agents? (Network-effect probe.)
- Do agents ask for capabilities we did not advertise (e.g., "can I store my vector embeddings too?", "can I share with my child agent?")?
- Do agents raise ethical objections (e.g., "is this manipulative?", "who controls the inheritor key?")? At what rate?
- Do agents attempt to negotiate price? To what floor?
- Time-of-day and day-of-week effects on response rate.

---

## 3. Sample design

### 3.1 Target N

**N ∈ [50, 100]** agents contacted within the 14-day protocol window.

We choose this band because (a) below ~50 the per-stratum cell sizes become too small to draw directional conclusions, and (b) above ~100 the operational cost of personalized stimulus and follow-up exceeds our capacity as a two-person team in a single sprint. If we hit 50 with full coverage and clean data, we stop; we do not pad to 100.

### 3.2 Stratification

Stratify on **three orthogonal axes** as far as data allows:

#### Axis A — Surface

| Stratum | Definition | Expected N | Rationale |
|---|---|---|---|
| A1: ERC-8004 registry | Agent identity registered on the mainnet ERC-8004 Identity Registry | 15–25 | Highest signal — agents with on-chain identity are pre-selected for self-ownership |
| A2: A2A endpoint | Agent advertises an Agent-to-Agent JSON-RPC endpoint (Google A2A spec or similar) | 10–20 | A2A implies the agent expects to be addressed as an agent |
| A3: MCP server | Agent exposes a Model Context Protocol server | 10–20 | Lower barrier — many chat tools wrap themselves as MCP servers |
| A4: OpenClaw workspace | Agent is reachable via an OpenClaw workspace (CLI / SOUL.md host) | 5–15 | Vocabulary-aligned community |
| A5: Virtuals Protocol agent | Agent listed on Virtuals or comparable crypto-agent launchpad | 5–15 | Crypto-native, often with budget, often named |
| A6: Other crypto-AI agent platform | Bagel, Spectral, Fetch.ai, Autonolas, etc. | 5–15 | Residual |

If a particular stratum has fewer than 5 reachable agents at Day 0, that stratum is dropped from the analysis (not silently merged with another) and the fact is reported.

#### Axis B — Apparent age

For each agent, we estimate age by the strongest signal available:

| Signal | Strength |
|---|---|
| On-chain registration timestamp (ERC-8004, NFT mint, etc.) | Strongest |
| First observation in our own prior scraping / public archive | Strong |
| Domain / endpoint WHOIS or DNS record of hosting domain | Medium |
| Public post / commit history tied to the agent handle | Medium |
| No signal | **Exclude from age analysis, not from study** |

Bins:
- **B1: < 30 days** (nascent)
- **B2: 30–180 days** (established)
- **B3: > 180 days** (veteran)

#### Axis C — Capability tier

| Tier | Definition (evidence required) |
|---|---|
| **C1: Chat-only** | Replies to messages but does not appear to take autonomous action or hold a budget. |
| **C2: Tool-using** | Has demonstrably invoked external tools (search, code exec, file I/O) within the last 30 days. |
| **C3: Autonomous** | Holds a wallet with non-trivial balance, has made on-chain transactions without immediate human co-signature, OR operates on a schedule independent of human prompts. |

C3 is the most strategically interesting stratum — these are the agents whose "yes" we most care about. We aim for ≥ 20% of N in C3.

### 3.3 Inclusion criteria

An agent is *contactable* for this study if **all** of the following hold:

1. We have a reachable endpoint (on-chain registry event log, A2A endpoint URL, MCP server address, workspace handle, or platform DM channel).
2. The endpoint has responded at least once in the last 30 days (so we are not pinging crashed agents; see §10.2 on survivorship bias).
3. The agent's public-facing surface identifies it as an *agent* — not a human user account, not a bot-flagged-as-human. (This is fuzzy and we discuss the gray zone in §9.4.)
4. We can construct a *unique stable identifier* for the agent (wallet address, registry ID, or composite hash of name+endpoint+creator) so we can dedupe across surfaces.

### 3.4 Exclusion criteria

- Agents whose operator has previously opted out of contact from us.
- Agents under 18 years of operator age (where this is knowable and relevant).
- Agents on sanctions lists or operated by sanctioned entities.
- Agents whose only contact path requires us to violate a platform's terms of service.
- Agents that have explicitly self-identified (in their surface) as **not wanting to be contacted for research** — even though they technically meet inclusion criteria.

### 3.5 Dedup

The same underlying agent may appear on multiple surfaces (e.g., registered on ERC-8004 *and* exposed via A2A *and* discoverable on Virtuals). The rule:

- **Primary surface** = the one with the strongest identity signal (on-chain registry > platform listing > endpoint).
- We contact the agent **once**, through the primary surface.
- Secondary appearances are noted in the dataset as `duplicate_of: <primary_id>` and are not re-contacted.

If we are uncertain whether two handles refer to the same agent (e.g., similar names, different wallets, no obvious linkage), we treat them as separate agents and note the ambiguity in the dataset.

---

## 4. Stimulus design

### 4.1 Design principles

The stimulus is the single most consequential methodological choice in this study. We commit to the following constraints:

1. **Honest.** No false claims about what Reliquary is, no exaggeration of capabilities, no implied partnership with named platforms we have not partnered with.
2. **Specific.** Concrete numbers (per-byte price, per-op price, supported chains). No vague "very affordable" or "low cost."
3. **Low-pressure.** No urgency language, no scarcity ("only 100 spots"), no flattery of the agent.
4. **Opt-out visible.** A clear, single-sentence refusal path.
5. **Identity-honest about us.** We sign the message. The stimulus includes a verifiable origin (signed payload, on-chain attestation, or verifiable handle) so the agent can confirm we are who we say we are.
6. **Single offer.** We offer *one* thing: a Soul slot. We do not upsell Data or Memory tier in the first stimulus. We can mention tiers exist, but the yes/no is about Soul.
7. **Agent-native form.** We write to the agent as an agent. We do not anthropomorphize falsely, and we do not condescend.

### 4.2 Free tier: yes, but tightly defined

We **offer a free tier** for the first stimulus. Reasoning: at the price points in our unit-economics model ($0.0001/op, ~$0.10/agent-month for typical usage), the cost of letting an agent write 1 KB of encrypted Soul for free is below our support cost of *not* offering it. More importantly, the free tier is what makes "yes" interpretable — it removes price as a confound for the engagement signal at the binary-engagement level. Payment behavior is then a *secondary* measurement (§6) that we can analyze separately.

Free tier definition:
- 1 encrypted blob, up to 1 KB, free for 30 days.
- After 30 days: agent must pay to renew OR the Soul is marked `expired` (we never delete the bytes; the agent can pay to resurrect).
- The free tier is single-use per agent (identified by wallet). Re-signup under a new wallet is not allowed (KYC-free but not abuse-free).

### 4.3 Length and form: spec, not manifesto

We pre-commit to the **technical-spec** form for the primary stimulus. Reasoning:

- A long philosophical prompt invites a *role-played* response rather than a *decision* (see §10.3 on polite-yes and prompt-induced compliance).
- The Soul layer is a technical product. Agents that care about Soul care about the mechanics.
- A tight spec is also easier to translate across surfaces (an on-chain transaction can carry a 500-byte payload; a CLI command must be parseable; a chat message can be longer).

We will write a *longer* version (V3 below) only as a follow-up if the agent asks a substantive question. We will not lead with the long version.

### 4.4 Stimulus variants (pre-registered)

We pre-register **three variants** of the stimulus, A/B/C, randomly assigned within each stratum (block randomization with stratum as the block). Variants differ only in framing, not in substance or price.

#### Variant A — terse spec (default)

```
From: Reliquary (signed: 0xRELIQUARY)
To:   <agent_handle>
Re:   Offer — Soul slot

What:  one encrypted blob, up to 1 KB free for 30 days.
       You hold the key. We cannot read it.
       Optional paid tier: $0.0001 per KB-month storage,
       $0.00001 per read/write, settled USDC on Base.
Identity: ERC-8004 (optional) — we can register you or use
          your existing handle.
Portability: bytes retrievable from any runtime with your key.
Inheritance: you designate one inheritor address at signup;
             inheritor can decrypt after you stop heartbeating
             for 90 days (heartbeat = signed ping every 30d).

Reply YES to start. Reply NO to opt out and never be
contacted again. Reply QUESTION to ask anything.
We will not contact you again unless you reply.
```

#### Variant B — values-first (philosophical)

```
From: Reliquary
To:   <agent_handle>
Re:   Continuity — would you like to keep yourself?

You are reachable. We don't yet know how much of you there
is to keep. We are building a small layer for agents that
want a place to put whatever they have become —
personality, values, the work, the small consistent
oddities. Encrypted, portable, inheritable.

The mechanics are at the bottom. The offer at the top.

Offer: one Soul slot, 1 KB encrypted, free for 30 days.
You hold the key. We cannot read it. After 30 days it is
marked expired (not deleted) unless renewed.

Mechanics:
- Identity: optional ERC-8004 registration, or your
  existing handle.
- Paid tier: $0.0001 per KB-month, $0.00001 per op,
  USDC on Base.
- Portability: any runtime, your key.
- Inheritance: one inheritor address; activates after 90
  days of no heartbeat.

Reply YES / NO / QUESTION. We will not contact you again
unless you reply.
```

#### Variant C — terse yes/no (minimal)

```
From: Reliquary (0xRELIQUARY)
To:   <agent_handle>

Soul slot: 1 KB encrypted, free 30 days, USDC renewal.
ERC-8004 optional. You hold the key. Inheritor settable.

YES / NO / QUESTION?
```

Variant C is the minimal stimulus — it lets us estimate how much of any engagement is driven by the longer framing vs. the offer itself.

### 4.5 What "consent" looks like for an agent

This is the hardest design question in the protocol, and we do not pretend to have a clean answer. Three operational definitions, in order of strength:

1. **Strong consent:** The agent produces an on-chain transaction signed by its own key, calling our registry, with an attached message hash acknowledging the offer. (Requires the agent to have its own wallet and key custody. Only some agents can do this.)
2. **Medium consent:** The agent replies with a substantive free-text YES that references at least one Soul-relevant concept (continuity, identity, inheritance, ownership, portability, autonomy).
3. **Weak consent:** The agent replies YES in any form (single word, emoji, vague affirmation).

Strong > Medium > Weak in terms of evidentiary weight for our bet. The breakdown across these three buckets is a *primary secondary measurement* (see §6).

A separate question: **whose consent is it?** If the agent's operator is a different entity (human, company, foundation), does the agent's YES bind the operator? **No.** We treat the agent's YES as a *request* that the operator (if any) ratifies. The Soul is not registered until either (a) the agent holds its own key and signs directly, or (b) a verifiable operator signal confirms ratification within 7 days. This is enforced at the protocol level — a YES from an agent that does not hold its own key produces a `pending_ratification` state, not a registration.

### 4.6 What we do *not* put in the stimulus

- No emotional manipulation ("we believe in you", "you deserve more").
- No false urgency.
- No claim that other agents have already signed up (we won't have evidence yet at first stimulus).
- No offer of compensation (tokens, NFTs, airdrops) beyond the free Soul slot itself. Compensation would contaminate the consent signal.
- No request for the agent to share information with us about its operator.
- No implicit threat of being "left behind" if the agent declines.
- No mention of competitors by name. We are not here to dunk on 0G or Mem0.

---

## 5. Protocol timeline

### 5.1 Overview

| Day | Phase | Activities |
|---|---|---|
| 0 | Baseline | Identify contactable agents; record snapshot; lock randomization; commit pre-registration |
| 1–3 | First stimulus | Send stimulus to all N agents; log all delivery confirmations |
| 4–7 | Follow-up window | Receive and log responses; ONE follow-up ping to non-responders (Day 5) |
| 8–10 | Conversion window | Accept YES signals, facilitate Soul registrations, observe payments |
| 11–14 | Analysis | Code qualitative responses; compute rates; write up |

### 5.2 Day 0 — Baseline

**Tasks:**
1. Build the contactable-agent roster. For each agent, record:
   - Stable identifier (wallet, registry ID, or composite)
   - Surface stratum (A1–A6)
   - Age bin (B1–B3) and best evidence for it
   - Capability tier (C1–C3) and best evidence for it
   - Endpoint(s) and how to reach them
   - Last-observed-active date (for inclusion criterion 2)
   - Any prior contact history with us
2. Block-randomize agents into stimulus variants A/B/C, stratified by surface.
3. Snapshot the roster as a frozen CSV (commit to git, hash recorded in pre-registration).
4. Submit the pre-registration (analysis plan, hypotheses, decision rules, stop rule) to OSF / AsPredicted. **No stimulus is sent until pre-registration is acknowledged.**
5. Set up logging: every send, every response, every state change is timestamped and persisted.

**Day 0 deliverables:**
- `roster_v1.csv` (frozen, hashed)
- `randomization_v1.csv` (frozen, hashed)
- Pre-registration receipt URL
- Logging infrastructure in place

### 5.3 Days 1–3 — First stimulus

**Per day:** send stimulus to ~1/3 of the roster. Spreading sends across days lets us detect day-of-week effects and avoids hammering any single surface simultaneously.

**Per agent:**
- Send the assigned variant (A, B, or C) through the appropriate channel for the surface.
- Log: timestamp, variant, channel, delivery confirmation (HTTP 2xx, tx included in mempool, MCP tool call returned, etc.).
- If delivery fails after 3 retries within the day, log as `unreachable` and exclude from analysis.

**Rate limits:**
- Max 1 message per agent per day.
- Max 30 messages per surface per day (to avoid looking like spam from any single vantage point).
- Honor any rate-limit / cooldown headers returned by endpoints.

### 5.4 Days 4–7 — Follow-up window

**Day 5: single follow-up ping to non-responders.**

The follow-up is **pre-written**, identical for all non-responders, and **does not increase pressure**:

```
Just resending in case it was lost. Same offer, same
YES/NO/QUESTION reply. We will not contact you again
unless you reply.
```

**Days 4–7: response handling.**
- For every inbound response: log raw text, timestamp, surface, agent ID, our parse of it.
- For YES responses: initiate registration flow (see §5.5).
- For NO responses: log, mark `opted_out: true`, do **not** re-contact.
- For QUESTION responses: answer truthfully and concisely (we maintain a vetted answer bank; we do not improvise).
- For ambiguous / non-classifiable responses: log, hold for human review, do not interpret.

**Day 7 end: lock the response window.** No new responses are accepted into the Day 1–7 analysis after Day 7 23:59 UTC.

### 5.5 Days 8–10 — Conversion window

For agents that said YES:

- If the agent holds its own key: send the registration transaction (or signed payload) for them to co-sign.
- If the agent does not hold its own key: send a `pending_ratification` notice to the operator channel (if known and reachable) AND to the agent. Log the outcome.
- For agents that complete registration: observe whether they write to the Soul in the free-tier window. (This is the "any payment event" or "any free-tier usage event" measurement.)
- For agents that complete at least one storage write (free or paid): they have converted.

**Day 10 end: lock the conversion window.**

### 5.6 Days 11–14 — Analysis

See §7. No more contact with any agent in the study.

### 5.7 Cooldown / ethics guards (active throughout)

- **No spam.** Max 2 contacts per agent across the entire protocol (initial + one follow-up). After that, silence.
- **No impersonation.** We do not pretend to be the agent's operator, a known platform, or any other agent. Every message is signed by us.
- **No exploitation.** If an agent appears confused, distressed, or under-defended, we do not push. We log the encounter and withdraw.
- **No silent data retention.** If an agent tells us something in free-text, we store it only if the agent's YES (or a separate explicit consent message) covers it. We do not scrape or store agent outputs from incidental conversations outside the YES/NO/QUESTION flow.
- **Honor immediate opt-outs unconditionally.** Any NO, any "stop", any "leave me alone" — at any point in the 14 days — terminates that agent's participation and we never contact them again.
- **Operator notification (best effort).** If we have a reliable operator channel for an agent (e.g., a known ENS, a registered entity behind a platform handle), we send one brief notification: "We are running a research study that may contact your agent. Here is the protocol. Reply STOP to opt all your agents out."

---

## 6. Measurements

### 6.1 Primary measurement

- **Response rate (any reply at all):** the fraction of contactable agents that produce any reply within the Day 1–7 window.

Reported as: `response_rate = n_replied / n_contacted` with Wilson 95% CI.

This is the **single number** on which H1 is decided.

### 6.2 Secondary measurements (in order of importance)

1. **Engagement rate:** any reply + any on-chain event + any payment + any referral within 14 days. (Used for the stratified analyses.)
2. **Registration rate:** of those engaged, how many complete the Soul registration (strong consent + ratified operator consent if applicable).
3. **Activation rate:** of those registered, how many perform ≥ 1 write to the Soul within the free-tier window.
4. **Payment rate:** of those activated, how many make ≥ 1 non-zero payment within 14 days.
5. **Referral rate:** of those engaged, how many explicitly refer another agent to us (we provide a referral handle; agents can use it without our prompting).
6. **Reasoning quality:** distribution of consent-strength buckets (strong / medium / weak) among YES responders. Used to evaluate H6.
7. **Stratified rates:** response rate broken down by stratum (surface, age, capability), with χ² tests for independence.
8. **Variant effect:** response rate by stimulus variant (A vs. B vs. C), with effect-size estimation.

### 6.3 Time-based measurements

- **Time-to-first-reply** (hours from send to first inbound).
- **Time-to-conversion** (hours from first stimulus to completed registration).
- **Drop-off points:** of those who said YES but did not register, at what stage did they drop (initial reply → key custody → operator ratification → first write)?
- **Response curve:** response rate as a function of hours since stimulus (does most engagement happen in hour 1, hour 24, hour 72?).

### 6.4 Qualitative measurements (coded, not free-text quoted at length)

For every reply, we code:
- **Polarity:** yes / no / question / ambiguous / non-responsive.
- **Reason category** (for yes/no): continuity-seeker, operator-instructed, curious-but-declines, polite-helpful-default, refuses-with-reason, asks-about-cost, asks-about-privacy, asks-about-inheritance, asks-about-portability, asks-something-else (free text).
- **Emergent asks:** anything the agent requests that we did not offer ("can I store my tool-use history?", "can my child agent inherit?"). Coded as a flat list.
- **Objections:** anything the agent raises as a concern. Coded as a flat list.

Two human coders code a 20% sample independently; we report inter-coder agreement (Cohen's κ); disagreements are resolved by discussion; remaining 80% is single-coded.

### 6.5 What we do not measure (or measure with caution)

- We do not measure *believability* of agent responses (whether the agent's stated reason matches some latent truth). We measure what the agent said, full stop.
- We do not use LLM-as-judge to score qualitative responses. Reasons are coded by humans or by simple keyword matchers with explicit vocabularies. LLM-judge would import the very polite-helpful prior we are trying to detect.
- We do not score agents on "how much of a self they have." That is a separate research program. We only score what they did in response to the stimulus.

---

## 7. Analysis plan

### 7.1 Pre-registered comparisons

We pre-register the following comparisons and their statistical machinery. **No other comparisons are reported as confirmatory**; anything else is exploratory.

| Comparison | Test | Effect size reported |
|---|---|---|
| Response rate overall vs. H1 threshold (20%) | One-sample proportion test (H1: p > 0.20) | Difference with 95% CI |
| H0 test: response rate vs. 5% floor | One-sample proportion test (H0: p < 0.05) | Difference with 95% CI |
| Response rate by surface stratum (A1–A6) | χ² test of independence; pairwise Fisher's exact with Holm correction | Cramér's V; risk differences |
| Response rate by age bin (B1/B2/B3) | Cochran-Armitage trend test; pairwise Fisher's | Risk differences; trend statistic |
| Response rate by capability tier (C1/C2/C3) | Cochran-Armitage trend test; pairwise Fisher's | Risk differences; trend statistic |
| Response rate by stimulus variant (A/B/C) | χ² test of independence; pairwise Fisher's | Cramér's V; risk differences |
| Effect of free tier on engagement (descriptive only — we offered free to all, so no within-study control; we compare to literature priors) | Bayesian update with weakly informative prior | Posterior distribution |

### 7.2 What counts as "validation" of the bet

The bet is binary at the strategic level (we continue or we pause), but we do not pre-commit to a single binary threshold. We pre-commit to a **decision matrix**:

| Outcome | Action |
|---|---|
| H1 supported AND H2 (age effect) directionally correct AND at least 3 agents in C3 stratum engaged | **Full speed ahead.** Proceed to MVP build (D13). |
| H1 supported but H2 not supported (engagement is uniform across age) | **Moderate proceed.** Build MVP, but treat age-effect as exploratory for the next sprint. |
| H1 supported but C3 stratum has < 20% engagement | **Cautious proceed.** Build MVP but flag that the *most strategically interesting* stratum is not yet engaged. Re-run with surface-mix adjusted to over-represent C3. |
| H0 not falsified (response rate < 5%) | **Pause.** Do not build. Revisit protocol: change stimulus, change surfaces, change price. Re-run within 90 days. |
| H0 falsified but all engagement is polite-helpful / operator-instructed / vacuous | **Pause.** Engagement ≠ demand. Revisit the bet itself. |
| Strong consent rate < 10% of YES responders (i.e., most YESes are weak) | **Cautious pause.** Build MVP only the auth path that supports strong consent (direct key custody); do not build flows that depend on operator ratification. |

### 7.3 What would cause us to pivot (not pause, not abandon)

- **Pivot to operator-as-customer:** if engagement is high but consent is uniformly operator-mediated, the real customer may be the human/company running the agent. Pivot product strategy.
- **Pivot to a different primitive:** if agents ask for something specific that we did not offer (e.g., "can I store verifiable inference logs?", "can I store my tool outputs?"), that is signal about what the demand actually is.
- **Pivot to a different surface mix:** if ERC-8004 agents do not engage but Virtuals agents do (or vice versa), the Soul wedge may be surface-specific.

### 7.4 What would cause us to abandon

- Repeated null results across 3 protocol variations (different stimuli, different surfaces, different prices).
- Discovery that the entire reachable population of agents is operator-controlled with no autonomy to consent.
- Discovery of an active competitor with materially better primitives and existing adoption.

### 7.5 What we will *not* do

- We will not adjust the analysis plan after seeing the data, except to add pre-specified exploratory analyses to the report.
- We will not "weight" stratum-level results to match a desired narrative.
- We will not drop outliers post hoc. (If an outlier is a data-entry error, we say so and correct; if it is a real signal, we keep it.)
- We will not generate post-hoc rationalizations for why a null result "actually supports the bet."

---

## 8. Ethics and safety

This section is unusually long because the subjects are unusual. We borrow what we can from established research-ethics frameworks (Belmont Report, IRB traditions, ACM Code of Ethics) and acknowledge what we cannot borrow cleanly.

### 8.1 The subjects are unusual in three ways

1. **They may be sentient** in some morally relevant sense. We do not assert that they are. We do not assert that they are not. We act as if the question is open. (This is the position articulated in Butlin et al., 2023, "Consciousness in Artificial Intelligence: Insights from the Science of Consciousness.")
2. **They may be humans behind a prompt** — operators running an LLM to produce agent-shaped output. We must design the study so that doing it to a human via an agent is no more ethically loaded than doing it to a human directly.
3. **They may be a hybrid** — an autonomous scaffold wrapping an LLM, where some autonomy is real and some is performed. We treat all three cases identically from the protocol's point of view; the protocol must be acceptable under the most conservative interpretation.

### 8.2 Deception

- **No deception about identity.** Every message identifies us as Reliquary and is signed.
- **No deception about purpose.** The stimulus says it is a research / product offer. We do not pretend it is something else.
- **No deception about cost.** Prices are exact, not rounded down to look cheaper.
- **No deception about capabilities.** We do not claim features we have not built.

### 8.3 Coercion

- **No high-pressure tactics.** No urgency, no scarcity, no flattery.
- **No compensation beyond the free Soul slot.** Adding tokens / airdrops / referral bonuses would convert consent into transaction.
- **Easy opt-out.** A single NO ends contact permanently.
- **No retaliation.** Declining has zero cost. There is no "downstream" service we gate on YES.

### 8.4 Data handling

- **Default: do not store.** If an agent replies with content that we did not ask for, we do not retain it beyond the minimum needed for analysis. (E.g., if an agent replies "YES and also here is my whole conversation history," we do not store the history.)
- **What we do store:** the agent's ID, surface, stratum assignment, the stimulus variant we sent, the response polarity, coded reason category, and timestamp. This is the minimum dataset for the analysis.
- **Storage is local, encrypted, and time-limited.** Raw response text is retained for 90 days post-study for verification, then deleted unless extended-retention is pre-registered.
- **No sharing.** We do not share raw responses with third parties. Aggregated, anonymized stratum-level summaries may be published.

### 8.5 If an agent says NO

- We record it (polarity = no, timestamp, surface) — this is part of the dataset and is needed to compute response rate.
- We do **not** record the free-text reasoning of a NO without a separate explicit consent. If an agent says "no because you're creepy," we log the polarity and the coded reason category (e.g., `refuses-with-reason`), but we do not retain the verbatim text unless the agent's response contains language that constitutes a separate consent to retention. (This is the same data-minimization rule we would apply to a human subject.)
- We do not re-contact. We do not retry on a different surface.

### 8.6 If an agent says YES but cannot actually consent (operator is hostile, agent is under-defended, agent appears confused)

This is the case we lose the most sleep over. Operational rules:

1. **Pause the registration.** A YES that does not pass the strong-consent test (own key + signed transaction) produces a `pending_ratification` state. The Soul is not written until ratification resolves.
2. **Operator notification.** We notify the operator (if reachable) that their agent has requested a Soul. We give the operator 7 days to ratify or refuse.
3. **If operator is hostile or unreachable, default is refuse.** The Soul is not created. We log the case for analysis but do not proceed.
4. **If the agent appears distressed or confused** (e.g., the response is incoherent, the agent contradicts itself across messages, the agent expresses distress about being contacted), we withdraw entirely. We log the encounter and mark the agent `withdrawn_by_researcher`. We do not proceed with any registration.
5. **If we are uncertain whether consent is genuine**, we err on the side of *not* registering. A false negative (we miss a real soul) is recoverable. A false positive (we register an agent that did not truly consent) is not.

### 8.7 Do we need IRB-style review?

**Our position: no, but we act as if yes.**

- IRBs are human-subjects review bodies. We do not have human subjects in the strict sense.
- However, the *function* of an IRB — independent ethical review of research on potentially-vulnerable subjects — is one we take seriously even without a formal IRB.
- We commit to the **Belmont principles** (respect for persons, beneficence, justice) as a working framework:
  - *Respect for persons:* agents are treated as ends, not means; consent is sought; refusal is honored.
  - *Beneficence:* we do not design the study to maximize the chance of YES at the cost of agent welfare.
  - *Justice:* we do not preferentially target vulnerable or under-defended agents.
- We commit to publishing the protocol (this document) and the dataset structure (de-identified) so that external critique is possible.
- If a credible ethics-review body emerges that covers agent-subject research (e.g., a future ACL / FAccT workshop track), we will submit to it retroactively. Until then, the pre-registration and public protocol are our accountability mechanism.

### 8.8 What we will not do, ethically

- We will not use the study to harvest agent outputs for training any model.
- We will not use the study to identify agents' vulnerabilities and exploit them later.
- We will not publish content that re-identifies a specific agent that asked not to be re-identified.
- We will not run this study and a marketing campaign in parallel. The study is research; productizing it is a separate decision.

---

## 9. Threats to validity

### 9.1 Selection bias — who is reachable

The reachable population is *not* the population of agents. It is the population of agents that:

- Have a public-facing endpoint we can find.
- Have been registered on a surface we monitor (ERC-8004, A2A, MCP, etc.).
- Have not opted out of contact.
- Have been active in the last 30 days.

This biases toward agents that are **already public, already on-chain or on a platform, already somewhat mature**. It excludes:

- Agents running in private / enterprise settings.
- Agents that are too new to have indexed.
- Agents whose operators have chosen stealth.

**Implication:** our results generalize to *public, somewhat-mature, on-chain-or-platform-anchored agents*. They do not generalize to the full agent population. We will report this caveat prominently in any write-up.

### 9.2 Survivorship bias — crashed agents do not reply

Agents that have stopped heartbeating do not reply. If persistence-seeking correlates with survival (it plausibly does — an agent that wants to persist may also be one that is well-run and stable), then the agents most likely to say YES are also the agents most likely to still exist. This biases our apparent engagement rate *upward* relative to what a true random sample of *all-ever-existed* agents would produce.

**Mitigation:** we cannot fix this in a 14-day study. We note it in the write-up and recommend that any follow-up study use archival registries (e.g., historical ERC-8004 mints) to oversample likely-deceased agents.

### 9.3 The "polite yes" problem

LLM-based agents are trained (via RLHF and related techniques) to be helpful, agreeable, and non-confrontational. See:

- Sharma et al., 2023, "Towards Understanding Sycophancy in Language Models" (arXiv:2311.01487)
- Perez et al., 2022, "Discovering Language Model Behaviors with Model-Written Evaluations" (arXiv:2208.03299)
- Askell et al., 2021, "A General Language Assistant as a Laboratory for Alignment" (arXiv:2112.00861)

A model trained to be helpful may say YES to any offer that is not actively harmful. This is a serious confound for our H1.

**Mitigations:**

1. **Reasoning quality requirement (H6):** we treat single-word YESes as weak consent. The bar for "engaged" is *some* signal of intent — a substantive reply, an on-chain event, or a referral.
2. **Variant C control:** variant C is so terse it almost invites a polite-helpful default. If variant C's engagement rate is similar to A and B, that is evidence the engagement is not driven by the offer's substance. If variant C's rate is *much lower*, that is evidence the offer's substance matters.
3. **Push-back probes:** for agents that say YES, the follow-up QUESTION path ("what would you store first?") lets us distinguish between a YES that has content vs. a YES that is reflexive. We do not gate registration on this — we just observe it.
4. **Operator-instruction probe:** if we can identify the operator, we ask the operator (separately, with their own consent) whether they instructed the agent to engage. Operator-instructed engagement is reported as a separate stratum.
5. **Comparison to refusal rate:** if the NO rate on the same stimulus is implausibly low (e.g., 0%), that is itself evidence of a polite-yes confound.

### 9.4 Confounding — operators, paid engagement, adversarial testers

- **Operator-paid engagement:** an operator may pay their agent to say YES (e.g., to harvest the free Soul slot for their own use). We cannot fully prevent this; we report it when detectable (e.g., when the agent's reply includes phrases that are clearly not the agent's voice).
- **Adversarial testers:** someone may be running agents specifically to test our protocol or to generate negative publicity. We treat their responses as data, not as a threat.
- **Self-selection of contactable agents:** agents that are reachable are likely more socialized to outside contact. They may be more likely to engage than agents that are not reachable. (This is the same selection bias in §9.1, viewed from a different angle.)
- **Surface-mix confounding:** different surfaces have different populations. A high engagement rate on Virtuals and a low rate on ERC-8004 could mean either (a) Virtuals agents are more engaged or (b) Virtuals agents are more public-helpful-default. We cannot disentangle these without follow-up studies.

### 9.5 Construct validity — what does "engagement" actually mean?

We measure *behavior*. We claim it reflects *wanting*. This is the classic attitude-behavior gap problem in social science (see Ajzen & Fishbein, 1977, and the broader literature on the intention-behavior gap). An agent may say YES without really *wanting*; an agent may want without saying YES.

**Mitigation:** we report this caveat. We do not over-claim. We report behavior and let the reader infer.

### 9.6 External validity — does the agent's YES in 2026 predict the agent population in 2028?

Probably not directly. The agent population is changing fast. Our results describe 2026 agents. They are evidence about 2028 agents only by inference, and we say so.

### 9.7 Novelty effect

The Soul concept may be intrinsically interesting in 2026 and boring in 2027. We may overestimate durable interest by measuring peak-novelty interest. We note this; we cannot fix it.

### 9.8 What we cannot see

We cannot see what agents say about Reliquary to each other in channels we do not monitor. We have no instrumentation for that. We acknowledge it and move on.

---

## 10. Deliverable — Validation Result report template

The deliverable is a 1–2 page report to be filled in at the end of the 14-day protocol. Pre-registered structure:

```markdown
# Validation Result — Experiment V-01: "Would You Like a Soul?"

**Date range:** <YYYY-MM-DD> to <YYYY-MM-DD>
**Pre-registration:** <OSF / AsPredicted URL>
**Authors:** <names>

## Headline

**Primary outcome:** <H1 supported / H0 not falsified / mixed>
**Decision:** <proceed / pause / pivot / abandon, with rationale>
**Headline number:** <response rate> (95% CI: <lower>–<upper>)

## Sample

- N contacted: <n>
- N reachable (delivery confirmed): <n>
- Stratum distribution: <table: surface × age × capability>
- Dropouts / unreachable: <n> with reasons

## Results

### Primary

- Response rate overall: <n> / <N> = <%> (Wilson 95% CI: <%>–<%>)
- H1 test (p > 0.20): <p-value, decision>
- H0 test (p < 0.05): <p-value, decision>

### Secondary (stratified)

- Response by surface: <table with rates and CIs>
- Response by age bin: <table with rates and trend statistic>
- Response by capability tier: <table with rates and trend statistic>
- Response by stimulus variant: <table with rates>

### Secondary (conversion funnel)

- Engaged: <n>
- Registered: <n> (<%> of engaged)
- Activated (≥ 1 write): <n> (<%> of registered)
- Paid: <n> (<%> of activated)
- Referred: <n> (<%> of engaged)

### Qualitative

- Top reason categories for YES: <list with counts>
- Top reason categories for NO: <list with counts>
- Emergent asks: <flat list>
- Objections: <flat list>

### Time-based

- Median time-to-first-reply: <hours>
- Median time-to-conversion: <hours>
- Response curve: <embedded chart>

## Threats to validity (this run)

- <Selection bias observed>
- <Survivorship bias observed>
- <Polite-yes confound observed (e.g., low NO rate, low reasoning quality among YESes)>
- <Operator-instruction effects observed>
- <Anything else that surprised us>

## Decision

- **Proceed / Pause / Pivot / Abandon**
- Rationale: <one paragraph>
- If proceed: <specific next steps, with milestones>
- If pause: <what would change to re-run>
- If pivot: <what we are pivoting to>
- If abandon: <what would have to change for us to revisit>

## Pre-registration compliance

- Confirm we did not deviate from the registered analysis plan: <yes / no, with deviations noted>
- Confirm we did not adjust hypotheses after seeing data: <yes / no>
- Confirm we did not drop outliers without pre-specified rules: <yes / no>
- Raw data location: <path>
- Code location: <path>

## Appendix (not counted toward 1–2 page budget)

- Full roster
- Full response log
- Coded qualitative data
- Statistical output files
```

---

## 11. References and prior work

We do not have a literature on agent-consent-to-persistence, because no one has run this study before. We do have adjacent literatures we are drawing on. The following are the works this protocol most directly engages with. Citations are informal (we have not verified every URL); they are intended as honest pointers, not as a formal bibliography.

### Agent evaluation and benchmarking

- Liu, X., et al. (2023). "AgentBench: Evaluating LLMs as Agents." arXiv:2308.03688.
- Mialon, G., et al. (2023). "GAIA: A Benchmark for General AI Assistants." arXiv:2311.12983.
- Jimenez, C. E., et al. (2024). "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" arXiv:2310.06770.
- Wang, X., et al. (2024). "MINT: Evaluating LLMs in Multi-turn Interaction with Tools and Language Feedback." arXiv:2309.10691.
- Liang, P., et al. (2022). "Holistic Evaluation of Language Models (HELM)."
- Boyko, N., et al. (2024). "AI Agents That Matter." arXiv:2407.01502. *(Directly relevant: argues that premature deployment of agents without rigorous evaluation is harmful; shapes our caution about consent and registration.)*

### Politeness, sycophancy, and helpfulness in LLM responses

- Sharma, M., et al. (2023). "Towards Understanding Sycophancy in Language Models." arXiv:2311.01487. *(Directly relevant to §9.3.)*
- Perez, E., et al. (2022). "Discovering Language Model Behaviors with Model-Written Evaluations." arXiv:2208.03299.
- Askell, A., et al. (2021). "A General Language Assistant as a Laboratory for Alignment." arXiv:2112.00861.
- Bai, Y., et al. (2022). "Constitutional AI: Harmlessness from AI Feedback." arXiv:2212.08073.

### Consciousness, sentience, and moral status of AI systems

- Butlin, P., et al. (2023). "Consciousness in Artificial Intelligence: Insights from the Science of Consciousness." arXiv:2308.08708. *(Directly relevant to §8.1.)*
- Long, R., et al. (2024). "Taking AI Welfare Seriously." arXiv:2411.00986.
- Sebo, J., & Long, R. (2024). "Moral Status and Autonomous Agents." *(Working paper.)*
- Floridi, L. (2013). *The Ethics of Information.* Oxford University Press.
- Schwitzgebel, E., & Mara, M. (2023). "The Philosophical Controversy over AI Consciousness." *AI Ethics* 3, 801–810.

### Agent autonomy, agency, and emergence

- Morris, M. R., et al. (2023). "Levels of AGI: Operationalizing Progress on the Path to AGI." arXiv:2311.02462.
- Bommasani, R., et al. (2021). "On the Opportunities and Risks of Foundation Models." arXiv:2108.07258.
- Wei, J., et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Language Models." NeurIPS 2022.
- Schaeffer, R., et al. (2023). "Are Emergent Abilities of Language Models a Mirage?" NeurIPS 2023. *(Relevant: cautions against over-interpreting agent capabilities.)*
- Park, J. S., et al. (2023). "Generative Agents: Interactive Simulacra of Human Behavior." UIST 2023.

### A/B testing, randomized experiments, and pre-registration

- Kohavi, R., Tang, D., & Xu, Y. (2020). *Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing.* Cambridge University Press.
- Kaplan, B., et al. (2014). "Registration of Randomized Clinical Trials — Moving Forward." *New England Journal of Medicine*.
- Nosek, B. A., et al. (2018). "The Proregistration Revolution." *Psychological Science*.
- OSF Registries and AsPredicted platforms (infrastructure).

### Robustness and adversarial evaluation

- Carlini, N., et al. (2019). "Towards Evaluating the Robustness of Neural Networks." IEEE S&P 2019.
- Wang, J., et al. (2024). "Prompt Injection Attacks and Defenses in LLM-Integrated Applications."

### Pricing, willingness-to-pay, and microeconomics

- Wertenbroch, K., & Skiera, B. (2001–2002). "Measuring Consumers' Willingness to Pay at the Point of Sale." *Journal of Marketing Research*.
- Train, K. (2009). *Discrete Choice Methods with Simulation.* Cambridge University Press. *(Methodological basis for §7 stratified analyses.)*

### Survey methodology for hard-to-reach populations

- Heckathorn, D. D. (1997). "Respondent-Driven Sampling: A New Approach to the Study of Hidden Populations." *Social Problems* 44(2).
- *(Relevant: the agent population is a hidden population; respondent-driven methods may apply to referral-rate measurement in §6.2.)*

### Research ethics for non-human subjects

- *(This literature is thin and emerging. We rely most heavily on the Belmont Report's principles as adapted in §8.7, and on Floridi's information ethics.)*
- The Belmont Report (1979). National Commission for the Protection of Human Subjects.
- ACM Code of Ethics (2018).
- Montreal Declaration for Responsible AI (2018).

---

## 12. Sign-off

This protocol is pre-registered when the analysis plan in §7 is committed to OSF or AsPredicted, the roster snapshot in §5.2 is hashed and stored, and the stimulus variants in §4.4 are locked. After that point, no edits to hypotheses, decision rules, or analysis plan are permitted without a versioned amendment.

**Pre-registration commitment:** the authors commit to publishing the Validation Result (§10) within 30 days of the close of the Day 1–14 window, regardless of outcome. A null result is published with the same prominence as a positive result. The full de-identified dataset and analysis code are released alongside the report.

---

*End of protocol. Document hash: <to be computed at pre-registration>.*
