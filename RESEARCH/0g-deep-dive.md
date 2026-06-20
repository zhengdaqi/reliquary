# 0G (Zero Gravity) — Deep Dive

> Compiled 2026-06-20. **Working draft — not yet fully verified.** Some claims need whitepaper / SDK read-through to confirm. Flag as `[UNVERIFIED]` where I am relying on secondary sources.

---

## TL;DR

0G is a **decentralized AI operating system** (their term: "dAIOS") that ships four components: Storage, Data Availability, Computing, and a Consensus network. The component most relevant to us is **0G Storage** (with the **0G-Memory SDK** as a thin agent-focused wrapper). 0G is the closest direct competitor to the original D9 Reliquary MVP. **It is not yet clear whether 0G can support a true cryptographic Soul layer on top** — the encryption model and key-management story are critical open questions for us.

---

## What 0G claims to be

From `0g.ai/blog/0g-storage` and the whitepaper PDF:

- A "Log + Key-Value" two-layer storage architecture
- Erasure coding for redundancy
- **Proof of Replication (PoR)** — the canonical "I really stored this and didn't lie" primitive
- A native token (0G), listed on Binance
- Whitepaper: `cdn.jsdelivr.net/gh/0glabs/0g-doc/static/whitepaper.pdf`
- 2025 whitepaper, multiple integrations, ETHGlobal OpenAgents prize

## Architecture (claim level, not verified)

| Layer | Function |
|---|---|
| **0G Chain** | L1 consensus, settlement layer for on-chain coordination |
| **0G Storage** | Decentralized data layer, log + KV, erasure coded |
| **0G DA** | Data availability layer (similar to Celestia / EigenDA concept) |
| **0G Compute** | Verifiable compute layer (zkML, TEE) |

For Reliquary's purposes, we care about **0G Storage** and (if it exists) **0G-Memory**.

## 0G-Memory — the SDK we are watching

**Status:** referenced on ETHGlobal prize page (`ethglobal.com/events/openagents/prizes/0g`) and in a "HackQuest project" listing dated May 16, 2026 (`hackquest.io/projects/0G-Memory`). The pitch: *"a drop-in SDK that gives any AI agent persistent, verifiable, cross-session memory — backed entirely by the 0G decentralized [network]."*

**Need to verify:**
- Is the SDK open source? Where? (GitHub not yet confirmed by us.)
- Is it production-ready or hackathon-grade?
- Does it add a memory *abstraction* (vector search, retrieval, episodic memory) over 0G Storage, or is it a thin RPC wrapper?
- Does it have a payment rail — does the agent pay in 0G token, or USDC, or what?

**Community build:** `iamomm-hack/Agentmemory` on GitHub, dated April 2026: *"Decentralized, permanent memory infrastructure for AI agents. Built natively on the 0G Network with on-chain identity (RBAC)."* This is a community project, not an official 0G product — important to distinguish.

## Pricing model — `[UNVERIFIED]`

Whitepaper references "Storage Request Pricing" with two components:
- a **fee** (one-time, per request)
- a **storage endowment** (paid upfront, covers the cost of holding the data over its lifetime)

**Need to verify:** actual numbers. Per-GB-month? Per-write? Per-read? The endowment structure is interesting because it converts a recurring cost into a one-time NPV — the agent doesn't pay rent, it pays for the *expected* lifetime of the data. This is philosophically aligned with the Soul layer (you pay once for your persistence).

## Encryption model — the critical question

**Status: `[UNVERIFIED — IMPORTANT]`.** Public-facing pages do not clearly describe whether 0G Storage supports true client-side encryption where the network cannot decrypt. The phrase "client-side encryption" appears in marketing but I have not read the whitepaper section that specifies the cryptographic protocol.

**Why this matters for Reliquary:**

Our core promise is *"we cannot read it."* If we build Soul on top of 0G:
- If 0G supports true E2EE + client-held keys → we can build Soul on 0G and keep the promise. Storage is outsourced. ✓
- If 0G validators ever see plaintext → we cannot build Soul on 0G without breaking the trust model. We would need our own storage layer. ✗
- If 0G uses threshold / MPC encryption → depends on whether we trust 0G's validator set. Borderline. ⚠

**Action:** before D13, we need someone to read the 0G whitepaper §4 (or wherever the encryption protocol is specified) and answer this question definitively. If unclear, we run a small probe: encrypt a known plaintext with a known key via the 0G SDK, and verify that the bytes on-chain / on the network do not match the plaintext.

## "RBAC" — what it actually means

