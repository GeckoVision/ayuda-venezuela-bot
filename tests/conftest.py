"""Shared fixtures — everything runs offline, $0, no secrets.

`recorded mode` synthesizes API responses from the spec schema (no network), and
the LLM is a scripted fake in the Anthropic shape (`bot.providers._Resp/_Block`),
so the whole bot is exercised without Telegram, Anthropic, OpenRouter, or a token.
"""

from __future__ import annotations

from typing import Any

import pytest

from bot.config import SPEC_PATH
from bot.providers import _Block, _Resp
from bot.surfcall_tools import SurfcallTools


@pytest.fixture
def tools() -> SurfcallTools:
    """Real surfcall seam over the bundled SOS Venezuela spec, in recorded mode."""
    return SurfcallTools(SPEC_PATH, mode="recorded")


def text_turn(text: str) -> _Resp:
    """A model turn that just answers (end_turn)."""
    return _Resp([_Block("text", text=text)], "end_turn")


def tool_turn(
    name: str, *, call_id: str = "t1", args: dict[str, Any] | None = None
) -> _Resp:
    """A model turn that requests one tool (tool_use)."""
    return _Resp(
        [_Block("tool_use", id=call_id, name=name, input=args or {})], "tool_use"
    )


class ScriptedLLM:
    """Fake Anthropic-shaped client. Returns the queued `_Resp`s in order; records
    every `create` call so a test can assert what the agent sent."""

    def __init__(self, *turns: _Resp) -> None:
        self._turns = list(turns)
        self.calls: list[dict[str, Any]] = []
        self.messages = self  # llm.messages.create -> self.create

    def create(self, **kwargs: Any) -> _Resp:
        self.calls.append(kwargs)
        if self._turns:
            return self._turns.pop(0)
        return text_turn("")  # ran past the script — model "stopped"
