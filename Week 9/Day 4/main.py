import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
import logging
from rich import print
from rich.panel import Panel

from autogen import AssistantAgent
from config import LLM_CONFIG

from memory.session_memory import SessionMemory
from memory.long_term_memory import LongTermMemory
from memory.vector_store import VectorStore

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "day4.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def call_llm(prompt: str) -> str:
    agent = AssistantAgent(
        name="memory_agent",
        system_message="""
You are a helpful assistant with memory of past conversations.

Use the provided memory context to give personalized,
relevant, practical responses.
""",
        llm_config=LLM_CONFIG
    )

    reply = agent.generate_reply(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return str(reply)

def main():
    logging.info("Day 4 started")

    print("[bold cyan]DAY 4 - Memory Systems[/bold cyan]\n")

    # Init memory systems
    session = SessionMemory(limit=10)

    db_path = os.path.join(DATA_DIR, "long_term.db")

    long_memory = LongTermMemory(db_path)
    long_memory.setup()

    vector = VectorStore()

    # Seed memory
    past_memories = [
        "User likes AI startup ideas",
        "User asked about scalable backend systems",
        "User wants CSV business analytics",
        "User is building a multi-agent AI system in Python",
        "User prefers concise and practical answers"
    ]

    print("[dim]Loading past memories into vector store...[/dim]")

    for item in past_memories:
        long_memory.store(item)
        vector.add(item)

    print(f"[dim]Seeded {len(past_memories)} memories[/dim]\n")

    print("[bold]Type your query (or 'exit' to quit)[/bold]\n")

    while True:
        query = input("You: ").strip()

        if query.lower() in ("exit", "quit"):
            break

        if not query:
            continue

        logging.info(f"User query: {query}")

        # STEP 1: session memory
        session.add("user", query)

        # STEP 2: retrieve relevant memory
        recalled = vector.search(query, top_k=2)

        logging.info(f"Recalled: {recalled}")

        # STEP 3: Build prompt
        session_context = session.format_for_prompt()

        memory_context = (
            "\n".join(f"- {item}" for item in recalled)
            if recalled else "None"
        )

        prompt = f"""
You have access to memory.

## Recalled Long-Term Memory:
{memory_context}

## Current Conversation:
{session_context}

Now respond to the user's latest message thoughtfully.
Use memory when relevant.
"""

        print("\n[yellow]Searching memory...[/yellow]")

        for item in recalled:
            print(f"  [dim]↳ recalled: {item}[/dim]")

        print("[yellow]Generating response...[/yellow]\n")

        # STEP 4: LLM response
        response = call_llm(prompt)

        # STEP 5: store memories
        session.add("assistant", response)

        long_memory.store(
            f"Q: {query} | A: {response[:200]}"
        )

        vector.add(
            f"{query} {response[:100]}"
        )

        print(
            Panel(
                response,
                title="[bold magenta]Agent Response[/bold magenta]",
                border_style="magenta"
            )
        )
        print()

    print("\n[bold cyan]Session ended. All memories stored.[/bold cyan]")

    logging.info("Day 4 session complete")

if __name__ == "__main__":
    main()