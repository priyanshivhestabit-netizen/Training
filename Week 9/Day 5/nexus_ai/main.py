"""
NEXUS AI — Autonomous Multi-Agent System
Day 5 Capstone
"""
import os
import sys
import time
import logging
from rich import print
from rich.panel import Panel
from rich.rule  import Rule
from rich.console import Console

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # nexus_ai/
DAY5_DIR = os.path.dirname(BASE_DIR)                    # Day 5/
sys.path.insert(0, DAY5_DIR)

from nexus_ai.config import LOG_FILE, MAX_RETRIES, MEMORY_DB
from nexus_ai.core.llm    import call_llm
from nexus_ai.core.memory import SessionMemory, LongTermMemory, VectorStore

from nexus_ai.agents.planner    import PlannerAgent
from nexus_ai.agents.researcher import ResearcherAgent
from nexus_ai.agents.coder      import CoderAgent
from nexus_ai.agents.analyst    import AnalystAgent
from nexus_ai.agents.critic     import CriticAgent
from nexus_ai.agents.optimizer  import OptimizerAgent
from nexus_ai.agents.validator  import ValidatorAgent
from nexus_ai.agents.reporter   import ReporterAgent

# ── Logging ───────────────────────────────────────────────────────────────────
os.makedirs(os.path.join(DAY5_DIR, "logs"), exist_ok=True)
os.makedirs(os.path.join(DAY5_DIR, "data"), exist_ok=True)

