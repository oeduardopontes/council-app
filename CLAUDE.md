# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r web_requirements.txt
cp .env.example .env   # fill in ANTHROPIC_API_KEY
```

## Development Commands

```bash
# Run dev server (port 8080)
source venv/bin/activate && python app.py

# Run production server
./start_council.sh  # Gunicorn, 4 workers

# Format code
black .

# Smoke tests (not pytest — standalone scripts)
python test_simple.py   # initializes council, polls CEO
python test_api.py      # direct Anthropic SDK connectivity check
python verify_setup.py  # environment check
python demo.py          # full council deliberation demo
```

## Architecture

This is a Flask web app that orchestrates a panel of AI agents to deliberate on a business question and produce a synthesized answer.

### Request flow
1. `POST /api/deliberate` → spawns a background thread, returns a `session_id`
2. Client polls `GET /api/progress/<session_id>` via Server-Sent Events
3. Background thread runs `AgentCouncil.deliberate()` in `council/orchestrator.py`
4. Each agent (CEO, CFO, CTO, CMO) runs sequentially via CrewAI `Crew`/`Task`
5. CEO agent runs a final synthesis pass; result is pushed to the SSE queue

### Key files
| File | Role |
|------|------|
| `app.py` | Flask routes, SSE streaming, rate limiting, background thread management |
| `council/orchestrator.py` | `AgentCouncil`: wires agents into a CrewAI crew, runs deliberation |
| `council/decision_framework.py` | `DecisionFramework`: formats prompts, classifies decision types |
| `agents/base_agent.py` | `BaseAgent`: loads YAML profile → CrewAI `Agent` |
| `config/agent_profiles.yaml` | YAML profiles for ceo, cfo, cto, cmo, analyst |
| `i18n.py` + `translations/` | Bilingual support (English / Brazilian Portuguese) |

### Agent types
- **Corporate council** (`agents/ceo.py`, `cfo.py`, `cto.py`, `cmo.py`): thin subclasses of `BaseAgent`, fully wired into the orchestrator. These are what runs.
- **DJ/Producer mentor agents** (`agents/ar.py`, `coach.py`, `produtor.py`, etc.): contain only an `AGENT_CONFIG` dict — **not yet integrated** into the orchestrator or `agents/__init__.py`. Described in `AGENTS_README.md` as planned future work.

### Known issues
- `orchestrator.py` at the repo root is a stale duplicate of `council/orchestrator.py`. The app imports from `council.orchestrator`.
- Rate limiting in `app.py` uses an in-memory dict — does not work correctly across Gunicorn's 4 workers.
- The `Users/` directory inside the repo is an accidental artifact (empty nested path).

## Environment Variables

```
ANTHROPIC_API_KEY=...
DEFAULT_MODEL=claude-3-haiku-20240307
TEMPERATURE=0.7
MAX_ITERATIONS=5
```

The default model in `base_agent.py` is `claude-3-haiku-20240307`; `council/orchestrator.py` falls back to `claude-3-5-sonnet-20241022`.

## Production Deployment

The app runs as a macOS LaunchAgent (`com.council.app`) on a Mac Mini (`edumini.local:8080`). See `SERVICE_MANAGEMENT.md` for `launchctl` commands.