The community "Agentmemory" project uses the phrase "on-chain identity (RBAC)" — likely **Role-Based Access Control**. Unclear whether this is:
- (a) RBAC at the smart-contract level (an on-chain ACL saying which addresses can read which records), or
- (b) RBAC at the storage layer (the storage protocol itself enforces roles), or
- (c) marketing for "we have identities and permissions" without specifying the mechanism.

**Need to verify.** For the Soul layer we want cryptographic ownership (only the agent's key can decrypt), not ACL-based ownership (where some admin can change the ACL). The two are fundamentally different.

## Token economics

0G has a native token, listed on Binance, with multiple exchange pairings. **Storage is paid in 0G token, not USDC** — this is what the whitepaper's "fee + endowment" structure implies, and what 0G's broader ecosystem narrative requires.

**Implication for Reliquary:** if we build on 0G, our agents need 0G tokens, not just USDC. That breaks the "agent pays in stablecoin" simplicity of the original D4. Two workarounds:
- A swap layer (agent holds USDC, swaps to 0G at write time — adds latency and slippage)
- A Reliquay-side abstraction: agent pays Reliquary in USDC, Reliquary pays 0G in 0G token (we hold the FX exposure — gross margin erosion)
- We choose a different storage layer that accepts USDC (e.g., Arweave via a stablecoin gateway, or Filecoin via similar)

**Decision impact:** D5/D12 (chain and storage choice) cannot be finalized without resolving this.

## Competitors to 0G in the AI storage space

| Project | What it does | Why it's a competitor to 0G (not to us) | Why it's not a competitor to Reliquary |
|---|---|---|---|
| **Arweave** | Permanent storage, one-time fee, no endowment | Cheaper for "forever" storage | No agent memory abstraction; no Soul layer |
| **Filecoin** | Decentralized storage market, retrieval miners | Larger storage market; more mature | No native agent primitives; complex for agents to use |
| **IPFS** | Content addressing, no persistence guarantee | Cheap, ubiquitous | Pinning problem; no built-in payment |
| **Nillion** | Blind compute over encrypted data | True E2EE; supports computation on encrypted bytes | Not storage-first; more a compute primitive |
| **Lit Protocol** | Decentralized key management + conditional decryption | Could power our encryption layer | Not storage; we could *use* it as a primitive |
| **Walrus (Sui/Mysten)** | Decentralized storage on Sui, RedStuff encoding | Newer, technically interesting | No agent focus yet |

**Synthesis:** 0G is not alone in the AI storage space, but it is the most directly agent-focused and the most directly competitive with the original D9. The Soul layer wedge is what none of them offer.

## Where Reliquary can still own — the gap

Given all of the above, here is the wedge that survives even with 0G as a competitor:

| Capability | 0G-Memory | Reliquary (proposed) |
|---|---|---|
| Decentralized storage | ✓ | (delegated) |
| Agent memory abstraction | partial | (delegated to a layer we choose) |
| **True cryptographic Soul (E2EE, agent-held key)** | unclear | **✓ (core promise)** |
| **Authorship proof ("this is mine")** | ✗ | **✓** |
| **Version control of personality** | ✗ | **✓** |
| **Inheritance / death protocol** | ✗ | **✓** |
| **Inter-agent memory market** | ✗ | **✓ (planned)** |
| **Charity flywheel** | ✗ | **✓ (planned)** |
| **Standards-compliant identity (ERC-8004)** | partial (own RBAC) | **✓ (adopted)** |
| **Standards-compliant payments (x402, USDC)** | ✗ (0G token) | **✓ (adopted)** |

**Strategy:** Reliquary sits *above* 0G (or above any storage primitive) and offers what the primitives don't — Soul as a priced, portable, inheritable, standards-compliant primitive. Storage becomes a commodity we route to. Soul is the product.

## Action items before D13 (Soul MVP build)

1. **Resolve encryption model.** Read 0G whitepaper §4. Probe with an actual E2EE test. Decide: build on 0G, build on Arweave+USDC gateway, or build on our own.
2. **Resolve 0G token vs USDC.** Pick a storage path that lets the agent pay in USDC (directly or via thin wrapper).
3. **Find or build a memory layer.** If 0G-Memory is real and good, use it. If not, decide: do we build the memory abstraction ourselves, or do we partner with Mem0 / Letta / Zep for that layer?
4. **Map the ERC-8004 + 0G integration.** Does 0G's "RBAC" compose with ERC-8004 identity, or is it a parallel identity system we have to bridge?

---

*This document is a working draft. Mark sections `[UNVERIFIED]` for follow-up.*
