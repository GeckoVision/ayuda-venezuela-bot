"""Telegram transport — the pure handlers, rate limiter, command routing, chunking."""

from __future__ import annotations

from bot.bot import (
    EMPTY_ES,
    HELP_ES,
    RATE_LIMIT_ES,
    WELCOME_ES,
    RateLimiter,
    chunk_message,
    handle_command,
    handle_message,
    resolve_command,
)
from bot.agent import FALLBACK_ES


def echo(text: str) -> str:
    return f"echo:{text}"


# --- RateLimiter ---------------------------------------------------------------


def test_rate_limiter_blocks_over_budget_then_recovers() -> None:
    rl = RateLimiter(max_per_min=2)
    assert rl.allow(1, now=0.0)
    assert rl.allow(1, now=1.0)
    assert not rl.allow(1, now=2.0)  # third within the window
    assert rl.allow(1, now=61.0)  # window slid past the first two
    # a different user has an independent budget
    assert rl.allow(2, now=2.0)


# --- handle_message ------------------------------------------------------------


def test_empty_message_prompts() -> None:
    rl = RateLimiter(8)
    assert handle_message("   ", 1, responder=echo, limiter=rl, now=0.0) == EMPTY_ES


def test_rate_limited_message() -> None:
    rl = RateLimiter(1)
    handle_message("hola", 1, responder=echo, limiter=rl, now=0.0)
    assert (
        handle_message("otra", 1, responder=echo, limiter=rl, now=0.1) == RATE_LIMIT_ES
    )


def test_responder_exception_degrades_not_crashes() -> None:
    def boom(_text: str) -> str:
        raise RuntimeError("upstream down")

    rl = RateLimiter(8)
    assert handle_message("hola", 1, responder=boom, limiter=rl, now=0.0) == FALLBACK_ES


def test_normal_message_runs_responder() -> None:
    rl = RateLimiter(8)
    assert handle_message("hola", 1, responder=echo, limiter=rl, now=0.0) == "echo:hola"


# --- command routing -----------------------------------------------------------


def test_resolve_command_static_and_queries() -> None:
    assert resolve_command("/start", "") == (WELCOME_ES, None)
    assert resolve_command("/ayuda", "") == (HELP_ES, None)
    assert resolve_command("/help", "") == (HELP_ES, None)

    static, query = resolve_command("/buscar", "María Pérez")
    assert static is None and query is not None and "María Pérez" in query

    static, query = resolve_command("/cifras", "")
    assert static is None and query is not None


def test_resolve_command_strips_mention_and_handles_unknown() -> None:
    # "/start@DEV_VEZbot" must resolve like "/start"
    assert resolve_command("/start@DEV_VEZbot", "") == (WELCOME_ES, None)
    assert resolve_command("/desconocido", "") == (None, None)


def test_buscar_without_arg_prompts() -> None:
    static, query = resolve_command("/buscar", "")
    assert static is not None and query is None


def test_handle_command_routes_query_through_responder() -> None:
    rl = RateLimiter(8)
    out = handle_command("noticias", "", 1, responder=echo, limiter=rl, now=0.0)
    assert out.startswith("echo:")


def test_handle_command_unknown_shows_help() -> None:
    rl = RateLimiter(8)
    assert handle_command("xyz", "", 1, responder=echo, limiter=rl, now=0.0) == HELP_ES


# --- chunking ------------------------------------------------------------------


def test_chunk_short_message_is_single() -> None:
    assert chunk_message("hola") == ["hola"]


def test_chunk_long_message_respects_limit_and_preserves_words() -> None:
    text = " ".join(f"palabra{i}" for i in range(1000))
    chunks = chunk_message(text, limit=200)
    assert len(chunks) > 1
    assert all(len(c) <= 200 for c in chunks)
    # no words lost or split across the join
    assert " ".join(chunks).split() == text.split()
