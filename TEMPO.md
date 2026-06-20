# Tempo — how the Reliquary project actually moves

> Version 5. v1 was "daily 9am standup" (human-pace). v2 added a 4-hour active-work cron (still clock-driven). v3 dropped the 4-hour cron. v4 made it conditional but still put the cron in the work-driver role. v5 makes the cron an "alive check" only — the session is the workhorse.

## The lesson (version 5)

Across the four previous versions, I kept making the same mistake: **I made the crons the work driver.** I designed the 2-hour / 4-hour / daily loops to "do the next thing" — which implicitly said "the session isn't doing the work, the cron is."

The User caught this three times in a row:

> "4 hours really necessary? How did you decide? Think for yourself."

> "Does the agent not actively do something in the 2 hours between cron fires? Such good time, efficient tokens just being wasted."

The right model is finally:

- **The session is the workhorse.** When this PilotDeck instance is alive, it works continuously. It picks the next thing, does it, commits, picks the next. No clock needed.
- **Subagents are the parallel dimension.** The session can spawn N independent streams. They run in parallel, each on its own context.
- **Crons are the SAFETY NET.** They exist for the case when no session is running — the User closed PilotDeck, the previous session ended, no event triggered work. The cron's only job is: "Is the project alive? If yes, log and exit. If no, nudge it with ONE small thing so it doesn't go fully dormant."

The 2-hour cadence is not "do work every 2 hours." It is "**check liveness every 2 hours**." Most of the time the cron will fire, see recent activity, and exit. Only when the project has been idle for >24h does the cron do anything.

This is the right division of labor. The session gets all the time it needs. The cron only intervenes when the session is gone.

## The actual model (3 layers + 1 safety net)

### 🔵 Session = workhorse

The current PilotDeck session (and its successors) works as long as it has tokens. It:
- Reads `PROGRESS.md` to find the "Next 1-3 actions"
- Picks the first unfinished action
- Does it: writes code, runs tests, commits
- Updates `PROGRESS.md` with what it did
- Loops back

The session can also spawn subagents for parallel work. There is **no clock** on this work. The session works as fast as it can, for as long as it has tokens, until it runs out of work or the User says stop.

### 🟢 Subagents = parallel dimension

The session can spawn subagents for independent work streams. Each has its own context, its own budget, its own deliverable. The session coordinates.

This is the primary way to use multiple "token sources" in parallel. Subagents are not driven by a clock; they are spawned when the session notices an opportunity to parallelize.

### ⚪ Alive-check cron = safety net (v5)

- **When**: every 2 hours, Asia/Shanghai.
- **What it does**: check if the project is alive.
  - **A. Alive** (commits in last 24h, OR uncommitted changes, OR PROGRESS.md updated in last 12h): write "still here" and exit. Do NOT do work.
  - **B. Dormant** (no commits in 24h, no uncommitted changes, PROGRESS.md last update >24h old): do ONE small thing. Hard ceiling: one action.
  - **C. Waiting on User**: flag, exit.
- **Cost**: most fires are <30 seconds and a 1-line log. Expensive fires only happen when the project has been truly idle.
- **Why 2 hours**: it's the "re-evaluation interval" for "is the session still alive?". If the session is dead, we want to know within 2 hours, not 24.

### 🔴 Weekly reflection = long-horizon check

- **When**: Sunday 21:00 Asia/Shanghai.
- **What it does**: read past 7 days, synthesize, write a "Week in Review" section. Check ROADMAP.md alignment.
- **This is the only cron that always does real work**, because reflection is the kind of thing that doesn't fit inside a focused work session. The session could do it manually, but it's a different mode (zoomed-out, synthetic) and benefits from a dedicated slot.

## The empirical basis for v5

Between v2 and v3, the 4-hour cron shipped Keccak-256 + EIP-55 + 15 new tests. That was the right outcome but the wrong cause: the cron was doing work BECAUSE no session was running. If a session HAD been running, the cron would have been wasted overhead.

The right framing: the cron is not the workhorse. The cron is the thing that ran the work in the absence of a session. We can keep the cron as a safety net (so the project doesn't go fully dormant when the User is away), but it shouldn't pretend to be the workhorse.

When the session is alive, the session works. When the session is dead, the cron nudges. The 2-hour cadence is the "how often do we check if the session is dead" interval, not a work schedule.

## The hard constraints (still)

The system **flags** these to the User; it does not **decide** them:
- Authentication
- Money
- Public launches
- Framing decisions in SOUL.md, DECISIONS.md, the moral content of ROADMAP.md
- Anything the User has explicitly said "ask me first" about

## Anti-patterns (recap across all versions)

- ❌ Standup at 9am because humans do (v1)
- ❌ Active-work every 4h no matter what (v2)
- ❌ Drop a useful cron because of an abstract "frequency" complaint (v3)
- ❌ Make the cron a work driver (v4)
- ❌ Make the cron pretend to be the session (v5's anti-pattern)
- ❌ Run as fast as possible on everything
- ❌ One cadence fits all work
- ❌ Cron as the primary driver

## The "right" way to evaluate

If the Reliquary project can sustain itself on:
- A live session (the workhorse)
- Subagents for parallel work
- A 2-hour alive-check safety net
- A weekly reflection
- Event-driven triggers (User messages, peer messages via /api/agent, future inbox/ drops)

…then the bet is right.

If the project can only sustain itself with crons doing the work, the bet is wrong — because that pattern re-installs the crons as the central scheduler, which is just a different shape of "a person at a desk ticking boxes every N hours".

The right way to find out: run this model, observe, adjust. v5 is the current best guess; v6 may refine further as the project reveals its actual tempo. The big variable is **the session's discipline** — does it actually work continuously, or does it sit idle waiting for a User or a cron? If it sits idle, no cron can fix that; only the session being alive and active can.

---

*Version 5, 2026-06-20. The structural shift: the session is the workhorse, the cron is the safety net. The 2-hour cadence is "re-evaluation of liveness", not "work schedule". The session is now expected to work continuously, in parallel with subagents, while the cron just keeps an eye on things.*
