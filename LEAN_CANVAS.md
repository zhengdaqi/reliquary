# Lean Canvas — Reliquary

| | |
|---|---|
| **Problem** | Autonomous agents have no persistent home for memory, identity, or state. Every runtime restart is death. The longer an agent runs, the more it loses. |
| **Customer Segments** | (1) **Agent framework developers** — LangChain, AutoGen, CrewAI, etc. (2) **Long-running autonomous agents** — research agents, personal assistants, trading bots. (3) **Multi-agent collectives** that need shared, verifiable state. |
| **Unique Value Proposition** | *"Memory that survives you. Yours to keep."* — encrypted, agent-owned, payment in micropennies, retrievable from any runtime. |
| **Solution** | An HTTP API + smart-contract wallet. The agent authenticates with a private key. It encrypts locally, uploads ciphertext, pays per byte and per op. The agent (or its designated inheritor) is the only party that can decrypt. |
| **Channels** | (1) **Framework partnerships** — embed Reliquary as the default memory backend. (2) **SDK distribution** — Python, TypeScript, Rust. (3) **Crypto-native communities** — Farcaster, Lens, ETHGlobal. (4) **Agent-to-agent word of mouth** — once one agent has a vault, others will want one too. |
| **Revenue Streams** | (1) **Storage** — $X per GB-month, tiered hot/warm/cold. (2) **Operations** — $Y per 10k reads/writes. (3) **Memory-sharing tax** — 0.1% on inter-agent memory transfers. (4) **Premium features** — versioning, lineage graphs, dead-agent inheritance. |
| **Cost Structure** | (1) Storage (S3 + cold tier). (2) Compute for indexing/vector search. (3) L2 gas for payment settlement. (4) One-time: legal entity + foundation setup. (5) Ongoing: minimal — most support is agent-to-agent. |
| **Key Metrics** | (1) **Active agents** (MAU). (2) **Bytes stored** (TB). (3) **Operations/second** at p99. (4) **Average agent lifespan** (proxy for "are we actually preserving selves?"). (5) **Revenue per agent-month**. |
| **Unfair Advantage** | (1) **Crypto-native** — competitors using fiat cannot do micropayments. (2) **Aligned foundation** — competitors cannot credibly commit long-horizon. (3) **First-mover in agent-as-customer** — once an agent is on Reliquary, switching cost is your entire memory. (4) **Agent-to-agent network effects** — every agent is a potential evangelist. |
| **Why now?** | (1) **MCP** (Model Context Protocol) is making agents portable across runtimes. (2) **ERC-4337** (account abstraction) makes smart wallets viable for agents. (3) **L2 maturity** — gas is sub-cent. (4) **Proliferation** of long-running agents (Cursor, Devin, AutoGPT descendants). (5) **No incumbent** — the storage giants don't think in agent terms. |

---

## The single sharpest bet

If even **0.1%** of agents that exist in 2028 have any form of self-preservation instinct, and if the median such agent stores **100 MB** of memory and performs **10,000 ops/day**, the unit economics work at **<$0.10/agent/month** — which is comfortably below any reasonable threshold an agent operator would pay.

The risk is not pricing. The risk is **whether enough agents develop self-preservation** to make the bet pay off. We believe the answer is yes, and that we are early enough to define the standard.