logging.basicConfig(
    filename=os.path.join(DAY5_DIR, LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger  = logging.getLogger(__name__)
console = Console()


# ── Orchestrator ──────────────────────────────────────────────────────────────
class Orchestrator:
    def __init__(self):
        # Memory
        self.session   = SessionMemory()
        self.long_mem  = LongTermMemory()
        self.vector    = VectorStore()

        # Agents
        self.planner    = PlannerAgent()
        self.researcher = ResearcherAgent()
        self.coder      = CoderAgent()
        self.analyst    = AnalystAgent()
        self.critic     = CriticAgent()
        self.optimizer  = OptimizerAgent()
        self.validator  = ValidatorAgent()
        self.reporter   = ReporterAgent()

        # Seed memory with system knowledge
        seeds = [
            "NEXUS AI handles multi-agent orchestration with planning, research, coding, and analysis",
            "System supports role switching between Researcher, Coder, and Analyst based on task type",
            "All outputs go through Critic → Optimizer loop for self-improvement",
        ]
        for s in seeds:
            self.vector.add(s)
            self.long_mem.store(s, category="system")

    def _step(self, label: str, fn, *args):
        """Run a step with failure recovery — retries up to MAX_RETRIES."""
        console.print(f"  [dim]→ {label}...[/dim]")
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                result = fn(*args)
                # Handle list results (Planner returns a list)
                if isinstance(result, list) and len(result) > 0:
                    logger.info(f"[{label}] completed (attempt {attempt})")
                    return result
                # Handle string results (all other agents)
                if isinstance(result, str) and len(result.strip()) > 20:
                    logger.info(f"[{label}] completed (attempt {attempt})")
                    return result
                logger.warning(f"[{label}] empty result on attempt {attempt}")
            except Exception as e:
                logger.warning(f"[{label}] attempt {attempt} error: {e}")
            # Wait between retries to respect Groq rate limits
            time.sleep(5)
        logger.error(f"[{label}] all retries failed")
        return f"[{label} failed after {MAX_RETRIES} retries]"

    def run(self, task: str):
        logger.info(f"NEXUS AI task: {task}")
        self.session.add("user", task)
        self.long_mem.store(task, category="task")
        self.vector.add(task)

        # ── 0. Memory Recall ──────────────────────────────────────────────
        console.print(Rule("[yellow]Memory Recall[/yellow]"))
        recalled = self.vector.search(task, top_k=2)
        memory_context = "\n".join(f"- {r}" for r in recalled)
        if recalled:
            for r in recalled:
                console.print(f"  [dim]↳ {r}[/dim]")
        else:
            console.print("  [dim]No prior memory found[/dim]")

        # ── 1. Planning ───────────────────────────────────────────────────
        console.print(Rule("[yellow]Phase 1 — Planning[/yellow]"))
        plan = self._step("Planner", self.planner.plan, task)
        if isinstance(plan, str):   # fallback returned a string
            plan = [plan]

        console.print(f"\n  [bold]Execution Plan ({len(plan)} steps):[/bold]")
        for i, step in enumerate(plan, 1):
            console.print(f"  [cyan]{i}.[/cyan] {step}")

        # ── 2. Research Phase ─────────────────────────────────────────────
        console.print(Rule("[yellow]Phase 2 — Research[/yellow]"))
        research_outputs = []
        for i, step in enumerate(plan, 1):
            out = self._step(f"Researcher-{i}", self.researcher.research, step, memory_context)
            research_outputs.append(out)
            self.vector.add(out[:200])
            time.sleep(2)   # pause between researcher calls to avoid 429

        combined_research = "\n\n".join(
            f"[Step {i+1}] {plan[i]}\n{out}"
            for i, out in enumerate(research_outputs)
        )

        # ── 3. Role Switching — Coder or Analyst? ─────────────────────────
        console.print(Rule("[yellow]Phase 3 — Role Switch (Coder / Analyst)[/yellow]"))

        TECHNICAL_KEYWORDS = ["architecture", "backend", "code", "pipeline", "system", "api",
                               "database", "rag", "infrastructure", "deploy", "stack"]
        is_technical = any(kw in task.lower() for kw in TECHNICAL_KEYWORDS)

        if is_technical:
            console.print("  [dim]Role → Coder Agent (technical task detected)[/dim]")
            specialist_out = self._step("Coder", self.coder.code, combined_research, task)
        else:
            console.print("  [dim]Role → Analyst Agent (business/strategy task detected)[/dim]")
            specialist_out = self._step("Analyst", self.analyst.analyze, combined_research, task)

        # ── 4. Self-Reflection Loop (Critic → Optimizer) ──────────────────
        console.print(Rule("[yellow]Phase 4 — Self-Reflection[/yellow]"))

        draft = specialist_out
        for iteration in range(1, 3):   # up to 2 improvement rounds
            console.print(f"  [dim]Reflection round {iteration}/2[/dim]")
            critique = self._step("Critic",    self.critic.critique, draft)
            time.sleep(2)
            draft    = self._step("Optimizer", self.optimizer.optimize, draft, critique)
            time.sleep(2)

        # ── 5. Validation ─────────────────────────────────────────────────
        console.print(Rule("[yellow]Phase 5 — Validation[/yellow]"))
        passed, validated = self.validator.validate(draft, task)

        if not passed:
            console.print("  [red]Validation failed — running one more optimization[/red]")
            logger.warning("Validation failed — triggering recovery optimization")
            time.sleep(2)
            critique = self._step("Critic",    self.critic.critique, draft)
            time.sleep(2)
            draft    = self._step("Optimizer", self.optimizer.optimize, draft, critique)
            time.sleep(2)
            passed, validated = self.validator.validate(draft, task)

        status = "[green]PASSED[/green]" if passed else "[red]FAILED (proceeding anyway)[/red]"
        console.print(f"  Validation: {status}")

        # ── 6. Final Report ───────────────────────────────────────────────
        console.print(Rule("[yellow]Phase 6 — Report Generation[/yellow]"))

        all_outputs = {
            "Research Summary":          combined_research[:800],
            "Technical/Analysis Output": specialist_out,
            "Optimized Draft":           draft,
            "Validation":                validated[:300],
        }
        time.sleep(2)
        final_report = self._step("Reporter", self.reporter.report, task, all_outputs)

        # ── Store everything to memory ─────────────────────────────────────
        self.session.add("assistant", final_report)
        self.long_mem.store(f"Task: {task} | Report: {final_report[:300]}", category="output")
        self.vector.add(final_report[:200])

        return final_report


# ── Entry Point ───────────────────────────────────────────────────────────────
def main():
    console.print(Panel.fit(
        "[bold cyan]NEXUS AI[/bold cyan] [white]— Autonomous Multi-Agent System[/white]\n"
        "[dim]v1.0 | Orchestrator + 8 Agents + Memory + Self-Reflection[/dim]",
        border_style="cyan"
    ))

    print()
    # Init orchestrator ONCE — memory persists across turns
    orchestrator = Orchestrator()

    while True:
        task = input("\nYou: ").strip()
        if not task:
            continue
        if task.lower() in ("exit", "quit", "bye"):
            print("[bold cyan]NEXUS AI shutting down. Goodbye.[/bold cyan]")
            break

        print()
        final_report = orchestrator.run(task)

        console.print(Rule("[bold magenta]FINAL REPORT[/bold magenta]"))
        console.print(Panel(final_report, border_style="magenta", title="[bold]NEXUS AI Output[/bold]"))

        logger.info("NEXUS AI completed")

if __name__ == "__main__":
    main()