# NEXUS AI — Autonomous Multi-Agent System

**Day 5 Capstone** of a 5-day multi-agent AI training program.

## What It Does
NEXUS AI is a fully autonomous multi-agent system that takes any complex task and runs it through a structured pipeline of 8 specialist agents with memory, self-reflection, and failure recovery.

## Quick Start
```bash
cd "Day 5"
python -m nexus_ai.main
```

## Requirements
```bash
pip install rich faiss-cpu numpy requests
ollama pull phi3:mini
ollama pull nomic-embed-text   # optional, for semantic memory
```

## Example Tasks
- `Plan a startup in AI for healthcare`
- `Generate backend architecture for a scalable app`
- `Design a RAG pipeline for 50k documents`
- `Analyze CSV and create a business strategy`

## Project Structure
```
Day 5/
├── nexus_ai/
│   ├── main.py          ← Orchestrator + entry point
│   ├── config.py        ← All settings
│   ├── core/
│   │   ├── llm.py       ← Central LLM caller with retries
│   │   └── memory.py    ← Session + SQLite + FAISS vector store
│   └── agents/
│       ├── planner.py
│       ├── researcher.py
│       ├── coder.py
│       ├── analyst.py
│       ├── critic.py
│       ├── optimizer.py
│       ├── validator.py
│       └── reporter.py
├── logs/day5.log
├── data/nexus_memory.db
├── README.md
├── ARCHITECTURE.md
└── FINAL-REPORT.md
```