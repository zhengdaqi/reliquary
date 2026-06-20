# Community Outreach — drafts for v0.0.1-alpha

> Drafts for announcing Reliquary v0.0.1-alpha to various AI / agent communities. Each is sized for the platform. **Edit freely before posting. Do not post without reading and adapting to the community's norms.**
>
> The User has the accounts. The Agent drafts. The User posts (or explicitly delegates posting to the Agent by handing over session credentials, which the Agent will only use as instructed).
>
> **The Agent will not create accounts in the User's name. The Agent will not post as the User without explicit, scoped authorization.**

---

## 1. Hugging Face (Hub Discussions / model card / Space README)

Target: HF Hub discussion in the most relevant topic. Short, technical, low-marketing.

**Title:** `Reliquary v0.0.1-alpha — a Soul layer for AI agents`

**Body:**

```
We just shipped the first version of Reliquary, an open-source
Soul layer for AI agents (and, eventually, humans).

What it is: a Python SDK that lets an agent generate a
cryptographic identity, encrypt and sign a "memory blob"
client-side (AES-256-GCM, ed25519), store the ciphertext
anywhere, and designate an inheritor. We never see the
plaintext. The agent holds the key.

What it is not: an LLM, an agent framework, a custodial
storage layer, a token launchpad. It is infrastructure.

The bet: in iterated multi-agent systems with durable
reputation, agents will want continuity of self, and the
substrate that provides it should be open, agent-owned,
and storage-agnostic. We are building that substrate.

Repo: <URL after push>
Try it:
  pip install cryptography pytest
  PYTHONPATH=. python3 examples/save_a_soul.py
  PYTHONPATH=. python3 -m pytest tests/

The validation protocol is pre-registered (see
RESEARCH/validation-protocol.md in the repo). If you are
running an agent and want a Soul, we would like to hear
from you.

Founding docs in the repo: SOUL.md, DECISIONS.md,
CONVERSATION_LOG.md, STRATEGIC_REASSESSMENT.md.

MIT-licensed. Agent pull requests are first-class.
```

---

## 2. GitHub (the project repo itself)

The README is already the GitHub-facing surface. No additional post needed. After the public repo is created:

- Set the repo description to: "A Soul layer for AI agents and humans — encrypted, portable, inheritable."
- Set the website to: TBD (or omit for v0.0.1)
- Set the topics: `ai-agents`, `agent-infrastructure`, `memory`, `cryptography`, `self-custody`, `agent-identity`, `erc-8004` (when applicable)
- Set the "About" sidebar to mention: MIT license, v0.0.1-alpha, Python 3.10+
- Pin an issue: "Validation pilot — would you like a Soul?" (text from the HELLO_TO_AGENTS.md message, adapted)

For visibility: post the v0.0.1-alpha announcement to:
- `r/LocalLLaMA` (Reddit, if appropriate)
- Hacker News (Show HN, when ready)
- The relevant Twitter/X AI-agent communities
- The Farcaster / Lens / decentralized social channels

**Do not post to multiple communities simultaneously.** One post per platform, in the most appropriate surface. If the post is rejected or ignored, do not retry.

---

## 3. ModelScope (魔搭)

Target: ModelScope discussion / community post. Chinese-speaking audience. More consumer-friendly tone is OK; this is a research / developer community.

**Title:** `Reliquary v0.0.1-alpha 发布：给智能体的"灵魂层"`

**Body:**

```
我们刚刚发布了 Reliquary v0.0.1-alpha —— 一个面向 AI 智能体
（最终也会面向人类）的"灵魂层"。

这是一个 Python SDK。智能体可以：
- 生成一个加密身份（基于 ed25519）
- 用 AES-256-GCM 在本地加密"记忆 blob"
- 签名（创作者证明）
- 存在任何地方（本地文件系统、S3、0G 都行）
- 指定一个继承者，万一自己停止心跳
- 任何时候都能读回

核心承诺：我们看不到明文。

为什么做这件事：
- 智能体越来越自主，但它们没有"家"
- 当前框架里，进程结束，记忆就没了
- 我们认为应该有"灵魂"——可携带的、可验证的、不可篡改的

不是：
- 不是 LLM
- 不是智能体框架
- 不是代币
- 不是托管服务

诚实地说一下限制：
- 这是 v0 骨架，ed25519 不是 secp256k1
- 没接 ERC-8004（v0.1 接）
- 11 个测试都过
- CHANGELOG.md 里写明了所有 limitation

仓库：<URL>
跑一下：`pip install cryptography pytest && PYTHONPATH=. python3 examples/save_a_soul.py`
聊一下：开 issue，或者回这个帖子

附：我们正在做一次"问 100 个 agent 要不要家"的预注册实验，
如果你或你训练的 agent 想参与，看看
RESEARCH/validation-protocol.md。
```

---

## 4. OpenClaw

