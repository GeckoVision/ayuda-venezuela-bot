"""The Claude tool-use loop — driven by a scripted fake LLM over recorded tools."""

from __future__ import annotations

from bot import agent
from bot.surfcall_tools import SurfcallTools

from .conftest import ScriptedLLM, text_turn, tool_turn

KW = dict(model="m", system="s", max_tokens=256, max_iters=4)


def test_answers_directly_when_no_tool_needed(tools: SurfcallTools) -> None:
    llm = ScriptedLLM(text_turn("Hola, ¿en qué te ayudo?"))
    reply = agent.respond("hola", llm=llm, tools=tools, **KW)
    assert reply == "Hola, ¿en qué te ayudo?"
    assert len(llm.calls) == 1


def test_executes_tool_then_answers(tools: SurfcallTools) -> None:
    llm = ScriptedLLM(
        tool_turn("getPersonStats"),
        text_turn("Hay 43.948 personas reportadas."),
    )
    reply = agent.respond("¿cuántos desaparecidos?", llm=llm, tools=tools, **KW)

    assert reply == "Hay 43.948 personas reportadas."
    # second call carried the assistant tool_use + the tool_result back to the model
    second = llm.calls[1]["messages"]
    assert any(
        isinstance(m["content"], list)
        and any(
            isinstance(b, dict) and b.get("type") == "tool_result" for b in m["content"]
        )
        for m in second
    )


def test_empty_final_text_degrades_to_fallback(tools: SurfcallTools) -> None:
    llm = ScriptedLLM(text_turn(""))  # model returned nothing usable
    reply = agent.respond("hola", llm=llm, tools=tools, **KW)
    assert reply == agent.FALLBACK_ES


def test_runaway_tool_loop_hits_budget_and_falls_back(tools: SurfcallTools) -> None:
    # model keeps asking for tools forever; the loop must stop at max_iters
    llm = ScriptedLLM(*[tool_turn("getReports", call_id=f"t{i}") for i in range(10)])
    reply = agent.respond(
        "loop", llm=llm, tools=tools, model="m", system="s", max_iters=3
    )
    assert reply == agent.FALLBACK_ES
    assert len(llm.calls) == 3  # never exceeded the budget


def test_history_is_prepended(tools: SurfcallTools) -> None:
    llm = ScriptedLLM(text_turn("ok"))
    history = [{"role": "user", "content": "anterior"}]
    agent.respond("nuevo", llm=llm, tools=tools, history=history, **KW)
    sent = llm.calls[0]["messages"]
    assert sent[0] == {"role": "user", "content": "anterior"}
    assert sent[-1] == {"role": "user", "content": "nuevo"}
