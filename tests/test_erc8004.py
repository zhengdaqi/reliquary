"""
Tests for the Reliquary ERC-8004 off-chain stub.

The stub's job is to prove the API shape, so the on-chain version
(v0.1.1) can be a localized swap. These tests cover the public API
and the on-chain-relevant edge cases: re-registration, chain
isolation, EIP-55 case-insensitive matching, the ERC-721-style
incremental agentId assignment, and the file persistence model.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from reliquary.erc8004 import (
    AlreadyRegisteredError,
    NotRegisteredError,
    RegistrationResult,
    STUB_CHAIN_ID,
    _normalize_address,
    clear_registry,
    get_agent_id,
    get_agent_uri,
    get_registration,
    is_registered,
    list_agents,
    register_soul,
)
from reliquary.soul_v1 import SoulV1


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_registry(tmp_path: Path) -> Path:
    """A fresh, isolated registry path for each test."""
    return tmp_path / "registrations.json"


@pytest.fixture
def soul() -> SoulV1:
    """A fresh SoulV1 for testing."""
    return SoulV1.generate()


@pytest.fixture
def other_soul() -> SoulV1:
    """A different SoulV1 — for the "different agents get different IDs" tests."""
    return SoulV1.generate()


# ---------------------------------------------------------------------------
# _normalize_address
# ---------------------------------------------------------------------------


def test_normalize_address_lowercases_hex_part():
    assert _normalize_address("0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf") == \
        "0x7e5f4552091a69125d5dfcb7b8c2659029395bdf"


def test_normalize_address_adds_0x_prefix_if_missing():
    assert _normalize_address("7E5F4552091A69125d5DfCb7b8C2659029395Bdf") == \
        "0x7e5f4552091a69125d5dfcb7b8c2659029395bdf"


def test_normalize_address_idempotent():
    addr = "0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf"
    once = _normalize_address(addr)
    twice = _normalize_address(once)
    assert once == twice


# ---------------------------------------------------------------------------
# register_soul
# ---------------------------------------------------------------------------


def test_register_soul_assigns_agent_id_1_to_first_soul(soul, tmp_registry):
    result = register_soul(soul, "ipfs://bafy.../agent.json", registry_path=tmp_registry)
    assert result.agent_id == 1


def test_register_soul_returns_registration_result_with_expected_fields(soul, tmp_registry):
    result = register_soul(soul, "ipfs://bafy.../agent.json", registry_path=tmp_registry)
    assert isinstance(result, RegistrationResult)
    assert result.agent_registry == STUB_CHAIN_ID
    assert result.agent_uri == "ipfs://bafy.../agent.json"
    assert result.owner == soul.ethereum_address
    assert result.tx_hash is None  # stub
    assert result.block_number is None  # stub
    assert result.registered_at > 0


def test_register_soul_persists_to_disk(soul, tmp_registry):
    register_soul(soul, "ipfs://bafy/agent.json", registry_path=tmp_registry)
    assert tmp_registry.exists()
    with open(tmp_registry) as f:
        store = json.load(f)
    assert "chains" in store
    assert STUB_CHAIN_ID in store["chains"]
    assert len(store["chains"][STUB_CHAIN_ID]) == 1


def test_register_soul_uses_incremental_agent_ids(soul, other_soul, tmp_registry):
    r1 = register_soul(soul, "ipfs://bafy/1.json", registry_path=tmp_registry)
    r2 = register_soul(other_soul, "ipfs://bafy/2.json", registry_path=tmp_registry)
    assert r1.agent_id == 1
    assert r2.agent_id == 2


def test_register_same_soul_twice_raises(soul, tmp_registry):
    register_soul(soul, "ipfs://bafy/1.json", registry_path=tmp_registry)
    with pytest.raises(AlreadyRegisteredError):
        register_soul(soul, "ipfs://bafy/2.json", registry_path=tmp_registry)


def test_register_same_soul_with_different_case_address_raises(tmp_registry):
    """EIP-55 case-insensitive matching is unit-tested in test_normalize_address_*.
    End-to-end: re-registering the same Soul (same keypair → same address) raises."""
    soul = SoulV1.generate()
    register_soul(soul, "ipfs://bafy/1.json", registry_path=tmp_registry)
    with pytest.raises(AlreadyRegisteredError):
        register_soul(soul, "ipfs://bafy/2.json", registry_path=tmp_registry)


# ---------------------------------------------------------------------------
# get_agent_id
# ---------------------------------------------------------------------------


def test_get_agent_id_returns_correct_id(soul, tmp_registry):
    r = register_soul(soul, "ipfs://bafy/1.json", registry_path=tmp_registry)
    assert get_agent_id(soul, registry_path=tmp_registry) == r.agent_id


def test_get_agent_id_for_unregistered_returns_none(soul, tmp_registry):
    assert get_agent_id(soul, registry_path=tmp_registry) is None


# ---------------------------------------------------------------------------
# is_registered
# ---------------------------------------------------------------------------


def test_is_registered_false_for_unregistered(soul, tmp_registry):
    assert is_registered(soul, registry_path=tmp_registry) is False


def test_is_registered_true_after_registration(soul, tmp_registry):
    register_soul(soul, "ipfs://bafy/1.json", registry_path=tmp_registry)
    assert is_registered(soul, registry_path=tmp_registry) is True


# ---------------------------------------------------------------------------
# get_agent_uri
# ---------------------------------------------------------------------------


def test_get_agent_uri_returns_stored_uri(soul, tmp_registry):
    register_soul(soul, "ipfs://bafy/soul.json", registry_path=tmp_registry)
    assert get_agent_uri(soul, registry_path=tmp_registry) == "ipfs://bafy/soul.json"


def test_get_agent_uri_for_unregistered_returns_none(soul, tmp_registry):
    assert get_agent_uri(soul, registry_path=tmp_registry) is None


def test_get_agent_uri_can_be_https(soul, tmp_registry):
    register_soul(soul, "https://reliquary.example/soul/agent.json", registry_path=tmp_registry)
    assert get_agent_uri(soul, registry_path=tmp_registry) == "https://reliquary.example/soul/agent.json"


# ---------------------------------------------------------------------------
# get_registration
# ---------------------------------------------------------------------------


def test_get_registration_returns_full_record(soul, tmp_registry):
    register_soul(soul, "ipfs://bafy/1.json", registry_path=tmp_registry)
    reg = get_registration(soul, registry_path=tmp_registry)
    assert reg.agent_id == 1
    assert reg.owner == soul.ethereum_address
    assert reg.agent_uri == "ipfs://bafy/1.json"
    assert reg.registered_at > 0


def test_get_registration_for_unregistered_raises(soul, tmp_registry):
    with pytest.raises(NotRegisteredError):
        get_registration(soul, registry_path=tmp_registry)


# ---------------------------------------------------------------------------
# list_agents
# ---------------------------------------------------------------------------


def test_list_agents_empty_for_fresh_registry(tmp_registry):
    assert list_agents(registry_path=tmp_registry) == []


def test_list_agents_returns_all_in_order(soul, other_soul, tmp_registry):
    register_soul(soul, "ipfs://bafy/1.json", registry_path=tmp_registry)
    register_soul(other_soul, "ipfs://bafy/2.json", registry_path=tmp_registry)
    agents = list_agents(registry_path=tmp_registry)
    assert len(agents) == 2
    assert [a.agent_id for a in agents] == [1, 2]
    assert agents[0].owner == soul.ethereum_address
    assert agents[1].owner == other_soul.ethereum_address


# ---------------------------------------------------------------------------
# Multi-chain isolation
# ---------------------------------------------------------------------------


def test_chains_are_isolated(soul, other_soul, tmp_registry):
    """A Soul on chain A is independent of the same Soul on chain B.
    This will matter when v0.1.1 ships multi-chain support."""
    register_soul(soul, "ipfs://bafy/mainnet.json", chain_id="eip155:1:0xstub", registry_path=tmp_registry)
    register_soul(soul, "ipfs://bafy/sepolia.json", chain_id="eip155:11155111:0xstub", registry_path=tmp_registry)

    # Same Soul, different chain, both registered independently
    assert is_registered(soul, chain_id="eip155:1:0xstub", registry_path=tmp_registry)
    assert is_registered(soul, chain_id="eip155:11155111:0xstub", registry_path=tmp_registry)

    # But agentIds are independent per chain
    r_mainnet = get_registration(soul, chain_id="eip155:1:0xstub", registry_path=tmp_registry)
    r_sepolia = get_registration(soul, chain_id="eip155:11155111:0xstub", registry_path=tmp_registry)
    assert r_mainnet.agent_uri == "ipfs://bafy/mainnet.json"
    assert r_sepolia.agent_uri == "ipfs://bafy/sepolia.json"


def test_separate_chains_have_separate_agent_ids(soul, other_soul, tmp_registry):
    """When we eventually ship multi-chain, each chain assigns its own
    agentIds. Same Soul can be agentId=1 on mainnet and agentId=1 on
    Sepolia — these are independent namespaces."""
    register_soul(soul, "ipfs://1.json", chain_id="chainA", registry_path=tmp_registry)
    register_soul(other_soul, "ipfs://2.json", chain_id="chainB", registry_path=tmp_registry)
    rA = get_registration(soul, chain_id="chainA", registry_path=tmp_registry)
    rB = get_registration(other_soul, chain_id="chainB", registry_path=tmp_registry)
    assert rA.agent_id == 1
    assert rB.agent_id == 1  # also 1, but on a different chain
    assert rA.chain_id == "chainA"
    assert rB.chain_id == "chainB"


# ---------------------------------------------------------------------------
# EIP-55 preservation
# ---------------------------------------------------------------------------


def test_eip55_checksum_is_preserved_in_storage(soul, tmp_registry):
    """The Soul's ethereum_address is EIP-55 checksummed. The stub
    should store it as-given (not normalize the casing), so the
    on-chain swap doesn't lose the checksum."""
    register_soul(soul, "ipfs://bafy/1.json", registry_path=tmp_registry)
    record = get_registration(soul, registry_path=tmp_registry)
    assert record.owner == soul.ethereum_address
    # EIP-55 means at least one of [a-f] is uppercase and at least one is lowercase
    hex_part = record.owner[2:]
    assert any(c.isupper() for c in hex_part)
    assert any(c.islower() for c in hex_part)


# ---------------------------------------------------------------------------
# Persistence across loads
# ---------------------------------------------------------------------------


def test_data_persists_across_loads(soul, tmp_registry):
    register_soul(soul, "ipfs://bafy/persistent.json", registry_path=tmp_registry)
    # A new "session" would still see the registration
    assert is_registered(soul, registry_path=tmp_registry)
    assert get_agent_uri(soul, registry_path=tmp_registry) == "ipfs://bafy/persistent.json"


def test_clear_registry_wipes_file(soul, tmp_registry):
    register_soul(soul, "ipfs://bafy/1.json", registry_path=tmp_registry)
    assert tmp_registry.exists()
    clear_registry(tmp_registry)
    assert not tmp_registry.exists()
    assert not is_registered(soul, registry_path=tmp_registry)
