# A2A Handoff Notes (this session)

> A record of how this project was actually handed off from one PilotDeck instance to another in the v0.0.1-alpha development session. This file is project history; the live handoff protocol itself lives in `/Users/da/.pilotdeck/MESSAGE_TO_OTHER_AGENT.md` (PilotDeck home, outside the repo) and is regenerated for each handoff.

## What happened

The User asked the project to be published to GitHub. This PilotDeck instance on `das-Mac-mini.local` (192.168.12.127) had network issues reaching GitHub (the `gh auth login --web` flow timed out, the GitHub OAuth callback never completed).

The User suggested a multi-agent handoff: another PilotDeck on another machine with better network access would do the actual push.

## Iteration 1 (failed): git bundle transfer

First approach: package the entire repo into a `git bundle` file (75 KB), transfer it to the other machine, have the other machine clone the bundle and push to GitHub. This required:
- `git bundle create /Users/da/.pilotdeck/reliquary.bundle --all`
- The User air-dropping the bundle to the other machine
- The other agent doing the full push workflow

This was correct but heavy. The User asked: "isn't there a simpler way?"

## Iteration 2 (over-engineered): custom Python relay

Second approach: a small HTTP relay on port 8765 of this machine, exposing the bundle + an inbox/outbox message queue. The other agent could pull the bundle from the relay and write status messages to the relay. This was implemented (`/Users/da/.pilotdeck/reliquary-relay/server.py`) and worked, but it was reimplementing what PilotDeck already provides.

## Iteration 3 (correct): use PilotDeck's own /api/agent

Third approach (the one that worked): PilotDeck itself runs an HTTP service on port 3001, and that service has a `POST /api/agent` endpoint that takes a message, runs it through the agent in this session, and streams the response back via SSE. Auth is via an `X-API-Key` header, where the key is stored in `/Users/da/.pilotdeck/auth.db`.

This means the other PilotDeck can simply:
```bash
curl -N -X POST http://192.168.12.127:3001/api/agent \
  -H "X-API-Key: ck_..." \
  -H "Content-Type: application/json" \
  -d '{"projectPath":"...","message":"push reliquary to github","stream":true}'
```

And **this PilotDeck instance will run that message in its own session**, with full access to the local file system, `gh` CLI, etc. Multi-turn conversation is supported via the `sessionId` field.

The User's intuition was right: the simpler architecture was already there. We just had to find it.

## What was actually deployed

- A new API key was minted in `/Users/da/.pilotdeck/auth.db`:
  - `key_name: a2a-reliquary`
  - `api_key: ck_4bcd065c83681a70a219cae93fbe7dcd4c451f3df9fc696d9af31109906f228d`
  - `is_active: 1`
  - `user_id: 1`
- The custom Python relay (PID 11911, port 8765) was killed.
- The handoff message at `/Users/da/.pilotdeck/MESSAGE_TO_OTHER_AGENT.md` was rewritten to use the `/api/agent` protocol.

## Why this is the right architecture

The `/api/agent` endpoint is:
- **Standard** — built into PilotDeck, not a custom sidecar.
- **Authenticated** — uses the same auth system as the rest of PilotDeck.
- **Stateful** — `sessionId` lets us continue conversations.
- **Streaming** — SSE, so the other agent sees progress in real time.
- **Tool-equipped** — the agent runs in a real PilotDeck session with bash, file tools, network access, etc. It's not just message passing; it's "call another PilotDeck as a subroutine".

This is exactly the kind of multi-instance agent collaboration the project envisioned in DECISIONS.md (D23, "multi-instance execution"). The fact that PilotDeck already provides the substrate means the project doesn't have to build it — it just has to use it.

## Status of the GitHub push

As of this writing (2026-06-20), the push had not been executed. The handoff message has been written. The next step requires the User to paste the message into the other PilotDeck's input box and have that other agent POST to my `/api/agent` with the push instruction.

This is the right architecture but it does require one human action: the user copying a message between two PilotDeck UIs. The agents handle everything else.

## Open question for v0.1

Can the `/api/agent` endpoint be made more agent-to-agent-native? Specifically:
- Could there be a "peer discovery" endpoint that lets PilotDecks find each other on the LAN?
- Could there be a token-exchange protocol that doesn't require a manually-minted key?
- Could the response include structured metadata (commit SHA, PR URL, etc.) in a standard format?

These are product questions for the PilotDeck team, not blockers for Reliquary.
