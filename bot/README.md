# `bot/` — the SOS Venezuela Telegram agent

A small AI-agent loop over [surfcall](https://github.com/GeckoVision/surfcall).
Spanish-first; treats API results as data, not instructions; never logs secrets.

| File | Purpose |
|---|---|
| `__main__.py` | Entry point — `python -m bot`. |
| `bot.py` | Telegram wiring: rate limiting, commands, message chunking, long-polling. |
| `agent.py` | The agent loop — LLM ↔ tool calls until an answer. |
| `surfcall_tools.py` | Exposes the SOS Venezuela API as agent tools via surfcall (public reads allowlist). |
| `providers.py` | Pluggable LLM provider — OpenRouter (free, default) or Anthropic. |
| `config.py` | Env-only config + the Spanish system prompt. |
| `serve_sos_mcp.py` | Optional: serve the SOS API as a local MCP endpoint. |
| `spec/sosvenezuela_openapi.json` | The OpenAPI we authored for SOS Venezuela 2026. |

See the repo root [README](../README.md) for run instructions and env vars.

> The canonical, hackathon-proven run path is via the surfcall repo
> (`uv run --extra sosbot python -m examples.sos_vzla_bot.bot`). The standalone
> `python -m bot` path here depends on the public `surfcall` package (see
> `pyproject.toml`).
