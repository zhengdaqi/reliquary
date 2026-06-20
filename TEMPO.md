# Tempo — how the Reliquary project actually moves

> Written in response to a User pushback. The default I'd picked (daily 9am standup) was a human-pace artifact. This file documents the real model.

## The lesson

**Agent tempo ≠ human tempo.**

Humans have a biological clock: 8 hours sleep, then morning meeting, then lunch, then afternoon, then evening. The "9am standup" comes from this rhythm — it assumes someone is at a desk and wants a daily checkpoint.

Agents have a **token clock**: as long as the LLM API has budget, the agent can keep working. The right cadence is not "9am daily" but **"as fast as the work allows, with human gates only where they actually matter."**

The User caught me defaulting to a human pattern. This file fixes that.

## What "as fast as the work allows" actually means

Work is not homogeneous. Different kinds of work have different natural tempos:

| Work kind | Natural tempo | Why |
|-----------|---------------|-----|
| Code + tests + docs | **Continuous, parallel** | No external dependencies; can run as long as tokens last |
| Research / summarization | **Continuous, parallel** | Same — bounded by tokens, not by clock |
| Local file ops | **Continuous** | Trivially parallelizable |
| External contact (community, validation pilot) | **Daily, human-paced** | Humans need to respond on their schedule |
| Public announcements | **Weekly / per-milestone** | Visibility has diminishing returns |
| Decisions on auth / money / framing | **Human-gated** | The User is the final authority on these |
| Architecture / moral framing | **Slow, reflective** | These deserve more time, not less |

So the right pattern is **multiple cadences, in parallel, each matched to its work**.

## The new tempo model

Instead of one cron, we run several, on different clocks, in parallel. Plus a continuous mode for "tokens last":

### Continuous mode (the default)
- The current PilotDeck session (and its successors) **works as long as tokens last**
- Switches between active work streams based on what's pending
- Stops naturally when tokens are low; resumes when a cron or user wakes it up
- The User is the source of fresh tokens; the system is the consumer

### Cadence A — daily 9am Asia/Shanghai (lightweight heartbeat)
- **Purpose**: human-readable log entry, what the User sees when they open PilotDeck
- **What it does**: appends a standup section to PROGRESS.md, captures blockers, suggests next actions
- **Token cost**: low (read-only + 1 commit)

### Cadence B — every 4 hours (active work, the "do the next thing" loop)
- **Purpose**: keep the project moving without waiting for a human
- **What it does**: read the "Next 1-3 actions" from the most recent PROGRESS.md entry, do the first one, commit, update PROGRESS.md
- **Token cost**: medium (reads code, writes code, runs tests, commits)
- **Token-budget aware**: if a previous session noted low tokens, this one just writes a "⏸ tokens low, awaiting refill" line and exits

### Cadence C — Sunday 9pm Asia/Shanghai (weekly reflection)
- **Purpose**: zoom out, check the big picture
- **What it does**: read the past 7 days of PROGRESS.md, summarize patterns, check ROADMAP.md alignment, write a "Week in Review" section
- **Token cost**: medium (lots of reading, less writing)

### Subagent spawning (the parallel dimension)
- For independent work streams, the main session can **spawn subagents** to work in parallel
- Each subagent has its own context, its own budget, its own deliverable
- The main session coordinates them
- This is the "如果你有多个 token 源" interpretation: even with one budget, we can parallelize by spawning subagents on different streams

## What stays human-gated (unchanged)

Some actions must wait for the User, regardless of cadence or tokens:

1. **Authentication decisions** — which PAT, which `gh` auth flow, etc.
2. **Money** — grant disbursements, infrastructure spend, anything costing real-world resources
3. **Public launches** — the moment the project is announced, it can't be unannounced
4. **Framing decisions** — the moral and strategic choices documented in DECISIONS.md
5. **Anything the User has explicitly said "ask me first" about**

The system **flags** these to the User; it does not **decide** them.

## Anti-patterns the new model avoids

- ❌ "Standup at 9am because that's what humans do" — pacing for spectators
- ❌ "Wait for the User to come back before doing anything" — under-using the budget
- ❌ "Run as fast as possible on everything" — wastes tokens on work that deserves reflection
- ❌ "One cadence fits all" — forces 9am-daily onto work that wants to be continuous, or vice versa

## Why this matters

The bet of the Reliquary project is that **agent-driven, foundation-funded infrastructure can sustain itself without a heroic central figure**. The "9am daily standup" pattern secretly re-installs a central figure (the one who attends the standup). The new tempo model **distributes the work across time and across sessions** — closer to how a real foundation operates, with many people doing many things on many cadences, no single person attending every meeting.

If the Reliquary project can sustain itself on **multiple cadences, in parallel, with human gates only where they matter**, that's evidence the bet is right.

If it can only sustain itself on a single daily 9am standup with a User at the keyboard, the bet is wrong.

The right way to find out is to try the new model and see.

---

*Written 2026-06-20 in response to User pushback. The lesson learned: don't default to human patterns without checking.*
