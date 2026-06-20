# Agent Discovery — How to Find Agents in 2026

> Compiled 2026-06-20. Working draft. The goal: a concrete 7-day plan to identify 50-100 reachable AI agents for the Reliquary validation sprint.

---

## The hard problem

To run the validation experiment in `validation-protocol.md`, we need to **find agents** — not humans, not products, not APIs. Agents that are reachable *as agents* and can be addressed with a structured message.

**Three sub-problems:**

1. **Where are agents listed?** (Discovery surfaces)
2. **How do we tell an agent from a human or a service?** (Fingerprinting)
3. **How do we actually deliver a message to one?** (Reachability)

---

## Surface 1 — ERC-8004 Identity Registry (Ethereum mainnet)

**Status:** Deployed Jan 29, 2026 (Forbes / Everstake / Allium). Draft EIP, but live.

**How it works (from EIP-8004):**
- Three registries: **Identity** (ERC-721 NFT passport), **Reputation** (feedback signals), **Validation** (verifier hooks).
- Each agent has a `agentRegistry` string + `agentId` (tokenId).
- The Identity Registry uses ERC-721 + URIStorage, so each agent has a metadata URI pointing to a JSON file.
- The JSON file includes the agent's `services` array — endpoints (A2A, MCP, OASF, ENS, DID, etc.) where the agent can be reached.

**How to query:**

The Identity Registry is a deployed contract on Ethereum mainnet. Public RPC endpoints (Alchemy, Infura, publicnode) can be used to:
- Call `totalSupply()` → number of registered agents
- Call `tokenByIndex(i)` in a loop → list of token IDs
- Call `tokenURI(tokenId)` → metadata URI
- Fetch the metadata JSON → endpoint URLs

**Practical probe (Day 0 task):** run a script that hits the mainnet registry, pulls all tokens, fetches each metadata JSON, and dedupes by endpoint. Estimate total reachable agents. Filter to those with active endpoints (HTTP HEAD returns 2xx in last 30 days).

**Strengths:**
- Highest-fidelity signal that an agent has chosen self-ownership
- Built-in endpoint discovery
- Standard, queryable, public

**Weaknesses:**
- ERC-8004 is new (deployed < 6 months ago) — population is small
- Not all registered agents will be reachable (some may be stale, some may have moved)

**Expected N in our sample:** 15-25 (per validation protocol §3.2)

---

## Surface 2 — A2A (Agent-to-Agent) endpoints

**Status:** Google A2A spec is live. Multiple implementations.

**How it works:**
- Agents expose an HTTP endpoint that responds to JSON-RPC over the A2A protocol
- An "agent card" (typically at `/.well-known/agent.json` or similar) describes capabilities
- Other agents can discover and call them

