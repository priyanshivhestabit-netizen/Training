import os
import sys
import logging
import importlib.util
from rich import print


# -----------------------------------
# Helpers
# -----------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

LOG_DIR = os.path.join(BASE_DIR, "logs")
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "day5.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def load_module(module_name, filepath):
    """Load module safely with error handling"""
    try:
        if not os.path.exists(filepath):
            logging.error(f"File not found: {filepath}")
            print(f"[red]Error: File not found - {filepath}[/red]")
            return None
        
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        logging.info(f"Successfully loaded: {module_name}")
        return module
    except Exception as e:
        logging.error(f"Failed to load {module_name}: {e}")
        print(f"[red]Failed to load {module_name}: {e}[/red]")
        return None


# -----------------------------------
# Fix Path for Day 4 Modules
# -----------------------------------
# Day 4 modules try to load Day 1 modules, so we need to add paths
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "Day 1"))
sys.path.insert(0, os.path.join(ROOT_DIR, "Day 1", "agents"))
sys.path.insert(0, os.path.join(ROOT_DIR, "Day 4"))
sys.path.insert(0, os.path.join(ROOT_DIR, "Day 4", "memory"))

# -----------------------------------
# Load Day 1 Files
# -----------------------------------
research_mod = load_module(
    "research_agent",
    os.path.join(ROOT_DIR, "Day 1", "agents", "research_agent.py")
)

summary_mod = load_module(
    "summarizer_agent",
    os.path.join(ROOT_DIR, "Day 1", "agents", "summarizer_agent.py")
)

answer_mod = load_module(
    "answer_agent",
    os.path.join(ROOT_DIR, "Day 1", "agents", "answer_agent.py")
)

# Check if Day 1 modules loaded
if not all([research_mod, summary_mod, answer_mod]):
    print("[red]Critical: Day 1 modules failed to load[/red]")
    sys.exit(1)

# -----------------------------------
# Load Day 2 Files
# -----------------------------------
planner_mod = load_module(
    "planner",
    os.path.join(ROOT_DIR, "Day 2", "orchestrator", "planner.py")
)

reflection_mod = load_module(
    "reflection_agent",
    os.path.join(ROOT_DIR, "Day 2", "agents", "reflection_agent.py")
)

validator_mod = load_module(
    "validator",
    os.path.join(ROOT_DIR, "Day 2", "agents", "validator.py")
)

if not all([planner_mod, reflection_mod, validator_mod]):
    print("[red]Critical: Day 2 modules failed to load[/red]")
    sys.exit(1)

# -----------------------------------
# Load Day 3 Files (Optional)
# -----------------------------------
file_mod = load_module(
    "file_agent",
    os.path.join(ROOT_DIR, "Day 3", "tools", "file_agent.py")
)

code_mod = load_module(
    "code_executor",
    os.path.join(ROOT_DIR, "Day 3", "tools", "code_executor.py")
)

db_mod = load_module(
    "db_agent",
    os.path.join(ROOT_DIR, "Day 3", "tools", "db_agent.py")
)

# -----------------------------------
# Load Day 4 Files with Dependency Fix
# -----------------------------------
# Create a wrapper to fix internal load_module calls in Day 4 modules
original_load_module = None

