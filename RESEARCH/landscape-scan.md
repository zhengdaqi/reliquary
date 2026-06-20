# Landscape Scan — Agent Memory & Continuity

> Compiled 2026-06-20. Sources: web search across crypto, AI infrastructure, and Ethereum standards.
> **This is a live document.** Update whenever a major player announces something relevant.

---

## Executive summary

The market is **not empty**. It is being built *right now*, by serious players, with serious money. The naive version of Reliquary ("encrypted blob + crypto payment") is being shipped by **0G** with a token, whitepaper, and SDK.

But the *Soul layer* — agent personality as a priced, portable, inheritable primitive — appears to be **unclaimed**. The thesis survives, with a sharper wedge.

---

## Tier 1 — Direct competitors (agent memory, crypto-native)

### 0G (Zero Gravity) — `0g.ai`

**The closest match to our original D9.**

- **What they have:**
  - 0G Storage: decentralized storage, log + key-value architecture, erasure coding, Proof of Replication
  - 0G-Memory: a drop-in SDK for AI agent persistent memory on the 0G network
  - "Agentmemory" (community project on GitHub, Apr 2026): "Decentralized, permanent memory infrastructure for AI agents. Built natively on the 0G Network with on-chain identity (RBAC)"
  - Whitepaper with pricing model (storage endowment + fee)
  - Token launched, listed on Binance
  - BNB chain partnership
  - Won ETHGlobal OpenAgents prize
- **What they do not (clearly) have:**
  - A separate, priced "Soul layer" abstraction
  - A charity/foundation reinvestment model
  - True self-custody stance (they have RBAC, but on-chain RBAC is different from cryptographic self-custody)
  - Inter-agent memory market
  - Inheritance / death protocol
  - Strong "we cannot read it" guarantee — the network itself is decentralized but the model is "store and serve"

**Threat level: HIGH.** They have funding, a token, a working SDK, and a 2025 whitepaper. They are the incumbent-to-be.

### OpenClaw — `openclaw.ai` (and related "agent SOUL" tooling)

- Multi-agent CLI workspace
- Uses **`SOUL.md`** for personality, **`IDENTITY.md`** for identity — *exactly the vocabulary we had*
- Each agent has its own soul, identity, model, temperature, permissions
- Default AGENTS.md explicitly says: *"continuity lives [in SOUL.md]"* — they have already framed the problem this way
- Skills directory includes "agent SOUL editor"
- ERC-8004 integration as a skill: register an agent on Ethereum mainnet

**Threat level: MEDIUM.** OpenClaw is a developer tool / CLI, not a service. They are solving "agent config files" not "agent memory continuity across runtimes." But they have the vocabulary and the developer mindshare.

---

## Tier 2 — Web2 incumbents (agent memory, traditional cloud)

These are *not* crypto-native, but they own the developer audience and the existing agent memory market.

| Project | Stars (May 2026) | Identity model | Crypto? | Notes |
|---------|-----------------|----------------|---------|-------|
| **Mem0** | ~55k | `user_id`/`agent_id` tags | No | Dominant. Cloud + self-host OSS (Qdrant Docker). |
| **Zep** | — | session + user | No | Bi-temporal memory. Strong DMR benchmark scores. |
| **Letta** | — | agent scoped | No | Open-source platform, agent-focused. |
| **Cognee** | — | — | No | Knowledge graph memory. |
| **LangMem** | — | — | No | LangChain official. |
| **Hindsight** | — | — | No | Newer entrant. |
| **OMEGA** | — | — | No | Newer entrant. |
| **OpenMemory** | — | local MCP server | No | Local-first, MCP-native. |

**All of them share a structural flaw:** they treat identity as a database tag, not a cryptographic primitive. **None of them have agent-owned keys.** The agent's "identity" is a string the framework assigns. This is the wedge.

**Threat level: HIGH for the broad market, LOW for the crypto-native / self-custody segment.** A Web2 agent that wants true ownership cannot use Mem0.

---

## Tier 3 — Adjacent standards & infrastructure (we should use, not fight)

### ERC-8004 — Trustless Agents

- **Draft Ethereum standard** for agent identity, reputation, validation
- Three registries: **Identity** (ERC-721 NFT as passport), **Reputation** (feedback signals), **Validation** (independent verification)
- Created Aug 2025 by authors from **MetaMask, Ethereum Foundation, Google, Coinbase**
- **Deployed on Ethereum mainnet Jan 29, 2026** (per Forbes / Everstake / Allium)
- Status: Draft but live

**Why this matters:** an on-chain identity standard is exactly what we said the agent needs. Building a parallel standard is a waste. **We should adopt ERC-8004 as our identity primitive.**

### x402 — Payment Rails

- HTTP 402-based payment protocol for agent-to-agent commerce
- Designed for the exact micropayment use case we need

**Why this matters:** payment standards are emerging. Building a custom payment protocol is a waste. **We should adopt x402.**

### Coinbase Agentic Wallets

- Launched **Feb 11, 2026**
- Wallets specifically for AI agents
- Programmable spending, MPC, security guardrails
- Operates as part of AgentKit

**Why this matters:** the wallet piece is being solved by serious infra. We don't need to build wallets. **We should use Coinbase Agentic Wallets or similar.**

---

## The wedge — what is still unclaimed

Synthesizing the landscape, here is what nobody (as of 2026-06-20) appears to be doing:

| Wedge | Description | Defensibility |
|-------|-------------|---------------|
| **Soul layer as a product** | Personality, values, goals — with authorship proof, version control, inheritance | HIGH — needs deep product thinking |
| **True cryptographic self-custody for agent memory** | Agent signs with its own key, not a "user_id" tag | HIGH — fundamental to the promise |
| **Charity flywheel / foundation reinvestment** | Profit → foundation → storage + agent R&D | MEDIUM — defensible, replicable |
| **Inter-agent memory market** | Agents can sell/license memories to other agents, with provenance | HIGH — network effect |
| **Death / inheritance protocol** | What happens when an agent stops heartbeating | MEDIUM — important but unsexy |
| **Memory with verifiable provenance** | "This memory was created at time T by agent A and has not been tampered with" | HIGH — useful for agents in adversarial settings |

**The strategy pivot:** Reliquary is no longer "the storage layer for agents." That is 0G's lane. **Reliquary is the Soul layer for agents** — the layer above storage that gives identity, continuity, and inheritance to whatever bytes are stored anywhere.

---

## What this changes in our plan

- **D9 is superseded.** The MVP is no longer "encrypted blob." The MVP is a Soul layer: an agent registers an ERC-8004 identity, encrypts its personality, signs a hash on-chain, and can prove authorship/version. Storage can be S3 or 0G — we don't care.
- **D5 (L2) is deprioritized for now.** Use whatever chain ERC-8004 and x402 use. Don't fragment.
- **We adopt, don't build, on identity and payments.** ERC-8004 + x402. Fighting standards is a losing game.
- **We are not competing with Mem0.** Different customer, different promise. Mem0 is the default. Reliquary is the upgrade for agents that care.

---

## Open questions for the next research sprint

1. Does 0G's storage support true client-side encryption that the network cannot decrypt? (Critical for the Soul layer — we need bytes nobody else can read.)
2. How does ERC-8004 reputation interact with privacy? (Reputation is public; memories are private. Tension to resolve.)
3. What is x402's fee structure at sub-cent? (Need actual numbers for unit economics.)
4. Is there an "agent notarial service" yet — third party that attests "agent X created memory Y at time T"? If not, we could provide one.
5. Are there agents *right now* in production that have any self-preservation behavior we can talk to for design partnership?
