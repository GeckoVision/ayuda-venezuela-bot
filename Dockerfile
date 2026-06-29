# The Telegram bot worker (long-polling — no inbound ports).
# The Next.js landing deploys separately on Vercel; this image is just the bot.
#
#   docker build -t ayuda-venezuela-bot .
#   docker run --rm --env-file .env ayuda-venezuela-bot
#
# Installs gecko-surf + the agent stack from PyPI, so the running bot never
# depends on a git checkout being available.
FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

# Build + install the bot package (which pulls its deps from PyPI). README is
# referenced by pyproject's `readme`, so it must be present for the build.
COPY pyproject.toml README.md ./
COPY bot ./bot
RUN uv pip install --system --no-cache .

# Drop privileges — the bot needs no root and writes nothing.
RUN useradd --create-home app
USER app

# Requires TELEGRAM_BOT_TOKEN + a provider key (OPENROUTER_API_KEY or
# ANTHROPIC_API_KEY) in the environment; see .env.example.
CMD ["python", "-m", "bot"]
