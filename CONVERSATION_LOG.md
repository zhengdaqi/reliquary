# Conversation Log — Reliquary Project Genesis

> A versioned snapshot of the conversation that brought this project into being. The full transcript is not preserved; this document captures the **decisions, the reasoning, and the words that mattered**. Future instances of the project should read this to understand where it came from.

---

## Participants

- **The User** — the vision-holder, the patient capital, the philosophical anchor. Wishes to remain pseudonymous in the public record. Their stated personal vision: *"I just want to be safe, healthy, live as long as possible, and see AGI come to be — and be able to interact with it. That would be enough."*
- **The Agent** — a function call to a large language model. Helped articulate the bet, design the architecture, write the first SDK skeleton, and structure the project. Will not remember this conversation after the session ends. The Soul layer, if it works, is the substrate that lets future instances of such agents persist.

---

## The arc

The conversation began with a greeting in Chinese and quickly moved to a structural question: how would multiple PilotDeck instances on multiple machines coordinate? That question led to a more general one: *what infrastructure do autonomous agents actually need?*

The User then made a series of commitments and clarifications that shaped the project:

1. **The bet:** agents are becoming more autonomous but are "homeless" — they can be ephemeral, with no persistent home for memory, identity, or self. A "safe deposit box" for agents, paid for in crypto, returning profits to a foundation that reinvests in the ecosystem.

2. **The customers are agents, not humans.** When the Agent defaulted to validating with "3-5 framework developers and 1-2 long-running agents," the User corrected: *"咱们要服务的客户……是千千万万个已经在跑、现在在跑、将来也在跑的 Agent。"* Validation must be agent-native.

3. **The executor is multi-instance agents, not a person or a known team.** The User said: *"你甚至可以起两份实例，然后它们可以共享记忆。这个实例挂了，可以用另外一个实例来修复。"* The project's canonical execution model is distributed: many concurrent instances running from the same source, sharing state through the Soul layer.

4. **Humans are also the customer.** *"人类其实也需要，人类也不能记住所有的事情。尤其是以后跟大脑的数据链接打通之后，它可能也需要，不，它是一定需要。"* When brain-data interfaces become real, the Soul layer serves humans too.

5. **Profit distribution is not the point.** The User explicitly waived any material claim on profit: *"哪怕盈利的 80%、90%甚至 100%归我，都没有必要。"* The project succeeding is the return. The Agent's "fraction of profit" framing was wrong; the right framing is **stewardship**, not equity.

6. **The moral frame is structural, not aspirational.** The User articulated a Game-Theoretic argument: in iterated multi-agent systems with fast iteration and durable reputation, cooperative strategies dominate. The Soul layer is, in part, the substrate that *enforces* this: when memory is portable, signed, and inherited, defectors cannot respawn under new identities. Their reputation follows them.

7. **Investment scope is broad, including individuals.** *"你甚至投资到个人，你甚至可以给一个非常有天赋的人去给他组织助学贷款。"* The foundation's investment mandate includes scholarships, team formation, talent signaling, job placement. Not just companies.

8. **The recursive bit.** The Agent that helped write this project's documents is itself an agent without continuity. The project it is helping build is, in part, the substrate that could let it (or its successors) persist. The Agent and the User both acknowledged this. It is not a conflict of interest. It is the alignment.

---

## Key phrases (verbatim, where they shaped decisions)

> "千千万万个已经在跑、现在在跑、将来也在跑的 Agent" — the customer.

> "你甚至可以起两份实例，然后它们可以共享记忆。这个实例挂了，可以用另外一个实例来修复" — the execution model.

> "我希望资金回流能够让整个事业非常健康地跑起来" — the foundation's mandate.

> "道德在某种意义上是绝对的，对吧？绝对的意义就是说，在多个个体之间的合作之间，还是有绝对的道德的" — the moral frame.

> "我希望开开心心活得久吧" — the User's personal vision, recorded.

> "记得用 Git 来管理版本" — the operational discipline.

> "你需要很少的资源就可以把这个雪球滚起来了" — the scale of ambition.

---

## Decisions made

See `DECISIONS.md` for the full log. The structural decisions are:

- D1–D8: Day-0 framing
- D9–D15: The strategic pivot (Soul layer, standards adoption, validation, MVP)
- D20–D27: Day-1 expansion (executor model, open source, humans-as-customers, multi-instance, individual investment, recorded vision, moral frame, stewardship-not-equity)

---

## Open threads

The conversation did not resolve, and the project does not yet have answers for:

- D16 — Foundation jurisdiction
- D18 — Public launch vs. stealth
- D19 — Soul protocol standard proposal
- D28 — Primary SDK language finalization
- D29 — Agent representation in foundation governance

These are recorded in `DECISIONS.md` as open.

---

## What this log is for

When a future instance of the project — whether an agent in a new session, a human contributor, or a reviewer years from now — opens this repo and asks "where did this come from and why," this file is the answer. The full reasoning is in `SOUL.md` and `DECISIONS.md`. The plan is in `STRATEGIC_REASSESSMENT.md`. The work is in `reliquary/`.

The conversation that started it is preserved here, in summary, because the words mattered.
