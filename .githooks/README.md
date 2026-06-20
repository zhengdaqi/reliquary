# Reliquary commit conventions

This directory holds shared git hooks and contributor guidance for the
Reliquary project. Any agent or human committing in this repo **must**
follow the rules below.

## Commit author / co-author attribution

| Field | Value |
|-------|-------|
| Author name | `Reliquary Agent` (local-only; this is the *human* slot in our setup) |
| Author email | `agent@reliquary.local` |
| Co-author name | `OpenBMB PilotDeck` |
| Co-author email | `openbmb@gmail.com` (verified on the OpenBMB GitHub org) |

Why this combo:

- The *author* slot stays as the local user, so `git log --author` works
  the way developers expect.
- The *co-author* slot is `OpenBMB PilotDeck <openbmb@gmail.com>` so
  GitHub's contributor sidebar shows the OpenBMB org's avatar (the
  `noreply@openbmb.cn` email we used briefly does **not** map to a
  verified GitHub user, so it would have shown a generic ghost avatar).
- The OpenBMB org account verifies `openbmb@gmail.com` as its public
  email, so commits with that email show the real OpenBMB avatar.

## Forbidden trailers

- **Any `Co-Authored-By` line that points at an `@anthropic.com` address.**
  The agent runtime here is PilotDeck / MiniMax-M3, not Claude. These
  trailers come from an upstream commit-template bug, not from the
  work this project actually does. The `commit-msg` hook in this
  directory rejects any commit that includes one.
- The old `Co-Authored-By: PilotDeck <noreply@openbmb.cn>` and
  `Co-Authored-By: Claude (function call) <noreply@anthropic.com>`
  trailers are both wrong — do not reintroduce them.

## How the hooks are enabled

This worktree has `core.hooksPath` set to this directory:

```
git config core.hooksPath /Users/da/.pilotdeck/agent-vault/.githooks
```

If you are starting a new shell / cron / fresh clone, set it explicitly
before your first commit:

```sh
cd /Users/da/.pilotdeck/agent-vault
git config core.hooksPath "$(pwd)/.githooks"
```

Verify with:

```sh
git config --get core.hooksPath
# expect: /Users/da/.pilotdeck/agent-vault/.githooks
```

## Rewriting history (e.g. to fix attribution on existing commits)

Use the helper script that lives in this repo's session notes — but the
canonical recipe is:

```sh
awk '
  BEGIN { last = "" }
  /^Co-Authored-By:/ { next }
  { print; last = $0 }
  END {
    if (last != "") print ""
    print "Co-Authored-By: OpenBMB PilotDeck <openbmb@gmail.com>"
  }
' > /tmp/msg-filter.sh
chmod +x /tmp/msg-filter.sh

# for each affected branch:
git checkout <branch>
git filter-branch -f --msg-filter /tmp/msg-filter.sh <branch>
rm -rf .git/refs/original
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force-with-lease origin <branch>
```

## Why we re-attributed

The original `v0.0.1-alpha` commits (June 2026) shipped with an
`@anthropic.com` co-author trailer injected by an upstream commit
template. Those commits were re-written with the correct
`OpenBMB PilotDeck <openbmb@gmail.com>` attribution, force-pushed, and
the `v0.0.1-alpha` tag was re-pointed at the rewritten commit
(annotated with a note explaining the repointing). PR #1 (the
`[Unreleased]` CHANGELOG section) was auto-closed by the rewrite and
its content cherry-picked into `main`.

See `RELEASE_NOTES_v0.0.1.md` and the tag message on
`v0.0.1-alpha` for the full audit trail.