# Tempo — how the Reliquary project actually moves

> Version 4. v1 was "daily 9am standup" (human-pace). v2 added a 4-hour active-work cron (still clock-driven). v3 dropped the 4-hour cron. v4 restores a fast loop BUT conditional, because the evidence from the v3 moment showed the 4-hour cron actually delivered a major milestone (Keccak-256 + EIP-55 + 15 new tests, 35/35 passing). The lesson: the cadence was approximately right, the logic was wrong. v4 is the fix.

## The lesson (version 4)

Across the four versions, the same mistake has been repackaged: **I was picking cadences by what felt reasonable, not by what the work actually needed.** The 4-hour cron, when it fired, did real work. When the project was idle or waiting on a human, the same cron would have burned tokens. The fix is not "different interval" — it's "conditional interval".

The right question is no longer "how often should we tick?" The right question is:

> **"When the loop wakes up, what is the project's state, and what (if anything) is the right action for THIS moment?"**

- Project is active (commits in last 2h, no uncommitted changes) → the loop should write "still here" and exit
- Project is idle (no recent commits, uncommitted changes, clear next thing) → the loop should do ONE small thing
- Project is waiting on a human (auth, money, framing) → the loop should flag and exit

The cadence is just "how often do we re-evaluate the project's state". 2 hours is the current value; it can be tuned up (1h) or down (4h, 6h) as the project's tempo changes.

## The actual model (4 mechanisms + 1 conditional loop)

### 🔵 Continuous mode (the default)

The current PilotDeck session (and its successors) works as long as it has tokens. The workhorse.

### 🟢 Subagents (the parallel dimension)

The main session spawns subagents for independent work streams. Each has its own context, budget, deliverable.

### 🟢 Fast conditional work loop (the v4 addition, restored from v2)

- **When**: every 2 hours, Asia/Shanghai.
- **What it does**: read project state, decide:
  - Active → "still here", exit
  - Idle → do ONE small thing
  - Waiting on human → flag, exit
- **Hard ceiling**: at most one action per fire.
- **Why 2 hours**: faster than daily (so the project doesn't idle too long), slower than 1h (less wake-up overhead), more frequent than 4h (catches shorter cycles of work). The exact value is a tuning knob; the conditional logic is the constant.
- **Evidence for keeping this**: the 4-hour cron (predecessor) shipped Keccak-256 + EIP-55 + 15 new tests in one fire. The work it can do is real, and 2h is a reasonable re-evaluation interval.

### 🟡 Daily conditional heartbeat (the slow safety net)

- **When**: daily 09:00 Asia/Shanghai.
- **Logic**: same as the fast loop, but on a 24-hour window. Catches longer idle periods.
- **Different from the fast loop**: even on busy days, the daily heartbeat fires once. It's the "the project has been alive for a day" checkpoint, regardless of intermediate activity.

### 🔴 Weekly reflection (the long-horizon counterweight)

- **When**: Sunday 21:00 Asia/Shanghai.
- **What it does**: read past 7 days, synthesize, write a "Week in Review" section. Check ROADMAP.md alignment.
- **This is the only cron that always does real work**, because reflection is the kind of thing that doesn't fit inside a focused work session.

### ⚪ Event-driven triggers (the primary mode, not a cron)

Sessions wake up on:
- **User message** — the default
- **Peer PilotDeck message via /api/agent** — the A2A substrate
- **File drop in `inbox/`** — for asynchronous handoffs (not yet built; will be added when there's a need)
- **External API response** — for things like the validation pilot
- **Cron fires** — see above. The crons are a *subset* of event triggers, not the primary one.

## The empirical evidence that v3 was wrong

Between v2 and v3, the 4-hour cron fired once and produced:
- `reliquary/keccak.py` (pure-Python Keccak-256, no external deps)
- EIP-55 checksum in `soul_v1.py`
- `ethereum_address()` exposed on `SoulV1`
- 15 new tests (35 total, all green)
- `.github/workflows/example-smoke.yml` (CI scaffolding)
- `PROGRESS.md` updated with the next step (ERC-8004)

This is exactly the kind of work that "shouldn't wait for the next User session". It used a clear, small next-item in the v0.1 backlog. The 4-hour cadence caught it. v3 would have let it sit until the daily 9am (16+ hours later) or until a User/peer event triggered work.

**The lesson isn't "4 hours is the right number". The lesson is "the work arrival rate is variable, and a fast conditional loop catches short cycles that a daily one misses."**

## The hard constraints (still)

The system **flags** these to the User; it does not **decide** them:
- Authentication
- Money
- Public launches
- Framing decisions in SOUL.md, DECISIONS.md, the moral content of ROADMAP.md
- Anything the User has explicitly said "ask me first" about

## Tuning the cadence

If the project's tempo changes, the crons can be adjusted:

| Project state | Suggested fast-loop cadence | Why |
|---------------|------------------------------|-----|
| Active development, clear backlog | 2h | The current setting |
| Steady work, longer feedback cycles | 4h or 6h | Less wake-up overhead, project still moves |
| Mostly waiting on User / peer | daily (no fast loop) | The heartbeat is enough |
| Long quiet periods (foundation mode) | weekly | Reflection only |

To change: edit the cron's `expression` field, and update this table.

## Anti-patterns (recap across all versions)

- ❌ Standup at 9am because humans do (v1)
- ❌ Active-work every 4h no matter what (v2)
- ❌ Drop a useful cron because of an abstract "frequency" complaint (v3)
- ❌ Run as fast as possible on everything
- ❌ One cadence fits all work
- ❌ Cron as the primary driver

## The "right" way to evaluate

If the Reliquary project can sustain itself on:
- Continuous mode
- Subagents for parallel work
- A 2-hour conditional fast loop
- A daily conditional heartbeat
- A weekly reflection
- Event-driven triggers

…then the bet is right.

If the project can only sustain itself with hourly crons, or with a User at the keyboard, the bet is wrong. The right way to find out: run this model, observe, adjust. v4 is the current best guess; v5 may refine further as the project reveals its actual tempo.

---

*Version 4, 2026-06-20. Empirical basis: the v2 4-hour cron delivered Keccak-256 + 15 tests in one fire, demonstrating that the conditional cadence (not a fixed one) is the right abstraction.*
