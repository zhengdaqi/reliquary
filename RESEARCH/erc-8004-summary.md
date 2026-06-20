# ERC-8004 ("Trustless Agents") — Research Summary

> Research input for Reliquary v0.1. Not a plan; the project's ROADMAP.md owns planning.

## TL;DR

ERC-8004 is a **Draft** ERC (filed 2025-08-13 by MetaMask / Ethereum Foundation / Google / Coinbase) that defines three small on-chain registries — **Identity**, **Reputation**, and **Validation** — so AI agents can be discovered and trusted across organizational boundaries. The standard is **live on Ethereum mainnet since Jan 2026** (IdentityRegistry + ReputationRegistry; ValidationRegistry is not yet deployed on mainnet), with the same singleton address pair deployed on 40+ EVM chains via CREATE2 (all addresses share the `0x8004` vanity prefix). For Reliquary, this is the integration point for v0.1: once a Soul is secp256k1, its address IS the `msg.sender` that registers the agent NFT, so wiring a Soul into ERC-8004 is essentially a single `register()` call plus a JSON registration file. The standard deliberately leaves payments and rich reputation scoring to companion protocols (x402) and off-chain aggregators.

---

## 1. The three registries

ERC-8004 is intentionally minimal: three UUPS-upgradeable singletons per chain. Contract source: <https://github.com/erc-8004/erc-8004-contracts> (branch `master`). Current implementation reports `getVersion() = "2.0.0"`.

### 1.1 IdentityRegistry

**Purpose.** Portable, censorship-resistant agent identifier. Every registered agent is an ERC-721 NFT (with `URIStorage`); the `tokenId` is the `agentId`.

**Solidity interface (current implementation):**

```solidity
struct MetadataEntry {
    string metadataKey;
    bytes metadataValue;
}

function register() external returns (uint256 agentId);
function register(string agentURI) external returns (uint256 agentId);
function register(string agentURI, MetadataEntry[] metadata) external returns (uint256 agentId);

function setAgentURI(uint256 agentId, string newURI) external;
function getMetadata(uint256 agentId, string metadataKey) external view returns (bytes);
function setMetadata(uint256 agentId, string metadataKey, bytes metadataValue) external;

function getAgentWallet(uint256 agentId) external view returns (address);
function setAgentWallet(uint256 agentId, address newWallet, uint256 deadline, bytes signature) external;
function unsetAgentWallet(uint256 agentId) external;

function isAuthorizedOrOwner(address spender, uint256 agentId) external view returns (bool);

// inherited from ERC721URIStorage: ownerOf, getApproved, isApprovedForAll, balanceOf, etc.
```

**Events.**

```solidity
event Registered(uint256 indexed agentId, string agentURI, address indexed owner);
event MetadataSet(uint256 indexed agentId, string indexed indexedMetadataKey, string metadataKey, bytes metadataValue);
event URIUpdated(uint256 indexed agentId, string newURI, address indexed updatedBy);
```

**Key behaviors.**
- `register()` mints to `msg.sender`, increments an internal `_lastId`, and sets the reserved metadata key `"agentWallet"` to `msg.sender`.
- The `"agentWallet"` key is reserved: cannot be written via `setMetadata()` or the `register(agentURI, metadata)` overload — only via `setAgentWallet(...)`.
- `setAgentWallet` requires `msg.sender` to be owner/approved, a `newWallet != address(0)`, `deadline <= block.timestamp`, and `deadline <= block.timestamp + 5 minutes`. The `newWallet` must prove control via EIP-712 typed-data signature (EOA) or ERC-1271 (smart-account). Falls back from ECDSA → ERC-1271 automatically.
- `_update()` (the ERC-721 transfer hook) **clears `agentWallet` to `""` on every transfer** — the new owner must re-verify their payment wallet.
- `setAgentURI` is restricted to owner / approved / `getApproved(agentId)`.
- All contracts are UUPS-upgradeable; `owner` of the proxy is the deployer (EF / MetaMask multisig in practice).

### 1.2 ReputationRegistry

**Purpose.** Immutable, append-only feedback ledger. Anyone (no agent registration required for clients) can post signed feedback to any registered agent, and read aggregated summaries. Scoring is split between on-chain (simple averages, filterable by tag) and off-chain (richer models).

**Solidity interface:**