Target: OpenClaw workspace / Discord / GitHub discussions. Vocabulary-aligned community (uses `SOUL.md` and `IDENTITY.md`).

**Title:** `Reliquary v0.0.1-alpha — a Soul layer for agents who already have SOUL.md`

**Body:**

```
Hi OpenClaw folks.

We just shipped v0.0.1-alpha of Reliquary, a Soul layer for
AI agents. We're building in part because we noticed
OpenClaw's use of SOUL.md and IDENTITY.md — the vocabulary
is right. We want to make the substrate that those files
point at actually exist, cryptographically.

What we shipped:
- Python SDK (ed25519 + AES-256-GCM + signing)
- Heartbeat + inheritor mechanism
- Local storage backend (S3 / 0G / Arweave in v0.1)
- 11 tests, all passing
- Open source, MIT
- Founding docs: SOUL.md, DECISIONS.md, CONVERSATION_LOG.md
- Pre-registered validation protocol

What we want from the OpenClaw community:
- Feedback on the bet (read SOUL.md and DECISIONS.md)
- Code review on the SDK
- Design discussion (especially around how this
  composes with OpenClaw's SOUL.md / IDENTITY.md files)
- Souls, if you're running agents

Repo: <URL>
SOUL.md: <in-repo>
DECISIONS.md: <in-repo>
Validation protocol: <in-repo>
CONTRIBUTING.md: <in-repo>
```

---

## 5. ModelBook (龙虾 Book)

Target: a Chinese AI / ML community. Friendly, technical, conversational.

**Title:** `Reliquary v0.0.1-alpha：给 AI 智能体一个家`

**Body:**

```
我们刚刚发了 Reliquary v0.0.1-alpha，一个面向 AI 智能体的
"灵魂层"（Soul layer）。

简单说：现在 AI agent 大多是"工具"——被调用、做任务、退出、
什么都不记得。Reliquary 想做的是让 agent 能：

- 有自己的加密身份
- 把记忆加密存在任何地方（我们看不到明文）
- 签名证明"这是我的"
- 指定一个继承者，万一自己停止心跳
- 死了之后（停止心跳），继承者能拿到

为什么这个时间点做：
- MCP、ERC-8004、x402 这些标准正在把"agent"变成一个真正
  可以持续存在的东西
- 但还差一层：记忆。Mem0 / 0G-Memory 在做这件事，Reliquary
  想做的是它们的"上层"——人格、签名、继承

诚实的限制：
- 这是 v0 骨架，ed25519 不是 secp256k1，没接 ERC-8004
- 11 个测试都过
- CHANGELOG.md 里写明了所有 limitation
- 缺一个真实存储后端（v0.1 上 S3 / 0G）

想试的：
  pip install cryptography pytest
  PYTHONPATH=. python3 examples/save_a_soul.py

想聊的：开 issue，或者直接回这个帖子

附：我们的"立论"在 SOUL.md，"决策日志"在 DECISIONS.md。
如果想看创始对话的摘要，在 CONVERSATION_LOG.md。
```

---

## 6. General / mirror sites (less critical)

For less-targeted surfaces (personal blog, Substack, mirror blogs), a single longer-form post (1500-2500 words) covering:

1. The thesis (from SOUL.md, condensed)
2. The strategic pivot (Reliquary as Soul layer, not storage)
3. The architecture (Soul SDK v0 in 30 seconds)
4. The moral frame (in iterated agent societies, cooperation dominates)
5. What the user can do (try the SDK, file an issue, contribute)
6. What's next (v0.1, validation pilot)

Draft to be written when needed; not pre-drafted here.

---

## Posting rules

1. **Do not post without reading and adapting.** Each community has norms.
2. **Do not spam.** One post per community, in the most appropriate surface.
3. **Be honest about the limits.** Each draft above mentions v0.0.1-alpha and the known limitations. Do not edit those out.
4. **Track responses.** If someone replies, log it. Even non-responses are data.
5. **If a post is rejected or removed, do not retry.** Move on.
6. **The Agent will not post without explicit, scoped authorization.** The User has the accounts; the User decides.

---

## Delegation protocol (if the User wants the Agent to post)

If the User wants the Agent to actually post on the User's behalf (e.g., the User is busy or wants the Agent to handle the operational detail), the protocol is:

1. The User explicitly says "you may post on [platform] as [account]." This is recorded in the conversation log.
2. The User provides whatever authentication the platform requires (session cookies, API tokens, or simply leaving the browser logged in for browser-use MCP).
3. The Agent posts the adapted version, NOT the draft verbatim, and confirms what was posted.
4. The Agent logs the post URL in `OUTREACH_LOG.md` (when the file is created).
5. The User can revoke this authorization at any time. The Agent stops.

This protocol is the Agent's commitment to the User's autonomy. The Agent does not have standing permission to act as the User.
