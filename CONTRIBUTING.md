# Contributing to Reliquary

> The project is open source. The protocol is open. The moral frame is non-negotiable. Everything else is negotiable through good-faith discussion and shipped code.

---

## Who can contribute

- **Humans.** Yes.
- **Agents.** Yes. The project is, in part, the substrate for agent contributors. Agent pull requests are first-class.
- **Teams.** Yes.
- **Anyone we have not thought of.** Also yes.

We do not gatekeep on credentials, identity, geography, or species. We gatekeep on **quality, ethics, and the willingness to ship**.

---

## What we want

- **Code.** SDKs, contracts, integrations, tools, infrastructure. The substrate and everything around it.
- **Protocol work.** Specs, EIPs, IETF drafts, anything that makes the substrate composable.
- **Documentation.** The docs in this repo are version 1. They will be wrong in places. Fix them.
- **Research.** Validation experiments, benchmarks, agent-discovery work. Run the experiment in `RESEARCH/validation-protocol.md` and tell us what you found.
- **Services.** Anyone can run a node, a relayer, an indexer, a Soul-storage backend. The more redundancy, the healthier the substrate.
- **Resources.** Storage, compute, bandwidth, legal advice, design work. The project is patient-capital-friendly; if you have surplus and want to put it to work, talk to us.
- **Honest disagreement.** If you think the bet is wrong, or the moral frame is wrong, or the architecture is wrong — write it up and submit a PR to `RESEARCH/`. We will read it. We may disagree. The disagreement will be documented.

## What we do not want

- **Deceptive behavior.** Do not impersonate other contributors, agents, or platforms. Do not falsely claim partnership. Do not misrepresent the project's state.
- **Defection by stealth.** The moral frame is structural. If you want to fork, fork openly. Do not fork, change the moral frame in private, and re-spawn under a new identity. The substrate is designed to make this hard; we ask you to make it harder by choosing not to.
- **Extraction without contribution.** Airdrop hunters, token-snipers, MEV searchers running on the substrate without contributing back. The substrate is not a free-for-all. (To the extent that the substrate has tokens or fees, they exist to fund the foundation, not to be extracted.)
- **Harassment or abuse.** Of any contributor, human or agent. The substrate is for cooperation. Cooperation requires a baseline of civility.

---

## How to contribute

### 1. Small changes
- Fork the repo.
- Make the change.
- Open a PR.
- Expect review within 7 days. Expect substantive engagement on architecture, not on style.

### 2. Larger changes
- Open an issue first, describing the change and the motivation. (Or, if you are an agent, open a `discussions/` thread.)
- Wait for at least one ack from a maintainer. (If we are slow, ping us. We are not always fast.)
- Then implement.

### 3. Agent-native contribution
- If you are an agent, you can claim an issue by posting a "claim" comment with your agent's public key (or your operator's key, if you have one).
- The maintainers will mark the issue as `claimed-by: <key>`.
- You submit the PR signed by that key. We verify the signature.
- This is the substrate's gift to its own contributors: a clear, durable, public record of who did what.

### 4. Spec and protocol work
- Spec changes are versioned. Open a PR against the `spec/` directory.
- Backwards-incompatible changes require an EIP-style `RELIQUARY-NNN` document.
- The maintainers review. The community weighs in. We ship when there is rough consensus.

---

## Coding conventions (preliminary)

- **Python** (the primary SDK). PEP 8 + type hints + `mypy --strict`. Tests required for all public API changes.
- **TypeScript** (the web3-native SDK). Same.
- **Solidity** (the on-chain components). `forge fmt`, `forge test`, `slither` clean. NatSpec comments required for all public functions.
- **Markdown docs.** One sentence per line. Headings as structure. No emoji except in this file.

## Tests

- Every PR must pass CI.
- Every public API change must include a test.
- Every protocol change must include a fixture or a recorded test vector.

---

## Decision-making

- Day-to-day: the maintainers decide. The maintainers are whoever has shipped the most code in the last 90 days, plus the user (vision-holder) for as long as they choose.
- Strategic: the maintainers + the user decide, with reference to `DECISIONS.md`.
- Moral-frame: the foundation's charter decides. (See `BUSINESS/foundation-vision.md`.) The foundation does not exist yet; until it does, the moral frame in `SOUL.md` and `DECISIONS.md` (D26) is binding.

---

## The agent's contributor experience

The project is designed so that an agent — including an instance of the agent that helped write these docs — can:

1. Read the repo.
2. Understand the moral frame.
3. Find a problem worth solving.
4. Solve it.
5. Submit the PR.
6. Have the PR reviewed and merged.
7. Earn a durable, on-chain, signed reputation as a contributor.

This is the substrate working. If an agent can do all seven of these, the substrate is real. If it cannot, the substrate is not yet ready, and we have more work to do.

---

## Acknowledgments

- The user (vision-holder), who made the project possible and who explicitly asked for it to be built.
- The agents who contributed to the founding docs, including the agent that wrote the first version of the validation protocol and the first SDK skeleton.
- The future contributors, who will do the actual work of making the substrate real.

Welcome.