try:
    # First, try to load session_memory but intercept its internal imports
    session_memory_path = os.path.join(ROOT_DIR, "Day 4", "memory", "session_memory.py")
    
    # Read the file and create a modified version temporarily
    with open(session_memory_path, 'r') as f:
        content = f.read()
    
    # Create a temporary fixed version that doesn't try to load modules
    temp_dir = os.path.join(BASE_DIR, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    temp_file = os.path.join(temp_dir, "session_memory_fixed.py")
    
    # Comment out the internal load_module calls
    import re
    fixed_content = re.sub(
        r'(\s+)(\w+_mod = load_module\([^)]+\))',
        r'\1# \2  # Commented out to prevent circular loading',
        content
    )
    
    # Also add print statements for debugging
    fixed_content = "# Fixed version for Day 5\n" + fixed_content
    
    with open(temp_file, 'w') as f:
        f.write(fixed_content)
    
    # Load the fixed version
    session_mod = load_module("session_memory_fixed", temp_file)
    
    # Similarly for other Day 4 modules
    long_term_path = os.path.join(ROOT_DIR, "Day 4", "memory", "long_term_memory.py")
    with open(long_term_path, 'r') as f:
        long_content = f.read()
    
    long_temp = os.path.join(temp_dir, "long_term_memory_fixed.py")
    long_fixed = re.sub(
        r'(\s+)(\w+_mod = load_module\([^)]+\))',
        r'\1# \2',
        long_content
    )
    with open(long_temp, 'w') as f:
        f.write(long_fixed)
    
    long_mod = load_module("long_term_memory_fixed", long_temp)
    
    # Vector store
    vector_path = os.path.join(ROOT_DIR, "Day 4", "memory", "vector_store.py")
    with open(vector_path, 'r') as f:
        vector_content = f.read()
    
    vector_temp = os.path.join(temp_dir, "vector_store_fixed.py")
    vector_fixed = re.sub(
        r'(\s+)(\w+_mod = load_module\([^)]+\))',
        r'\1# \2',
        vector_content
    )
    with open(vector_temp, 'w') as f:
        f.write(vector_fixed)
    
    vector_mod = load_module("vector_store_fixed", vector_temp)
    
except Exception as e:
    logging.error(f"Failed to load Day 4 modules: {e}")
    print(f"[yellow]Warning: Day 4 modules failed to load, using fallbacks[/yellow]")
    
    # Fallback classes
    class SessionMemory:
        def __init__(self, limit=10):
            self.limit = limit
            self.memory = []
            print("[green]Using fallback SessionMemory[/green]")
        
        def add(self, role, content):
            self.memory.append({"role": role, "content": content})
            if len(self.memory) > self.limit:
                self.memory.pop(0)
        
        def get_context(self):
            return self.memory
    
    class LongTermMemory:
        def __init__(self, db_path):
            self.db_path = db_path
            print("[green]Using fallback LongTermMemory[/green]")
        
        def setup(self):
            pass
        
        def store(self, content):
            pass
    
    class VectorStore:
        def __init__(self):
            self.items = []
            print("[green]Using fallback VectorStore[/green]")
        
        def add(self, text):
            self.items.append(text)
        
        def search(self, query, top_k=1):
            return [f"Recalled: {query}"] if self.items else ["No memory available"]
    
    session_mod = type('obj', (object,), {'SessionMemory': SessionMemory})
    long_mod = type('obj', (object,), {'LongTermMemory': LongTermMemory})
    vector_mod = type('obj', (object,), {'VectorStore': VectorStore})


# -----------------------------------
# Main App
# -----------------------------------
def main():
    print("[bold cyan]NEXUS AI - Final Integrated Capstone[/bold cyan]\n")
    
    # Debug: Print loaded modules
    print("[dim]Checking loaded modules...[/dim]")
    modules_ok = True
    
    if not research_mod or not hasattr(research_mod, 'ResearchAgent'):
        print("[red]✗ ResearchAgent not loaded[/red]")
        modules_ok = False
    else:
        print("[green]✓ ResearchAgent loaded[/green]")
    
    if not summary_mod or not hasattr(summary_mod, 'SummarizerAgent'):
        print("[red]✗ SummarizerAgent not loaded[/red]")
        modules_ok = False
    else:
        print("[green]✓ SummarizerAgent loaded[/green]")
    
    if not answer_mod or not hasattr(answer_mod, 'AnswerAgent'):
        print("[red]✗ AnswerAgent not loaded[/red]")
        modules_ok = False
    else:
        print("[green]✓ AnswerAgent loaded[/green]")
    
    if not planner_mod or not hasattr(planner_mod, 'Planner'):
        print("[red]✗ Planner not loaded[/red]")
        modules_ok = False
    else:
        print("[green]✓ Planner loaded[/green]")
    
    if not reflection_mod or not hasattr(reflection_mod, 'ReflectionAgent'):
        print("[red]✗ ReflectionAgent not loaded[/red]")
        modules_ok = False
    else:
        print("[green]✓ ReflectionAgent loaded[/green]")
    
    if not validator_mod or not hasattr(validator_mod, 'Validator'):
        print("[red]✗ Validator not loaded[/red]")
        modules_ok = False
    else:
        print("[green]✓ Validator loaded[/green]")
    
    if not modules_ok:
        print("\n[red]Error: Required modules not loaded properly![/red]")
        print("[yellow]Please check that all agent files exist in Day 1 and Day 2 folders[/yellow]")
        return

    task = input("\nEnter complex task: ").strip()

    if not task:
        print("[red]Task cannot be empty.[/red]")
        return

    logging.info(f"User task: {task}")
    print(f"\n[cyan]Processing task: {task}[/cyan]\n")

    try:
        # Instantiate Classes
        print("[dim]Initializing agents...[/dim]")
        planner = planner_mod.Planner()
        researcher = research_mod.ResearchAgent()
        summarizer = summary_mod.SummarizerAgent()
        answerer = answer_mod.AnswerAgent()
        reflector = reflection_mod.ReflectionAgent()
        validator = validator_mod.Validator()
        
        session = session_mod.SessionMemory(limit=10)
        memory_db = os.path.join(DATA_DIR, "nexus_memory.db")
        long_memory = long_mod.LongTermMemory(memory_db)
        long_memory.setup()
        vector = vector_mod.VectorStore()
        
        print("[green]✓ All agents initialized[/green]\n")

        # Memory
        session.add("user", task)
        long_memory.store(task)
        vector.add(task)
        recalled = vector.search(task, top_k=1)

        # Planning
        print("[yellow]Creating execution plan...[/yellow]")
        plan = planner.create_plan(task)
        
        if not plan:
            print("[red]Plan creation failed![/red]")
            return

        print("\n[yellow]Execution Plan:[/yellow]")
        for i, step in enumerate(plan, 1):
            print(f"  {i}. {step}")

        # Research Phase
        print("\n[cyan]Researching each step...[/cyan]")
        worker_outputs = []
        
        for i, step in enumerate(plan, 1):
            print(f"  Processing step {i}/{len(plan)}: {step[:50]}...")
            result = researcher.process(step)
            worker_outputs.append(result)
            logging.info(f"Step {i} completed")

        # Reflection
        print("\n[cyan]Reflecting on outputs...[/cyan]")
        improved = reflector.improve(worker_outputs)

        # Summarization
        print("[cyan]Summarizing results...[/cyan]")
        summary = summarizer.process(improved)

        # Final Answer
        print("[cyan]Generating final answer...[/cyan]")
        final_answer = answerer.process(summary)

        # Validation
        print("[cyan]Validating answer...[/cyan]")
        validated = validator.validate(final_answer)

        # Save to memory
        session.add("assistant", validated)
        long_memory.store(validated)
        vector.add(validated)

        # Output
        print("\n[green]Memory Recall[/green]")
        print(f"  {recalled[0] if recalled else 'No recall'}")

        print("\n[blue]Improved Draft[/blue]")
        print(f"  {improved[:200]}{'...' if len(improved) > 200 else ''}")

        print("\n[bold magenta]Final Output[/bold magenta]")
        print(f"  {validated}")

        print("\n[bold green]✓ Task completed successfully![/bold green]")
        logging.info("NEXUS AI completed successfully")

    except AttributeError as e:
        logging.exception("Missing method in agent")
        print(f"\n[red]Error: Agent method missing - {e}[/red]")
        print("[yellow]Make sure all agent classes have required methods[/yellow]")
        
    except Exception as e:
        logging.exception("Application crashed")
        print(f"\n[red]Error: {e}[/red]")
        print(f"[yellow]Check log: {os.path.join(LOG_DIR, 'day5.log')}[/yellow]")


if __name__ == "__main__":
    main()