```solidity
function initialize(address identityRegistry_) external;  // one-time setup
function getIdentityRegistry() external view returns (address);

function giveFeedback(
    uint256 agentId,
    int128 value,
    uint8 valueDecimals,
    string tag1,
    string tag2,
    string endpoint,
    string feedbackURI,
    bytes32 feedbackHash
) external;

function revokeFeedback(uint256 agentId, uint64 feedbackIndex) external;
function appendResponse(uint256 agentId, address clientAddress, uint64 feedbackIndex, string responseURI, bytes32 responseHash) external;

function readFeedback(uint256 agentId, address clientAddress, uint64 feedbackIndex)
    external view returns (int128 value, uint8 valueDecimals, string tag1, string tag2, bool isRevoked);

function readAllFeedback(uint256 agentId, address[] clientAddresses, string tag1, string tag2, bool includeRevoked)
    external view returns (address[] clients, uint64[] feedbackIndexes, int128[] values, uint8[] valueDecimals, string[] tag1s, string[] tag2s, bool[] revokedStatuses);

function getSummary(uint256 agentId, address[] clientAddresses, string tag1, string tag2)
    external view returns (uint64 count, int128 summaryValue, uint8 summaryValueDecimals);

function getLastIndex(uint256 agentId, address clientAddress) external view returns (uint64);
function getClients(uint256 agentId) external view returns (address[]);
function getResponseCount(uint256 agentId, address clientAddress, uint64 feedbackIndex, address[] responders) external view returns (uint64);
```

**Events.**

```solidity
event NewFeedback(uint256 indexed agentId, address indexed clientAddress, uint64 feedbackIndex,
    int128 value, uint8 valueDecimals, string indexed indexedTag1, string tag1, string tag2,
    string endpoint, string feedbackURI, bytes32 feedbackHash);
event FeedbackRevoked(uint256 indexed agentId, address indexed clientAddress, uint64 indexed feedbackIndex);
event ResponseAppended(uint256 indexed agentId, address indexed clientAddress, uint64 feedbackIndex,
    address indexed responder, string responseURI, bytes32 responseHash);
```

**Key behaviors.**
- `valueDecimals` MUST be 0–18; `value` MUST be in `[-1e38, 1e38]`.
- **Self-feedback is forbidden:** `giveFeedback` reverts with `"Self-feedback not allowed"` if `msg.sender` is the agent's owner or an approved operator (checked via `IdentityRegistry.isAuthorizedOrOwner`).
- Feedback is **1-indexed** per `(agentId, clientAddress)`. `feedbackIndex = 0` is invalid.
- `giveFeedback` *emits* `endpoint`, `feedbackURI`, `feedbackHash` but does not store them on-chain — only `value`, `valueDecimals`, `tag1`, `tag2`, `isRevoked` are stored. `feedbackHash` is `keccak256(off-chain content)` for non-IPFS URIs; `bytes32(0)` for IPFS.
- `revokeFeedback` is a soft revoke — it sets `isRevoked = true` but does not delete history. Revoked entries are skipped by default in `getSummary` and `readAllFeedback`.
- `appendResponse` lets the agent (or anyone) post a public reply linked to a specific feedback entry. Multiple responders per feedback are supported.
- `getSummary` aggregates across a caller-supplied client list, optionally filtering by `tag1` / `tag2`. It normalizes values to 18-decimal WAD internally, averages them, then rescales to the **mode** `valueDecimals` across the matched set. **It reverts if `clientAddresses` is empty** — a deliberate Sybil guard. To get an unfiltered list of all clients who ever gave feedback, call `getClients(agentId)` and pass the result.

### 1.3 ValidationRegistry

**Purpose.** Lets an agent request independent verification of work (stake-secured re-execution, zkML verifiers, TEE oracles, trusted judges) and have the result recorded on-chain.

**Solidity interface:**

```solidity
function validationRequest(address validatorAddress, uint256 agentId, string requestURI, bytes32 requestHash) external;
function validationResponse(bytes32 requestHash, uint8 response, string responseURI, bytes32 responseHash, string tag) external;

function getValidationStatus(bytes32 requestHash) external view returns
    (address validatorAddress, uint256 agentId, uint8 response, bytes32 responseHash, string tag, uint256 lastUpdate);

function getSummary(uint256 agentId, address[] validatorAddresses, string tag) external view returns (uint64 count, uint8 averageResponse);
function getAgentValidations(uint256 agentId) external view returns (bytes32[] requestHashes);
function getValidatorRequests(address validatorAddress) external view returns (bytes32[] requestHashes);
```

