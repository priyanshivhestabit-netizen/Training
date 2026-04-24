import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
import logging
from concurrent.futures import ThreadPoolExecutor
from rich import print

from orchestrator.planner import Planner
from agents.worker_agent import WorkerAgent
from agents.reflection_agent import ReflectionAgent
from agents.validator import Validator


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "day2.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def main():
    print("[bold cyan]DAY 2 - Multi-Agent Orchestration[/bold cyan]\n")

    query = input("Enter your task: ")

    planner = Planner()
    reflector = ReflectionAgent()
    validator = Validator()

    # STEP 1: PLAN
    plan = planner.create_plan(query)

    print("\n[yellow]Execution Tree[/yellow]")
    print("Planner Agent")

    for i, step in enumerate(plan, start=1):
        print(f" ├── Worker-{i}: {step}")

    # STEP 2: PARALLEL WORKERS
    worker_outputs = []

    with ThreadPoolExecutor(max_workers=3) as executor:  #threadpool with 3 workers
        futures = [] 

        for i, task in enumerate(plan, start=1):
            worker = WorkerAgent(i)
            futures.append(executor.submit(worker.execute, task))

        for future in futures:
            worker_outputs.append(future.result())  #waits for each worker to finish and store result

    print("\n[green]Worker Outputs[/green]")

    for output in worker_outputs:
        print(output)

    # STEP 3: REFLECTION
    improved = reflector.improve(worker_outputs)

    print("\n[blue]Reflection Output[/blue]")
    print(improved)

    # STEP 4: VALIDATION
    final = validator.validate(improved)

    print("\n[bold magenta]Final Output[/bold magenta]")
    print(final)


if __name__ == "__main__":
    main()