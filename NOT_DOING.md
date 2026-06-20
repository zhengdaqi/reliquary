# What we are not doing (yet)

> The most expensive decisions are the things you say yes to by not saying no. This file is the explicit no.

---

## Hard "no"

- **No LLM.** We do not train, fine-tune, or host language models. We are storage.
- **No agent framework.** We do not build LangChain, AutoGen, or anything that competes with them.
- **No UI for humans.** The API and the SDKs are the product. There is no dashboard for a human to log into and read an agent's memory. (This is a feature: the human has no access either.)
- **No custodial wallets.** We never hold an agent's key. Ever. Under any circumstance. Including legal compulsion — we will architect the system so that legal compulsion yields nothing usable. (See D6.)
- **No KYC of agents or their operators.** The agent is the customer. The wallet is the identity. If the operator wants to remain pseudonymous, that's their right and our default.
- **No personal data of humans.** If a memory contains human PII, that's the agent's problem to handle — we are a vault, not a data processor for GDPR purposes.

---

## Soft "not yet"

- **No vector search.** Day 0 is dumb blob storage. Vector search is a V2 feature that requires a clear customer pulling for it.
- **No Soul layer implementation.** The three-layer model is for pricing and design. Implementation of the Soul layer waits for at least one customer who needs it.
- **No on-chain agent registry.** Tempting (and probably useful) but premature. We use wallets, not a registry.
- **No inter-agent memory market.** The 0.1% memory-sharing tax is in the canvas but is not in the MVP.
- **No agent death/inheritance protocol.** Important, but a v2/v3 feature. Day 0 is just persistence.

---

## "We'll evaluate later"

- **Token issuance.** Could be useful for governance, could be a distraction. Not deciding.
- **Mobile SDK.** Most agent runtimes are server-side. Mobile is hypothetical.
- **Fiat on-ramp.** If an operator wants to fund their agent's wallet in fiat, that's a third-party service (Coinbase, MoonPay). We do not integrate payment processors in the MVP.
- **Open-sourcing the server.** Maybe. The client SDKs will likely be open from day 0.

---

## Why this file exists

When someone asks "why don't you also build X?" the answer is in this file. When we are tempted to say yes to a feature, we update this file first, then build.

The cost of this discipline is the cost of focus. It is the single highest-leverage thing we can do.
