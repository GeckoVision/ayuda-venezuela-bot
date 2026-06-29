"""Provider pluggability — the OpenAI-compatible adapter that lets a free OpenRouter
model drive the exact same Anthropic-shaped agent loop."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from bot.providers import (
    OpenAICompatLLM,
    _Block,
    make_llm,
    to_openai_messages,
    to_openai_tools,
)


def test_to_openai_tools_shape() -> None:
    tools = [
        {"name": "getNews", "description": "news", "input_schema": {"type": "object"}}
    ]
    out = to_openai_tools(tools)
    assert out == [
        {
            "type": "function",
            "function": {
                "name": "getNews",
                "description": "news",
                "parameters": {"type": "object"},
            },
        }
    ]


def test_to_openai_messages_translates_tool_roundtrip() -> None:
    messages = [
        {"role": "user", "content": "hola"},
        {
            "role": "assistant",
            "content": [_Block("tool_use", id="t1", name="getNews", input={"q": "x"})],
        },
        {
            "role": "user",
            "content": [{"type": "tool_result", "tool_use_id": "t1", "content": "{}"}],
        },
    ]
    out = to_openai_messages("sys", messages)

    assert out[0] == {"role": "system", "content": "sys"}
    assert out[1] == {"role": "user", "content": "hola"}
    assistant = out[2]
    assert assistant["role"] == "assistant"
    assert assistant["tool_calls"][0]["function"]["name"] == "getNews"
    tool_msg = out[3]
    assert tool_msg == {"role": "tool", "tool_call_id": "t1", "content": "{}"}


# --- the OpenAI-compatible adapter, against a fake OpenAI client ----------------


@dataclass
class _FakeFn:
    name: str
    arguments: str


@dataclass
class _FakeToolCall:
    id: str
    function: _FakeFn


@dataclass
class _FakeMsg:
    content: str | None = None
    tool_calls: list[_FakeToolCall] | None = None


class _FakeChoices:
    def __init__(self, msg: _FakeMsg) -> None:
        self.choices = [type("C", (), {"message": msg})()]


class _FakeOpenAI:
    """Minimal `client.chat.completions.create` returning a queued message."""

    def __init__(self, msg: _FakeMsg) -> None:
        self._msg = msg
        self.chat = type("Chat", (), {"completions": self})()

    def create(self, **_kwargs: Any) -> _FakeChoices:
        return _FakeChoices(self._msg)


def test_adapter_maps_tool_calls_to_tool_use() -> None:
    msg = _FakeMsg(
        tool_calls=[_FakeToolCall("c1", _FakeFn("getReports", '{"limit": 3}'))]
    )
    llm = OpenAICompatLLM(_FakeOpenAI(msg))

    resp = llm.messages.create(
        model="m", max_tokens=10, system="s", tools=[], messages=[]
    )

    assert resp.stop_reason == "tool_use"
    block = resp.content[0]
    assert block.type == "tool_use" and block.name == "getReports"
    assert block.input == {"limit": 3}


def test_adapter_plain_text_is_end_turn() -> None:
    llm = OpenAICompatLLM(_FakeOpenAI(_FakeMsg(content="Hola")))
    resp = llm.messages.create(
        model="m", max_tokens=10, system="s", tools=[], messages=[]
    )
    assert resp.stop_reason == "end_turn"
    assert resp.content[0].text == "Hola"


def test_adapter_tolerates_malformed_tool_arguments() -> None:
    msg = _FakeMsg(tool_calls=[_FakeToolCall("c1", _FakeFn("getNews", "not-json"))])
    llm = OpenAICompatLLM(_FakeOpenAI(msg))
    resp = llm.messages.create(
        model="m", max_tokens=10, system="s", tools=[], messages=[]
    )
    assert resp.content[0].input == {}  # bad JSON -> empty args, no crash


def test_make_llm_openrouter_builds_compat_client() -> None:
    assert isinstance(make_llm("openrouter", "or-key"), OpenAICompatLLM)
