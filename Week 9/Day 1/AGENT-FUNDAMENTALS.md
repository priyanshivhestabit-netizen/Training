# DAY 1 — Agent Foundations + Message-Based Communication

## Objective

Build a basic multi-agent AI pipeline where different agents handle separate responsibilities.

This demonstrates how modern AI systems are designed using modular agents instead of one chatbot doing everything.

---

## What Is an AI Agent?

An AI agent is a software component that can:

1. Perceive input
2. Reason about the task
3. Take actions
4. Return results

Unlike chatbots, agents can specialize in roles and collaborate.

---

## Agent vs Chatbot vs Pipeline

### Chatbot

Single system answers everything directly.

```text
User → Chatbot → Answer
```

### Pipeline

Fixed step-by-step process.

```text
Input → Step 1 → Step 2 → Output
```

### Agent System

Independent intelligent components communicate.

```text
User → Research Agent → Summarizer → Answer Agent
```

---

## Concepts Learned Today

- Agent architecture
- Role-based prompts
- Message passing
- Memory windows
- Separation of concerns
- Logging and debugging

---

## Project Structure

```
Day 1/
├── agents/
│   ├── research_agent.py
│   ├── summarizer_agent.py
│   └── answer_agent.py
├── logs/
├── main.py
└── AGENT-FUNDAMENTALS.md
```

---

## Agents Built

### 1. Research Agent

**Responsibility**

- Understand user topic
- Gather relevant facts
- Prepare context

**Restrictions**

- Does not summarize
- Does not give final answer

---

### 2. Summarizer Agent

**Responsibility**

- Read research output
- Compress findings
- Simplify information

**Restrictions**

- Does not add new facts
- Does not answer user directly

---

### 3. Answer Agent

**Responsibility**

- Read summary
- Produce final polished response

---

## System Flow

```text
User Query
   ↓
Research Agent
   ↓
Summarizer Agent
   ↓
Answer Agent
   ↓
Final Output
```

---

## Memory Window

Each agent uses:

```python
deque(maxlen=10)
```

This stores only the last 10 interactions.

**Purpose:**

- Keep recent context
- Prevent memory overflow
- Simulate session memory

---

## Logging

All actions are stored in:

```
logs/day1.log
```

**Used for:**

- Debugging
- Monitoring execution
- Tracking agent activity

---

## Why This Design Matters

Large AI systems use multiple smaller agents because:

- Better specialization
- Easier debugging
- Reusable modules
- Higher accuracy
- Easier scaling

---

## Good Coding Practices Used

- OOP class design
- Error handling with `try/except`
- Logging
- Small focused methods
- Clean file structure
- Single responsibility principle

---

## Real World Use Cases

### Customer Support

- Intent Agent
- Search Agent
- Response Agent

### Coding Assistant

- Planner Agent
- Code Agent
- Testing Agent

### Business Analysis

- Data Agent
- Insight Agent
- Report Agent