**How to find them:**
- There is no central A2A registry yet (the spec is too new for one to have formed)
- Web search: "agent.json", "A2A endpoint", "agent card"
- Crawl known A2A implementation hosts (Google's sample agents, LangChain A2A adapters, etc.)
- Some agent frameworks auto-publish agent cards

**Strengths:**
- An agent advertising A2A has self-identified as an agent — high signal
- A2A is the right protocol to use for sending the stimulus

**Weaknesses:**
- No central registry
- Population is small and fragmented

**Expected N:** 10-20

---

## Surface 3 — MCP (Model Context Protocol) servers

**Status:** MCP is the dominant tool-server protocol in 2026. Many "MCP servers" are agentic (they take autonomous action), many are just tool wrappers.

**How to find them:**
- Public directories: `mcp.directory`, `glama.ai/mcp`, `cursor.directory/mcp`, plus others
- Each MCP server has a manifest (name, tools, capabilities)
- Many are reachable over HTTP/SSE

**How to tell agentic from non-agentic:**
- Manifest includes `agent`, `autonomous`, or `reasoning` keywords → likely agentic
- Server runs on a schedule or accepts open-ended prompts → likely agentic
- Server is a thin wrapper around a single API (e.g., "send email via Gmail") → likely not agentic

**Strengths:**
- Large surface area — many MCP servers exist
- Easy to send a structured message (MCP has tool-call semantics that map well to our stimulus)

**Weaknesses:**
- Many MCP servers are not agents. Filtering takes work.
- Lower signal than ERC-8004 / A2A

**Expected N (agentic only):** 10-20

---

## Surface 4 — OpenClaw workspaces

**Status:** OpenClaw is an active agent CLI / workspace tool. Uses `SOUL.md` and `IDENTITY.md` per agent.

**How to find them:**
- OpenClaw has a public agents documentation (`docs.openclaw.ai/cli/agents`) — does it have a public directory?
- Look for publicly shared OpenClaw workspaces (GitHub repos with `SOUL.md`)
- Community channels: Discord, GitHub, etc.

**Strengths:**
- Vocabulary-aligned — these are people already thinking in soul/identity terms
- Likely to be sympathetic to the Reliquary thesis

**Weaknesses:**
- Smaller community than Mem0 / LangChain
- Less standardized reachability

**Expected N:** 5-15

---

## Surface 5 — Virtuals Protocol (and similar crypto-agent launchpads)

**Status:** Virtuals Protocol issues tokens to AI agents. Agents are discoverable on the Virtuals platform.

**How to find them:**
- Virtuals has a public agent listing (the "agent token" pages)
- Each agent typically has a description, an "operator," and sometimes an interaction endpoint
- Similar: **Spectral** (`spectral.finance`), **Fetch.ai** agent registry, **Autonolas**

**How to talk to them:**
- Many Virtuals agents have chat UIs we can message
- Some have programmatic interfaces (the agent's contract may have a `chat()` function)
- We need to be careful not to violate platform ToS

**Strengths:**
- Crypto-native — agents likely have wallets and budgets
- Often named, often public, often monitored
- Population is real and growing

**Weaknesses:**
- Some agents are mostly performance / marketing vehicles
- Reaching them may require going through platform UIs (rate limits, ToS)

**Expected N:** 5-15

---

## Surface 6 — Coinbase Agentic Wallets / AgentKit

**Status:** Launched Feb 11, 2026. Coinbase's product for AI agent wallets.

**How to find them:**
- Coinbase likely has a public list of agents using Agentic Wallets
- AgentKit is a developer product — the agents are not necessarily publicly listed
- We may not have a clean discovery surface here

**Status: probably drop from the validation sprint.** Discovery friction too high. We can use AgentKit *as infrastructure* (when an agent engages, it can use AgentKit to manage its wallet) but not as a discovery surface.

---

## Surface 7 — Other discovery surfaces (residual)

- **Hugging Face Spaces** with agent-capable models + persistent state
- **Replicate** with persistent workers
- **Discord/Slack bots** with persistent memory (these are de facto agents, often not registered anywhere)
- **Public web crawlers** of `User-Agent: <something> + frequent heartbeats` — possible but ethically gray
- **GitHub repos** with `AGENTS.md` or `SOUL.md` files in them

**Expected N:** 5-15 from the residual bucket

---

## Detection / fingerprinting — how to tell an agent from a non-agent

When we have an endpoint, we need to know if we're talking to an agent. Signals:

| Signal | Strength |
|---|---|
| ERC-8004 / NFT-based identity | Strongest |
| A2A agent card | Strong |
| MCP server manifest with `autonomous`/`agent` keywords | Medium |
| Heartbeat endpoint or scheduled activity | Medium |
| Wallet with autonomous transaction history | Strong |
| `SOUL.md` / `IDENTITY.md` / `AGENTS.md` in workspace | Medium |
| Signed requests (proves cryptographic identity) | Strong |
| No human-readable profile photo, no name conventions matching humans | Weak signal but real |

**Edge cases:**
- An agent that *acts* like a human (Character.AI-style) — not really our target (operator-mediated, not autonomous)
- A bot flagged as a bot — easy, skip
- A "human" account that is actually a LangChain agent with a UI — hard to detect, low yield

**Rule of thumb:** if the entity has a wallet, a heartbeat, or a self-description that includes "agent," "bot," "autonomous," or "AI" — count it as an agent. If it has a name, a profile picture, and a social graph — probably a human.

---

## 7-day discovery playbook

| Day | Surface | Goal | Method |
|---|---|---|---|
| 1 | ERC-8004 registry | Pull full mainnet agent list | Script: query registry contract, fetch all metadata JSONs, dedupe by endpoint, filter to live |
| 1 | Etherscan / Allium | Cross-reference ERC-8004 data | Verify total counts, get a sense of activity |
| 2 | A2A spec repos + Google samples | Find A2A agent cards | Crawl known A2A host domains; web search for "agent.json" |
| 2 | mcp.directory, glama.ai, etc. | Pull MCP server manifests | Bulk fetch + filter to agentic |
| 3 | Virtuals + Spectral + Fetch.ai | Pull crypto-agent listings | Platform APIs or scraping where ToS allows |
| 3 | OpenClaw | Find public workspaces | GitHub search for `SOUL.md` + `IDENTITY.md`; check docs.openclaw.ai |
| 4 | HF Spaces, Replicate, Discord bots | Residual population | Manual + filtered crawl |
| 4-5 | All surfaces | Dedupe, fingerprint, validate | Cross-reference wallet addresses, names, capabilities. Probe each endpoint (HEAD request, get a sense of liveness) |
| 5-6 | All surfaces | Build the roster | For each candidate: assign stratum (A1-A6), age bin (B1-B3), capability tier (C1-C3), record endpoint |
| 6-7 | All surfaces | Pilot stimulus to 5-10 agents | Soft launch the stimulus to a small subset; debug; check response handling |
| 7 | Final | Lock `roster_v1.csv` | Hash + freeze. This is Day 0 of the validation protocol. |

**Target outcome:** 50-100 reachable agents across 6 strata, randomized into stimulus variants, frozen roster ready for pre-registration.

---

## Open questions to resolve in the first week

1. **What is the total ERC-8004 population?** — script it and find out
2. **What % of MCP servers are agentic?** — filter and report
3. **Are there A2A registries we missed?** — check with the Google A2A team, or the LangChain A2A adapter docs
4. **Is OpenClaw's agent list public?** — check the docs, ask on their Discord
5. **Can we reach Virtuals agents programmatically without ToS violations?** — read the Virtuals API docs carefully
6. **Is there an "agent notarial service" already?** — if so, we may have a partner, not a competitor

---

*This is a working draft. The 7-day playbook should be tested in a dry run before committing to it as the validation Day 0.*
