import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import logging
from rich import print

from agents.research_agent import ResearchAgent
from agents.summarizer_agent import SummarizerAgent
from agents.answer_agent import AnswerAgent

import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "day1.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def main():
    print("[bold cyan]DAY 1 - Multi Agent Flow[/bold cyan]\n")

    user_query = input("Enter your question: ")

    research = ResearchAgent()
    summarizer = SummarizerAgent()
    answer = AnswerAgent()

    research_output = research.process(user_query)
    print("\n[yellow]Research Output:[/yellow]")
    print(research_output)

    summary_output = summarizer.process(research_output)
    print("\n[green]Summary Output:[/green]")
    print(summary_output)

    final_output = answer.process(summary_output)
    print("\n[bold magenta]Final Output:[/bold magenta]")
    print(final_output)


if __name__ == "__main__":
    main()