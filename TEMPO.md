# Tempo — how the Reliquary project actually moves

> The third draft. The first was "daily 9am standup" (human-pace default). The second was "continuous + three crons including a 4-hour active-work loop" (still a clock-driven default). This is the third: **event-driven primarily, with one conditional heartbeat and one weekly reflection as safety nets.**

## The lesson (version 3)

The first two drafts both had the same flaw: I was picking cadences by **clock**, not by **work**. 9am, 4 hours, daily, weekly — these are all clock numbers. They feel reasonable but they have no relationship to what the project actually needs.

The right question is not "how often should we tick?" The right questions are:

1. **When is there work to do?** Triggered by events: a new message, a peer PilotDeck contact, a file drop, a test failure, a User decision.
2. **What is the marginal value of a wake-up?** If the project is active (a live session is working), waking it up is pure overhead. If the project is idle (no commits in 24h, no events), a wake-up might do one small thing.
3. **What is the marginal cost of a wake-up?** New session = context-loading overhead + minimum token spend. If the session can only do 1 small thing, this overhead is most of the cost.
4. **How many wake-ups does the User want to see?** The User said the 9am daily was arbitrary. They want fewer noise events, more signal.

From these: **clock-driven crons are mostly wrong. Event-driven is mostly right. A single conditional daily heartbeat is the right safety net. A weekly reflection is the right long-horizon counterweight.**

## The actual model (4 mechanisms, mostly event-driven)

### 🔵 Continuous mode (the default)

The current PilotDeck session (and its successors) works as long as it has tokens. It picks the next concrete action from PROGRESS.md and does it. It stops naturally when:
- Tokens are low
- There's nothing in the "Next 1-3 actions" list that this session can do autonomously
- The User says stop

**This is the workhorse.** Most of the project's progress comes from here, not from crons.

### 🟢 Subagents (the parallel dimension)

The main session can spawn subagents for independent work streams. Each subagent has its own context, its own budget, its own deliverable. The main session coordinates.

**Examples of when to spawn a subagent:**
- "I need a doc written for the v0.1 SDK while I work on v0.1 code" → spawn a doc subagent
- "I want to research ERC-8004 in depth while continuing the secp256k1 work" → spawn a research subagent
- "I need to test something I don't want to pollute my context with" → spawn a test subagent

**The right rhythm is "when I notice the work can be parallelized"**, not "every N hours". If a subagent is running, it runs in parallel with the main session — that IS the parallelism. No clock required.

### 🟡 Daily conditional heartbeat (the safety net)

- **When**: every day at 09:00 Asia/Shanghai.
- **What it does FIRST**: check the project state.
  - If the project is active (commits in last 24h, no uncommitted changes): just write a 1-line "still here" entry. Exit in <30 seconds. No work.
  - If the project is idle (no commits in 24h, OR uncommitted changes exist): do exactly ONE small thing from the "Next 1-3 actions" list. Run tests. Commit. Exit.
- **Hard ceiling**: at most one concrete action per day. Even if the project has been idle for a week, the heartbeat does ONE thing, not seven days' worth of catch-up. The heartbeat is a nudge, not a backfill engine.
- **Why daily, not 4-hourly**: 4 hours = 6 wake-ups/day, mostly redundant with continuous mode and noisy. Daily = 1 wake-up/day, and it's conditional so it does nothing on busy days. The cost drops 6×, the value stays.

### 🔴 Weekly reflection (the long-horizon counterweight)

- **When**: Sunday 21:00 Asia/Shanghai.
- **What it does**: read the past 7 days of PROGRESS.md, synthesize, write a "Week in Review" section. Check if ROADMAP.md is still aligned with reality. If not, update it.
- **Why weekly**: shorter than a week, you can't see patterns. Longer than a week, drift accumulates. A week is the natural reflection unit for a project at this pace.
- **This is the only cron that always does real work**, because reflection is exactly the kind of thing that doesn't fit inside a focused work session.

### ⚪ Event-driven triggers (the primary mode, not a cron)

Sessions wake up on:
- **User message** — the default. PilotDeck receives a message, a session is created or resumed.
- **Peer PilotDeck message via /api/agent** — the A2A substrate. We already have one peer; more may come.
- **File drop in `inbox/`** — for asynchronous handoffs. (Not yet built; will be added when there's a need.)
- **External API response** — for things like the validation pilot (peer contact results come back asynchronously).
- **Cron fires** — see above. The crons are a *subset* of event triggers, not the primary one.

## What was wrong with the 4-hour cron

| Symptom | Why it was wrong |
|---------|------------------|
| Triggered every 4h no matter what | Clock-driven, not event-driven |
| 6 wake-ups per day | Burned startup overhead on days when continuous mode was already moving |
| Always did "the next thing" | If continuous mode is alive, the next thing is already being done |
| No idle detection | Wasted wake-ups when project was waiting on the User |

## What stays human-gated (unchanged from version 2)

1. **Authentication** — which PAT, which `gh` auth flow
2. **Money** — grant disbursements, infrastructure spend
3. **Public launches** — the moment a project is announced, it can't be unannounced
4. **Framing decisions** — SOUL.md, DECISIONS.md, and the moral content of ROADMAP.md
5. **Anything the User has explicitly said "ask me first" about**

The system **flags** these to the User; it does not **decide** them.

## Anti-patterns the new model avoids

- ❌ "Standup at 9am because that's what humans do" — version 1's mistake
- ❌ "Active work loop every 4 hours because progress should be frequent" — version 2's mistake
- ❌ "Run as fast as possible on everything" — wastes tokens on work that deserves reflection
- ❌ "One cadence fits all work" — forces a clock onto work that wants events
- ❌ "Cron as the primary driver" — crons are a safety net, not the engine

## The "right" way to evaluate this

If the Reliquary project can sustain itself on:
- Continuous mode (the main session)
- Subagents for parallel work
- One daily conditional heartbeat
- One weekly reflection
- Event-driven triggers for things outside these

…then the bet is right. The project can sustain itself without a heroic central figure.

If it can only sustain itself with a 4-hour cron (or hourly, or "every N minutes"), the bet is wrong — because that pattern re-installs a clock-driven central scheduler, which is just a different shape of "a person at a desk".

The right way to find out: run this model, observe, adjust.

---

*Version 3, 2026-06-20. Previous versions: clock-driven 9am daily (v1), continuous + 3-cron mix (v2). This version is event-driven with conditional safety nets.*
