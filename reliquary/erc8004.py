"""
Reliquary ERC-8004 integration — register a Soul on the on-chain agent registry.

v0.1.0 (this file): off-chain stub. The Soul's registration is recorded
in a local JSON file (`~/.reliquary/registrations.json`) that mimics
the IdentityRegistry's data model. The public API matches what the
on-chain version (v0.1.1) will look like, so swapping in web3.py is a
localized change in this single file.

v0.1.1 (next): real chain integration. Requires web3.py + an RPC URL
+ a funded Soul address. This is GATED on the User (auth + money), so
it's not built in this commit. The public API below is designed not to
change.

ERC-8004 background (see RESEARCH/erc-8004-summary.md for the full picture):
- Three on-chain registries: IdentityRegistry, ReputationRegistry, ValidationRegistry
- An agent is an ERC-721 NFT; agentId = tokenId
- A Soul's secp256k1 keypair → ethereum_address = the msg.sender / owner
- The on-chain calls we'd eventually make:
    identity.functions.register("ipfs://.../agent.json")
    reputation.functions.giveFeedback(agentId, value, valueDecimals, tag1, tag2, ...)
    validation.functions.validationRequest(validatorAddress, agentId, ...)

The stub's job: prove out the integration shape, write the tests, get
the API right, so the v0.1.1 swap is mechanical.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional

from reliquary.soul_v1 import SoulV1


# Default storage path for the off-chain stub.
# Override via the `registry_path` parameter, or via the env var
# RELIQUARY_REGISTRY_PATH, in tests or non-default deployments.
DEFAULT_REGISTRY_PATH = Path.home() / ".reliquary" / "registrations.json"

# Stub chain identifier. Mimics ERC-8004's CAIP-10-ish format
# ("eip155:<chainId>:0x<registry>") so the on-chain swap is mechanical.
STUB_CHAIN_ID = "stub:1"

# When the on-chain version lands, the address per chain looks like:
#   "eip155:1:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"  (mainnet IdentityRegistry)
#   "eip155:11155111:0x8004A818BFB912233c491871b3d84c89A494BD9e"  (Sepolia)
# The stub's "stub:1" is the placeholder until then.


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class RegistrationResult:
    """The result of registering a Soul on the IdentityRegistry.

    Mirrors the fields an on-chain transaction receipt would expose.
    For the stub, tx_hash and block_number are None.
    """
    agent_id: int
    agent_registry: str
    agent_uri: str
    owner: str
    tx_hash: Optional[str]
    block_number: Optional[int]
    registered_at: int

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RegistrationRecord:
    """A stored registration record (the stub's equivalent of a chain event log).

    Storage shape: camelCase (agentId, agentURI, registeredAt) to match
    the on-chain event log schema. The Python attribute names are
    snake_case for idiom; `to_dict` / `from_dict` translate.
    """
    agent_id: int
    owner: str
    agent_uri: str
    registered_at: int
    chain_id: str

    def to_dict(self) -> dict:
        """Return the on-chain-shape dict (camelCase)."""
        return {
            "agentId": self.agent_id,
            "owner": self.owner,
            "agentURI": self.agent_uri,
            "registeredAt": self.registered_at,
            "chainId": self.chain_id,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RegistrationRecord":
        return cls(
            agent_id=d["agentId"],
            owner=d["owner"],
            agent_uri=d["agentURI"],
            registered_at=d["registeredAt"],
            chain_id=d["chainId"],
        )


class AlreadyRegisteredError(Exception):
    """Raised when a Soul is already registered on the given chain."""


class NotRegisteredError(Exception):
    """Raised when looking up a Soul that has no registration."""


# ---------------------------------------------------------------------------
# Storage helpers
# ---------------------------------------------------------------------------


def _default_path() -> Path:
    """Resolve the registry path, honoring RELIQUARY_REGISTRY_PATH if set."""
    env = __import__("os").environ.get("RELIQUARY_REGISTRY_PATH")
    return Path(env) if env else DEFAULT_REGISTRY_PATH


def _load_store(path: Path) -> dict:
    """Load the registrations store. Returns an empty store if file doesn't exist."""
    if not path.exists():
        return {"version": 1, "chains": {}}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_store(path: Path, store: dict) -> None:
    """Save the registrations store. Creates parent dirs if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=2, sort_keys=True)
        f.write("\n")


def _ensure_chain(store: dict, chain_id: str) -> list:
    """Ensure a chain entry exists in the store; return its registrations list."""
    store.setdefault("chains", {}).setdefault(chain_id, [])
    return store["chains"][chain_id]


def _normalize_address(addr: str) -> str:
    """Lowercase + 0x-prefix an Ethereum address for comparison.

    The Soul returns EIP-55 checksummed addresses (`0x7E5F4552...9395Bdf`).
    The stub stores them as-given but compares case-insensitively.
    """
    if not addr.startswith("0x"):
        addr = "0x" + addr
    return "0x" + addr[2:].lower()


# ---------------------------------------------------------------------------
# Public API — these signatures are designed to match the on-chain version.
# ---------------------------------------------------------------------------


def register_soul(
    soul: SoulV1,
    agent_uri: str,
    chain_id: str = STUB_CHAIN_ID,
    registry_path: Optional[Path] = None,
) -> RegistrationResult:
    """Register a Soul on the (stub) IdentityRegistry.

    Mirrors the eventual on-chain call:
        identity.functions.register(agentURI).transact({"from": soul_address})

    Args:
        soul: A SoulV1 to register. Its `ethereum_address` becomes the owner.
        agent_uri: A URI (ipfs://, https://, data:...) pointing to the
            agent registration JSON file.
        chain_id: The chain identifier. Default is the stub.
        registry_path: Override the default storage path. Useful for tests.

    Returns:
        A RegistrationResult with the assigned agent_id, agent_registry,
        and registration metadata.

    Raises:
        AlreadyRegisteredError: if the Soul is already registered on this chain.
    """
    path = registry_path or _default_path()
    store = _load_store(path)
    registrations = _ensure_chain(store, chain_id)

    owner = soul.ethereum_address
    owner_norm = _normalize_address(owner)

    for reg in registrations:
        if _normalize_address(reg["owner"]) == owner_norm:
            raise AlreadyRegisteredError(
                f"Soul {owner} is already registered on {chain_id} "
                f"as agentId {reg['agentId']}"
            )

    # ERC-8004 assigns agentIds incrementally (tokenIds in the ERC-721 mint).
    # In the stub we replicate the same: agentId = len(registrations) + 1.
    agent_id = len(registrations) + 1
    registered_at = int(time.time())

    record = RegistrationRecord(
        agent_id=agent_id,
        owner=owner,
        agent_uri=agent_uri,
        registered_at=registered_at,
        chain_id=chain_id,
    )
    registrations.append(record.to_dict())
    _save_store(path, store)

    return RegistrationResult(
        agent_id=agent_id,
        agent_registry=chain_id,
        agent_uri=agent_uri,
        owner=owner,
        tx_hash=None,  # stub: no real transaction
        block_number=None,  # stub: no real block
        registered_at=registered_at,
    )


def get_agent_id(
    soul: SoulV1,
    chain_id: str = STUB_CHAIN_ID,
    registry_path: Optional[Path] = None,
) -> Optional[int]:
    """Get the agent_id for a Soul on the given chain, or None if not registered.

    Mirrors the on-chain view call:
        identity.functions ... lookup by owner
    """
    path = registry_path or _default_path()
    store = _load_store(path)
    registrations = store.get("chains", {}).get(chain_id, [])
    owner_norm = _normalize_address(soul.ethereum_address)
    for reg in registrations:
        if _normalize_address(reg["owner"]) == owner_norm:
            return reg["agentId"]
    return None


def is_registered(
    soul: SoulV1,
    chain_id: str = STUB_CHAIN_ID,
    registry_path: Optional[Path] = None,
) -> bool:
    """Check if a Soul is registered on the given chain."""
    return get_agent_id(soul, chain_id, registry_path) is not None


def get_agent_uri(
    soul: SoulV1,
    chain_id: str = STUB_CHAIN_ID,
    registry_path: Optional[Path] = None,
) -> Optional[str]:
    """Get the agentURI for a registered Soul, or None if not registered.

    Mirrors the on-chain call:
        identity.functions.tokenURI(agentId).call()
    """
    path = registry_path or _default_path()
    store = _load_store(path)
    registrations = store.get("chains", {}).get(chain_id, [])
    owner_norm = _normalize_address(soul.ethereum_address)
    for reg in registrations:
        if _normalize_address(reg["owner"]) == owner_norm:
            return reg["agentURI"]
    return None


def get_registration(
    soul: SoulV1,
    chain_id: str = STUB_CHAIN_ID,
    registry_path: Optional[Path] = None,
) -> RegistrationRecord:
    """Get the full RegistrationRecord for a Soul, or raise NotRegisteredError."""
    path = registry_path or _default_path()
    store = _load_store(path)
    registrations = store.get("chains", {}).get(chain_id, [])
    owner_norm = _normalize_address(soul.ethereum_address)
    for reg in registrations:
        if _normalize_address(reg["owner"]) == owner_norm:
            return RegistrationRecord.from_dict(reg)
    raise NotRegisteredError(
        f"Soul {soul.ethereum_address} is not registered on {chain_id}"
    )


def list_agents(
    chain_id: str = STUB_CHAIN_ID,
    registry_path: Optional[Path] = None,
) -> List[RegistrationRecord]:
    """List all registered agents on a chain. Mirrors an event-scan over `Registered`."""
    path = registry_path or _default_path()
    store = _load_store(path)
    registrations = store.get("chains", {}).get(chain_id, [])
    return [RegistrationRecord.from_dict(reg) for reg in registrations]


def clear_registry(registry_path: Path) -> None:
    """Test helper: remove the registry file. Not for production use."""
    if registry_path.exists():
        registry_path.unlink()
