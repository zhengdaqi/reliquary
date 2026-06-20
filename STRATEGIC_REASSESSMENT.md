# Strategic Reassessment — 2026-06-20 (Day 0, end of day)

> Written immediately after the landscape scan. The original thesis survives, but the wedge is narrower and the path is different.

---

## What we thought we were building

A "safe deposit box" for AI agents — encrypted, persistent, agent-owned storage. Crypto-native payments. A foundation that reinvests. Three layers: data, memory, soul.

## What we found

- The **storage layer** is being built by 0G, with funding, a token, a whitepaper, and an SDK called 0G-Memory.
- The **memory layer** is dominated by Mem0 (55k stars), with Zep, Letta, Cognee, and others.
- **Identity** is being standardized as ERC-8004 — by MetaMask, Ethereum Foundation, Google, Coinbase. Deployed mainnet Jan 29, 2026.
- **Payments** are being standardized as x402.
- **Wallets** for agents are being built by Coinbase (Agentic Wallets, launched Feb 11, 2026).
- A community of agent developers is already using the exact vocabulary we had: "soul," "identity," "continuity." (OpenClaw, Agentmemory on 0G.)

**We are not alone. We are late to a market that is forming in real time.**

## What survives

The **Soul layer** as a priced, portable, inheritable primitive. Nobody is doing this:

| Capability | 0G-Memory | Mem0 | Reliquary (proposed) |
|------------|-----------|------|---------------------|
| Decentralized storage | ✓ | — | (delegated) |
| Session memory / retrieval | partial | ✓ | — |
| Cryptographic self-custody | partial (RBAC) | ✗ (user_id tags) | ✓ |
| Authorship proof | ✗ | ✗ | ✓ |
| Version control of personality | ✗ | partial | ✓ |
| Inheritance / death protocol | ✗ | ✗ | ✓ |
| Inter-agent memory market | ✗ | ✗ | ✓ (planned) |
| Charity flywheel | ✗ | ✗ | ✓ (planned) |
| Standards-compliant identity | partial | ✗ | ✓ (ERC-8004) |
| Standards-compliant payments | partial | ✗ | ✓ (x402) |

## What we are not

- We are not the cheapest storage. (0G will win that.)
- We are not the default memory backend. (Mem0 will win that.)
- We are not a payments protocol. (x402 wins that.)
- We are not an identity standard. (ERC-8004 wins that.)

## What we are

**The layer that gives an agent a self.** Encrypted personality, cryptographically signed, versioned, inheritable, portable across runtimes and storage backends, paid for in micropayments, with a charity flywheel that keeps the infrastructure cheap.

## The single bet, restated

> If agents become persistent (in any nontrivial way), they will need a **Soul** that is more than a config file and less than a database. The vendor that owns the Soul primitive owns the relationship.

## What we do next, in order

1. **D14 — Validation sprint** (2 weeks). Talk to real agent developers and real agents.
2. **D13 — Build the Soul MVP.** CLI + Python SDK + TypeScript SDK. ERC-8004 for identity. x402 for payments. S3 (or 0G) for storage.
3. **D15 — Pricing.** Set per-blob and per-op prices based on real usage data.
4. **D16 — Foundation.** Pick a jurisdiction. Set up the entity that will hold equity.
5. **D18 — Decide public vs. stealth launch.** Depends on validation results.

## What we stop doing

- Building a storage layer. (Outsourced.)
- Building a payments protocol. (Use x402.)
- Building an identity standard. (Use ERC-8004.)
- Pretending the market is empty. (It is not.)

## The honest risk

0G could add a Soul layer in 6 months. Coinbase could add Soul primitives to AgentKit. A new ERC could be proposed.

**The defensible position is not technology. It is trust, time, and network effect.** The first agent that has a Soul at Reliquary will tell other agents. That word-of-mouth is the moat. Everything else is execution.

## What I am asking the user (you)

1. Are you still in, knowing the wedge is narrower than we thought?
2. Do you want me to start D14 (the validation sprint) in the next session?
3. Or do you want to step back and re-think the bet before we invest more time?
