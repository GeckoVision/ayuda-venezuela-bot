"""The surfcall⇄LLM seam — the bot's safety boundary.

Covers the allow-list (only 5 public reads), the never-raises contract, and `_cap`
keeping JSON valid (the bug class behind the earlier getNews truncation)."""

from __future__ import annotations

import json

from bot.config import SPEC_PATH
from bot.surfcall_tools import PUBLIC_READS, SurfcallTools, _cap


def test_only_public_reads_exposed(tools: SurfcallTools) -> None:
    assert tools.tool_names == PUBLIC_READS
    assert len(PUBLIC_READS) == 5


def test_tools_for_llm_shape(tools: SurfcallTools) -> None:
    defs = tools.tools_for_llm()
    assert defs, "expected at least one tool def"
    for d in defs:
        assert d.keys() >= {"name", "description", "input_schema"}
        assert d["name"] in PUBLIC_READS


def test_call_rejects_non_allowlisted_tool(tools: SurfcallTools) -> None:
    out = json.loads(tools.call("deleteEverything", {}))
    assert "error" in out
    assert "deleteEverything" in out["error"]


def test_custom_allowlist_hides_other_reads() -> None:
    only_news = SurfcallTools(SPEC_PATH, mode="recorded", allowlist={"getNews"})
    assert only_news.tool_names == {"getNews"}
    # a real read that exists in the spec but isn't allow-listed is rejected
    assert "error" in json.loads(only_news.call("searchPersons", {"q": "maria"}))


def test_call_returns_valid_capped_json(tools: SurfcallTools) -> None:
    out = tools.call("getPersonStats", {})
    parsed = json.loads(out)  # must be valid JSON
    assert parsed["status"] == 200  # status is mapped through, not silently dropped
    assert {"missing", "found", "total"} <= set(parsed["data"])  # real recorded shape
    assert len(out) <= tools.max_chars


def test_call_never_raises_on_bad_args(tools: SurfcallTools) -> None:
    # garbage args must degrade to a typed error string, not blow up the bot
    out = tools.call("searchPersons", {"unexpected": object()})  # type: ignore[dict-item]
    assert isinstance(out, str)
    json.loads(out)  # still valid JSON


def test_cap_passes_small_payload_through() -> None:
    payload = {"status": 200, "data": [{"id": 1}]}
    out = _cap(payload, 10_000)
    assert json.loads(out) == payload


def test_cap_trims_oversized_list_but_keeps_valid_json() -> None:
    payload = {"status": 200, "data": [{"x": "y" * 50} for _ in range(200)]}
    out = _cap(payload, 800)

    parsed = json.loads(out)  # the whole point: still parseable
    assert parsed["truncated"] is True
    assert 0 < len(parsed["data"]) < 200
    assert len(out) <= 800


def test_cap_byte_caps_oversized_non_list() -> None:
    payload = {"status": 200, "data": {"blob": "z" * 5000}}
    out = _cap(payload, 200)
    assert len(out) == 200  # last-resort byte cap for a non-list payload