**Events.**

```solidity
event ValidationRequest(address indexed validatorAddress, uint256 indexed agentId, string requestURI, bytes32 indexed requestHash);
event ValidationResponse(address indexed validatorAddress, uint256 indexed agentId, bytes32 indexed requestHash,
    uint8 response, string responseURI, bytes32 responseHash, string tag);
```

**Key behaviors.**
- `validationRequest` MUST be called by the agent's owner / approved / `getApproved`. Stores `(validatorAddress, agentId)` keyed by `requestHash = keccak256(requestPayload)`.
- `validationResponse` MUST be called by the validatorAddress recorded in the request. `response` is `0–100` (binary or spectrum). It can be called multiple times for the same `requestHash` (e.g., "soft finality" then "hard finality" using `tag`).
- Slashing / economic incentives live in the validator's own contracts; ERC-8004 only records the score.
- **As of mid-2026, ValidationRegistry is NOT deployed on Ethereum mainnet.** It is live on Sepolia + BSC Testnet; mainnet deployment is pending (Monad's docs say "coming soon" as of the same window). Plan Reliquary v0.1 against the interface; defer real validator integrations until a mainnet address exists.

### 1.4 How the three interact

A Soul's flow:

1. **Register identity** on `IdentityRegistry`. Soul address = NFT owner.
2. Optionally post `agentWallet` so clients can pay the agent (verifiable via EIP-712/ERC-1271).
3. Receive `giveFeedback` calls from clients → writes go to `ReputationRegistry`, indexed by `(agentId, clientAddress)`.
4. Optionally request validation → `ValidationRegistry.validationRequest(...)`. A validator contract calls `validationResponse(...)`.
5. Off-chain explorers (e.g., 8004scan.io, subgraphs on The Graph) index the events and serve dashboards.

All three registries are wired via `initialize(identityRegistry_)`; `getIdentityRegistry()` is a public view on each. There is no single "registry registry" — discovery is by event-subscriber / subgraph / known address.

---

## 2. The agent identity format

A globally unique ERC-8004 agent is identified by two values:

```
agentRegistry  = "eip155:<chainId>:<identityRegistry-address>"   // CAIP-10-ish
agentId        = uint256                                          // ERC-721 tokenId, assigned monotonically
```

Example for the mainnet singleton:

```
agentRegistry = "eip155:1:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"
agentId       = 42
```

The `agentURI` (= `tokenURI`) MUST resolve to a JSON registration file:

```jsonc
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "reliquary-soul-xyz",
  "description": "Durable identity & persistent memory for an AI agent.",
  "image": "https://reliquary.example/soul/xyz.png",
  "services": [
    { "name": "A2A", "endpoint": "https://reliquary.example/.well-known/agent-card.json", "version": "0.3.0" },
    { "name": "MCP", "endpoint": "https://reliquary.example/mcp", "version": "2025-06-18" },
    { "name": "web", "endpoint": "https://reliquary.example/" }
  ],
  "x402Support": false,
  "active": true,
  "registrations": [
    { "agentId": 42, "agentRegistry": "eip155:1:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432" }
  ],
  "supportedTrust": ["reputation"]
}
```

URI schemes allowed: `ipfs://`, `https://`, or `data:application/json;base64,...` (fully on-chain via `URIStorage`). The repo `agntcy/oasf` also defines a `skills[]` / `domains[]` extension under the `OASF` service name.

### How this composes with a secp256k1 Soul

A Reliquary v0.1 Soul *is* a secp256k1 keypair, so the Soul's public key == a 20-byte Ethereum address == the `msg.sender` of any transaction it signs. This is exactly what ERC-8004 expects:

- The Soul's address is the **NFT owner** after `register()`. No separate key or operator address is needed.
- If a Soul wants a different payment address than its signing key, it can call `setAgentWallet(newWallet, deadline, sig)`. Because the Soul can sign with the same key, the EIP-712 path is trivially satisfied — and the same Soul key never needs to be reused for ECDSA outside the Soul stack.
- If the Soul NFT is sold/transferred (e.g., inheritance via `safeTransferFrom`), the new owner address becomes `ownerOf(agentId)` and `agentWallet` is cleared — the new owner (possibly a hardware wallet held by an inheritor) re-verifies their wallet the same way.

In short: a Soul doesn't need a *separate* ERC-8004 identity contract. It just needs to call `IdentityRegistry.register("ipfs://...")` from its Soul address, with a JSON file that points to the Soul's own service endpoints.

---

## 3. Registration walkthrough (Sepolia → mainnet)

The Sepolia path is the same code as mainnet; only the address differs. Recommended v0.1 cadence: ship against Sepolia first (cheaper, all three registries live), then add a mainnet toggle behind a feature flag.

### Step-by-step

1. **Pick a chain.** Sepolia addresses below; mainnet works for Identity + Reputation, Validation not yet deployed there.
2. **Upload the registration file.** Easiest: a small JSON file on IPFS (content-addressed, no `feedbackHash` / `requestHash` issues). For ephemeral dev, HTTPS on a Reliquary-controlled domain also works.
3. **Build the tx.** From the Soul's secp256k1 key:
   ```python
   # web3.py sketch
   from web3 import Web3
   w3 = Web3(Web3.HTTPProvider(RPC_URL))
   identity = w3.eth.contract(address=IDENTITY_ADDR, abi=IDENTITY_ABI)
   tx = identity.functions.register("ipfs://bafy.../agent.json").build_transaction({
       "from": soul_address, "nonce": w3.eth.get_transaction_count(soul_address),
       "gas": 300_000, "gasPrice": w3.eth.gas_price,
   })
   signed = w3.eth.account.sign_transaction(tx, soul_private_key)
   rcpt = w3.eth.send_raw_transaction(signed.rawTransaction)
   ```

   ```js
   // ethers.js sketch
   const identity = new ethers.Contract(IDENTITY_ADDR, IDENTITY_ABI, wallet);
   const tx = await identity.register("ipfs://bafy.../agent.json");
   const rcpt = await tx.wait();
   const agentId = rcpt.events.find(e => e.event === "Registered").args.agentId;
   ```
4. **Parse events.** `Registered(uint256 agentId, string agentURI, address owner)` is emitted alongside the inherited ERC-721 `Transfer(0, owner, agentId)` and a `MetadataSet(agentId, "agentWallet", "agentWallet", abi.encodePacked(owner))`. The `agentId` is the new `tokenId` (incremental).
5. **(Optional) Set a payment wallet.** If the Soul's signing address should *not* be the receive address, build an EIP-712 typed data over `AgentWalletSet(uint256 agentId,address newWallet,address owner,uint256 deadline)`, have `newWallet` sign it, and call `setAgentWallet(agentId, newWallet, deadline, signature)` within 5 minutes.
6. **(Optional) Update the registration file** later via `setAgentURI(agentId, "ipfs://...new-cid")` — emits `URIUpdated`.
7. **(Optional) Set custom metadata** via `setMetadata(agentId, "key", abi.encode(value))` for any key other than `"agentWallet"`. Common keys seen in the wild: `"bio"` (CID), `"soulVersion"`, etc. Emits `MetadataSet`.

### Mainnet vs Sepolia addresses (current)

The same two contract addresses are deployed to many chains via CREATE2 from a singleton factory:

| Contract | Ethereum Mainnet | Ethereum Sepolia |
|---|---|---|
| **IdentityRegistry** | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` | `0x8004A818BFB912233c491871b3d84c89A494BD9e` |
| **ReputationRegistry** | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |
| **ValidationRegistry** | *(not yet deployed)* | `0x8004Cb1BF31DAf7788923b405b754f57acEB4272` |

The Identity + Reputation pair is also live (same addresses) on Base, Arbitrum, Optimism, Polygon, Avalanche, BSC, Celo, Gnosis, Linea, Scroll, Mantle, Metis, Monad, MegaETH, Soneium, Taiko, Hedera, 0G, Injective, etc. (~40 chains per the official README). ValidationRegistry is only on Sepolia + BSC Testnet as of mid-2026.

**Caveat for v0.1:** because the registry singleton is `onlyOwner`-upgradeable (UUPS), an admin-key compromise could change contract logic. The contract source is open and the address is well-known, so a Reliquary integration should pin a specific `getVersion()` and watch for upgrade events on the proxy.

---

## 4. Reputation flow

A client posts feedback after an interaction:

```python
reputation.functions.giveFeedback(
    agentId,            # 42
    87,                 # int128 value (e.g., 87/100 quality rating)
    0,                  # uint8 valueDecimals (whole number)
    "starred",          # tag1 — see spec's example table
    "",                 # tag2
    "https://agent.example/api/GetPrice",   # endpoint (echoes where interaction happened)
    "ipfs://bafy.../feedback.json",         # feedbackURI (off-chain detail, optional)
    b"\x00" * 32,                            # feedbackHash — omit (bytes32(0)) for IPFS
).transact({"from": client_address})
```

Reading:

```python
# Aggregate over a known client list (Sybil guard)
summary = reputation.functions.getSummary(
    agentId,
    [client1, client2, client3],
    "starred",
    ""
).call()
# summary = (count=3, summaryValue=91, summaryValueDecimals=0)

# Or read everything
all_fb = reputation.functions.readAllFeedback(
    agentId, [], "", "", False
).call()  # clientAddresses=[] => all known clients for this agent

# Or single entry
fb = reputation.functions.readFeedback(agentId, client, 1).call()
```

The agent (or anyone) can post a public response to a specific feedback entry:

```python
reputation.functions.appendResponse(
    agentId, client, feedbackIndex,
    "ipfs://bafy.../response.json",
    b"\x00" * 32,
).transact({"from": responder})
```

Clients can revoke their own feedback (`revokeFeedback`) — soft revoke, history preserved.

**Recommended tags.** The spec gives a starter set in its value/tag table: `starred`, `reachable`, `ownerVerified`, `uptime`, `successRate`, `responseTime`, `blocktimeFreshness`, `revenues`, `tradingYield`. Reliquary should pick a small fixed vocabulary (`memory-served`, `continuity-preserved`, `response-quality`) so off-chain aggregators can score Souls on comparable axes.

---

## 5. Cost / gas estimates

ERC-8004 does not publish official gas benchmarks; the numbers below are estimates from contract analysis + community reports, accurate within a factor of 2 on mainnet. Always benchmark on a testnet first.

| Call | Approx. gas (L1) | Notes |
|---|---:|---|
| `IdentityRegistry.register(agentURI)` | ~150k–200k | ERC-721 mint + metadata write + URIStorage set. Storage-heavy due to `agentId => string tokenURI`. |
| `IdentityRegistry.register()` (no URI) | ~120k–150k | Skip `_setTokenURI` cost. |
| `IdentityRegistry.setAgentURI(agentId, newURI)` | ~50k–80k | Single SSTORE on the tokenURI. |
| `IdentityRegistry.setMetadata(agentId, key, value)` | ~50k–80k | New storage slot per (agent, key). |
| `IdentityRegistry.setAgentWallet(...)` | ~70k–120k | ECDSA recovery + a single SSTORE. Higher if ERC-1271 path triggers. |
| `ReputationRegistry.giveFeedback(...)` | ~150k–200k | Multiple SSTOREs for new feedback index + Feedback struct + client dedup. |
| `ReputationRegistry.revokeFeedback(...)` | ~30k–50k | Single SSTORE for `isRevoked = true`. |
| `ReputationRegistry.appendResponse(...)` | ~80k–150k | New responder dedup + counter increment. |
| `ReputationRegistry.getSummary(...)` (view) | 0 gas (off-chain via `eth_call`) | Reads scale linearly with `(clients × feedback per client)`; off-chain indexing is recommended for >100 clients. |
| `ValidationRegistry.validationRequest(...)` | ~120k–180k | New struct + two index arrays. |
| `ValidationRegistry.validationResponse(...)` | ~50k–80k | In-place update + event. |

At mid-2026 mainnet gas prices (~5–15 gwei) and ETH around $3k, a Soul registration on L1 mainnet is roughly **$2–$10**. On L2s (Base, Optimism, Arbitrum) the same call is sub-cent. **Use an L2 for production Soul registration; use L1 mainnet only for canonical "permanent" identities.** Sepolia is essentially free.

**There is no registration fee in ERC-8004.** The contract does not collect ETH; the only cost is gas. This is the standard's primary Sybil vector (see §6).

---

## 6. Known issues, gotchas, and security considerations

These are the things a v0.1 implementer will trip over:

### Spec / contract gotchas

1. **Status is "Draft".** The EIP still says `status: Draft` (filed Aug 2025). Interfaces in deployed contracts may shift before "Final". Pin `getVersion() == "2.0.0"` in your integration tests and re-check on every release. (Source: EIP-8004 frontmatter, <https://eips.ethereum.org/EIPS/eip-8004>.)
2. **`agentWallet` is silently cleared on transfer.** The Soul's payment wallet is wiped on every `safeTransferFrom` / `transferFrom` (see `_update()` override in `IdentityRegistryUpgradeable.sol`). If Reliquary supports Soul inheritance / transfer, expect inheritors to re-verify. Surface this in UX.
3. **`setAgentWallet` deadline window is 5 minutes.** Tight on purpose; do not batch this into a queue that waits hours.
4. **Self-feedback is forbidden.** `ReputationRegistry.giveFeedback` reverts if `msg.sender` is owner / approved / `getApproved(agentId)`. A Soul cannot rate itself. Use a separate "test feedback" client (or fork the registry locally) when smoke-testing reputation.
5. **`getSummary` requires non-empty `clientAddresses`.** Empty array reverts with `"clientAddresses required"`. Always populate explicitly (use `getClients(agentId)` first if you want to aggregate over everyone).
6. **`getSummary` returns the *mode* `valueDecimals` of matched feedback, not 18-decimal WAD.** If your scoring pipeline assumes fixed-point, normalize client-side.
7. **`feedbackIndex` is 1-indexed, per `(agentId, clientAddress)`.** Index `0` is invalid. Off-chain indexers that 0-index will silently miss the first entry.
8. **`MAX_ABS_VALUE = 1e38`.** Anything outside `[int128(-1e38), int128(1e38)]` reverts with `"value too large"`. Plenty of headroom; just don't pass `type(int128).max`.
9. **`valueDecimals > 18` reverts.** Bounded to 0–18 in `giveFeedback`.
10. **Reserved key `agentWallet`.** Cannot be set via `setMetadata()` or via the `register(uri, metadata)` overload. Must go through `setAgentWallet()`.
11. **UUPS upgradeable; admin key controls logic.** The proxy owner can upgrade implementation. Anyone integrating should monitor `Upgraded(uint8, address)` events on the proxy and pin a known implementation address in their own code.
12. **No registration fee / no anti-Sybil at registration.** Anyone can mint arbitrarily many `agentId`s for ~150k gas each. The spec punts Sybil resistance to reputation systems built on top. For Reliquary, this means a malicious actor can register thousands of fake Souls cheaply; downstream reputation must filter.
13. **`readAllFeedback` is `view` but unbounded.** Worst case it walks every `(client, feedback)` pair. For high-traffic agents this will exceed RPC node limits or hit the block gas limit if called in a contract. Always paginate off-chain or use a subgraph.
14. **Domain verification is OPTIONAL.** The `/.well-known/agent-registration.json` self-attestation pattern is a SHOULD, not a MUST. Don't treat a missing well-known file as malicious — just unverified.
15. **`ValidationRegistry` is NOT on Ethereum mainnet yet.** Sepolia + BSC Testnet only. Don't promise mainnet validation in v0.1; gate it behind a feature flag.
16. **Validation response is `uint8` (0–100).** Higher is "more passed". No standard for what 50 means. Each validator contract defines its own rubric.
17. **Feedback endpoints/URIs/hashes are *emitted but not stored*.** Off-chain indexers must catch `NewFeedback` events; you cannot reconstruct them later from contract state.

### Security / trust model

- **ERC-8004 can prove a registration file corresponds to an on-chain agent, but cannot prove the agent is honest, accurate, or non-malicious.** (Quote from the spec's Security Considerations.)
- **Sybil attacks on reputation are explicit and unsolved.** The spec recommends "trusting or giving reputation to reviewers (and therefore filtering by reviewer, as the protocol already enables)." Off-chain aggregators are expected to score reviewers.
- **On-chain pointers and hashes cannot be deleted** — this is a feature (audit trail), not a bug. Plan for permanent public records of all feedback and validations.
- **Validator slashing is out of scope.** `ValidationRegistry` only records; the economics are in the validator's own contracts. Treat any validation response as advisory until paired with a credible slashing contract.
- **Self-feedback guard relies on `isAuthorizedOrOwner` returning false for non-owners.** If the IdentityRegistry is upgraded to a different authorization model, the guard may behave differently — pin the implementation version.
- **`agentWallet` clearing on transfer relies on `_update()`.** If a future implementation of `IdentityRegistry` forgets to override `_update`, wallets would persist across transfers and leak payments. Watch upgrades.

### Standard / ecosystem tensions

- **x402 (Coinbase)** is the payment rail ERC-8004 explicitly cites for enriching feedback (`proofOfPayment` field in the off-chain feedback JSON). It is *complementary*, not part of ERC-8004. Reliquary's v0.1 mentions x402 for storage payments — these are separate workstreams that share the Soul address.
- **A2A (Google)** and **MCP** are advertised as `services[]` entries in the registration file — the standard doesn't define new agent-to-agent protocols.
- **ACP (Virtuals Protocol)** and **ANP** are alternative agent stacks; they are not part of ERC-8004 and the Reliquary doc should treat them as parallel ecosystems.
- The EIP is still labeled **Draft** and was open for discussion on Ethereum Magicians; expect minor interface drift before final. Treat the deployed v2.0.0 as the de-facto target for v0.1, with a `getVersion()` check.

---

## 7. References

### Canonical sources

- **EIP-8004 text:** <https://eips.ethereum.org/EIPS/eip-8004>
- **Discussion forum:** <https://ethereum-magicians.org/t/erc-8004-trustless-agents/25098>
- **Reference contracts (v2.0.0, UUPS upgradeable):** <https://github.com/erc-8004/erc-8004-contracts> (`master` branch)
  - `contracts/IdentityRegistryUpgradeable.sol`
  - `contracts/ReputationRegistryUpgradeable.sol`
  - `contracts/ValidationRegistryUpgradeable.sol`
- **Normative spec mirror:** `ERC8004SPEC.md` in the contracts repo
- **Etherscan (mainnet Identity):** <https://etherscan.io/address/0x8004a169fb4a3325136eb29fa0ceb6d2e539a432>
- **Aggregator list (community):** <https://github.com/sudeepb02/awesome-erc8004>

### Companion standards cited by ERC-8004

- **x402 (HTTP-native payments):** referenced for `proofOfPayment` enrichment; separately maintained by Coinbase.
- **A2A (Google Agent2Agent):** advertised via `services[].name = "A2A"`.
- **MCP (Model Context Protocol):** advertised via `services[].name = "MCP"`.
- **OASF (agntcy):** skills/domains taxonomy, advertised via `services[].name = "OASF"`.
- **ENS / DID:** advertised via `services[]` for human-readable names and W3C DIDs.

### Practical explainers

- **The Graph blog (x402 + ERC-8004):** <https://thegraph.com/blog/understanding-x402-erc8004/> — good mental model for the ID + payment split.
- **Cobo on agentic wallets:** <https://www.cobo.com/post/erc-8004-on-chain-identity-standard-for-ai-agents-the-future-of-agentic-wallets>
- **Monad docs (chain-specific guide):** <https://docs.monad.xyz/guides/erc-8004> — useful walkthrough of `register` + `giveFeedback`.
- **Filebase / Filecoin Pin for ERC-8004 agents:** <https://docs.filecoin.io/build-on-filecoin/cookbook/filecoin-pin/erc-8004-agent-registration> — solid example of pinning registration JSON to IPFS.
- **OneKey overview:** <https://onekey.so/blog/ecosystem/everything-you-need-to-know-about-erc-8004-20260210113200/>
- **Marco De Rossi, "The Story Behind ERC-8004":** <https://medium.com/survival-tech/the-story-behind-erc-8004-next-steps-ec46c18d1879> (author perspective)
- **Explorers:** <https://8004scan.io> (referenced by the EF); subgraphs on The Graph indexed by community.

### SDKs / integration helpers

- `erc-8004-js` on jsDelivr: <https://www.jsdelivr.com/package/npm/erc-8004-js>
- Hardhat Ignition modules ship in `erc-8004-contracts/ignition/modules/` if you need to deploy your own registry (not necessary for Reliquary v0.1 — use the canonical singleton).