"""BotConfig.from_env — provider selection, overrides, and the redaction promise."""

from __future__ import annotations

import pytest

from bot.config import ANTHROPIC_MODEL, BotConfig
from bot.providers import DEFAULT_FREE_MODEL


def _clear(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in (
        "TELEGRAM_BOT_TOKEN",
        "SOSBOT_PROVIDER",
        "OPENROUTER_API_KEY",
        "ANTHROPIC_API_KEY",
        "SOSBOT_MODEL",
        "SOSBOT_MODE",
    ):
        monkeypatch.delenv(var, raising=False)


def test_defaults_to_free_openrouter(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear(monkeypatch)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "tok")
    monkeypatch.setenv("OPENROUTER_API_KEY", "or-key")

    cfg = BotConfig.from_env()

    assert cfg.provider == "openrouter"
    assert cfg.model == DEFAULT_FREE_MODEL
    assert cfg.llm_api_key == "or-key"
    assert cfg.mode == "live"  # default


def test_anthropic_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear(monkeypatch)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "tok")
    monkeypatch.setenv("SOSBOT_PROVIDER", "anthropic")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant")

    cfg = BotConfig.from_env()

    assert cfg.provider == "anthropic"
    assert cfg.model == ANTHROPIC_MODEL


def test_model_and_mode_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear(monkeypatch)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "tok")
    monkeypatch.setenv("OPENROUTER_API_KEY", "or-key")
    monkeypatch.setenv("SOSBOT_MODEL", "some/other-model")
    monkeypatch.setenv("SOSBOT_MODE", "recorded")

    cfg = BotConfig.from_env()

    assert cfg.model == "some/other-model"
    assert cfg.mode == "recorded"


def test_missing_token_names_only_the_var(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear(monkeypatch)
    monkeypatch.setenv("OPENROUTER_API_KEY", "or-key")  # token missing

    with pytest.raises(RuntimeError) as exc:
        BotConfig.from_env()

    assert "TELEGRAM_BOT_TOKEN" in str(exc.value)


def test_error_never_leaks_a_present_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    """One var missing must not cause the *other*, present secret to appear in the
    error message — the redaction promise in config.py."""
    _clear(monkeypatch)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "super-secret-token-value")
    # OPENROUTER_API_KEY missing -> error should name it, never echo the token value

    with pytest.raises(RuntimeError) as exc:
        BotConfig.from_env()

    msg = str(exc.value)
    assert "OPENROUTER_API_KEY" in msg
    assert "super-secret-token-value" not in msg
