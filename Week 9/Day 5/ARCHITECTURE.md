## System Flow

```
User Task
    │
    ▼
┌─────────────────────────────────────────────┐
│              ORCHESTRATOR                   │
│                                             │
│  ┌──────────┐    ┌──────────────────────┐   │
│  │  Memory  │───▶│  0. Memory Recall    │   │
│  │  Layer   │    └──────────┬───────────┘   │
│  └──────────┘               │               │
│                             ▼               │
│                   ┌──────────────────────┐  │
│                   │  1. Planner          │  │
│                   │  → 4-6 step plan     │  │
│                   └──────────┬───────────┘  │
│                              │              │
│                              ▼              │
│                   ┌──────────────────────┐  │
│                   │  2. Researcher ×N    │  │
│                   │  → one per step      │  │
│                   └──────────┬───────────┘  │
│                              │              │
│                              ▼              │
│                   ┌──────────────────────┐  │
│                   │  3. Role Switch      │  │
│                   │  Coder  OR  Analyst  │  │
│                   │  (keyword detection) │  │
│                   └──────────┬───────────┘  │
│                              │              │
│                              ▼              │
│              ┌───────────────────────────┐  │
│              │  4. Self-Reflection Loop  │  │
│              │   Critic → Optimizer ×2   │  │
│              └──────────────┬────────────┘  │
│                             │               │
│                             ▼               │
│                   ┌──────────────────────┐  │
│                   │  5. Validator        │  │
│                   │  PASS → continue     │  │
│                   │  FAIL → retry once   │  │
│                   └──────────┬───────────┘  │
│                              │              │
│                              ▼              │
│                   ┌──────────────────────┐  │
│                   │  6. Reporter         │  │
│                   │  → Final Report      │  │
│                   └──────────────────────┘  │
└─────────────────────────────────────────────┘
```

## Memory Architecture

| Layer        | Storage          | Scope           |
|---|---|---|
| Session      | In-memory deque  | Current run     |
| Long-Term    | SQLite           | Persistent      |
| Vector       | FAISS + embeddings | Semantic recall |

## Agent Roles

| Agent      | Role |
|---|---|
| Planner    | Breaks task into 4-6 actionable subtasks |
| Researcher | Gathers facts and context per subtask |
| Coder      | Produces architecture, code, tech design |
| Analyst    | Produces SWOT, risks, recommendations |
| Critic     | Finds flaws and gaps in draft output |
| Optimizer  | Fixes issues raised by Critic |
| Validator  | QA gate — PASS or FAIL with recovery |
| Reporter   | Synthesizes everything into final report |

## Failure Recovery
- Every agent step wrapped in `_step()` with `MAX_RETRIES` attempts
- Validator failure triggers one extra Critic → Optimizer round
- LLM timeout/error returns a safe fallback string (never crashes)

## Role Switching
NEXUS AI detects task type by keyword matching:
- Technical keywords → `CoderAgent`
- Otherwise → `AnalystAgent`