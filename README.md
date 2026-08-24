# Architecture GPT

Generate **editable software architectures**, **implementation roadmaps** and
**infrastructure cost estimates** from a plain-language product description —
with a critic loop that keeps regenerating the diagram until it scores at
least 80/100 on a staff-level review, instead of trusting a single-shot draft.

Every pipeline step is routed across **5 SOTA LLMs from 5 providers**
(Claude, GPT, Gemini, Grok, DeepSeek) with automatic cross-provider failover,
orchestrated with **LangGraph**, routed through **LiteLLM** and served by
**FastAPI**.

## How it works

```
                        ┌─────────────────────────────────────────────┐
                        │              LangGraph pipeline             │
                        │                                             │
 project title/desc ──► analyze ──► architect ──► critic ──┬─ score   │
                        │             (diagram)      ▲     │  >= 80?  │
                        │                             │     │         │
                        │                             └─ improve      │
                        │                                (loop)       │
                        │                                  │          │
                        │                                  ▼          │
                        │                    roadmap ──► costs ──► done│
                        └─────────────────────────────────────────────┘
                              each node routes through LiteLLM to its
                              own model fleet with provider failover
```

| Pipeline step | Model fleet (first = preferred, rest = failover) |
| --- | --- |
| architecture + analysis | `claude-sonnet-5` → `gpt-5.1` → `gemini-3-pro` → `grok-4` |
| critique | `gpt-5.1` → `claude-opus-5` → `gemini-3-pro` |
| roadmap | `gemini-3-pro` → `claude-sonnet-5` → `deepseek-chat` |
| infra costs | `gpt-5.1` → `deepseek-chat` → `gemini-3-pro` |
| diagram editing | `claude-sonnet-5` → `gpt-5.1` → `grok-4` |

Every fleet is overridable per environment (`LLM_<USE_CASE>_MODELS`), and
every call is audited: which model served it, tokens, latency and estimated
USD cost are stored on the generation run.

## Backend setup

```bash
cd backend
python -m venv venv
venv/Scripts/activate          # windows
pip install -r requirements.txt
copy .env.example .env         # then fill in the provider API keys you use
uvicorn app.main:app --reload  # docs at http://localhost:8000/docs
```

The server must run from `backend/` so relative imports and `.env` resolve.
SQLite is used by default (`architecture_gpt.db` is created on startup);
point `DATABASE_URL` at Postgres/MySQL to change that.

## API walkthrough

```bash
# 1. create a project
curl -X POST localhost:8000/api/v1/projects \
  -H 'content-type: application/json' \
  -d '{"title": "Food delivery app", "description": "…"}'

# 2. kick off a generation run (executes in the background)
curl -X POST localhost:8000/api/v1/generations \
  -H 'content-type: application/json' -d '{"project_id": 1}'

# 3. poll it: status, quality score, per-step model routing and spend
curl localhost:8000/api/v1/generations/1

# 4. fetch the artifacts (all editable via PUT)
curl localhost:8000/api/v1/architectures/1          # draw.io mxGraphModel XML
curl localhost:8000/api/v1/architectures/1/roadmap  # phases, milestones, tasks
curl localhost:8000/api/v1/architectures/1/costs    # monthly infra line items

# 5. edit the diagram with a natural-language prompt (routes through the
#    edit model fleet) — the result opens directly in diagrams.net
curl -X POST localhost:8000/api/v1/prompts/prompt \
  -H 'content-type: application/json' \
  -d '{"architecture_id": 1, "prompt": "add a redis cache in front of the API"}'
```

## Repository layout

```
backend/
  app/
    api/v1/          routers: auth, users, projects, architectures, prompts, generations
    config/          settings, database, LLM routing configuration
    models/          SQLAlchemy models (projects, architectures, roadmaps, costs, generations)
    schemas/         pydantic request/response models
    services/
      llm/           LiteLLM model router (use case -> model fleet)
      generation/    LangGraph pipeline: state, prompts, nodes, graph
      …              CRUD + orchestration services
frontend/            Vite + React app (in progress)
```
