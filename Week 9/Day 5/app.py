import streamlit as st
import sys
import os

# ── Path setup ─────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)

from nexus_ai.core.memory import LongTermMemory, VectorStore
from nexus_ai.agents.planner import PlannerAgent
from nexus_ai.agents.researcher import ResearcherAgent
from nexus_ai.agents.coder import CoderAgent
from nexus_ai.agents.analyst import AnalystAgent
from nexus_ai.agents.critic import CriticAgent
from nexus_ai.agents.optimizer import OptimizerAgent
from nexus_ai.agents.validator import ValidatorAgent
from nexus_ai.agents.reporter import ReporterAgent

# ── Page config ────────────────────────────
st.set_page_config(page_title="NEXUS AI", page_icon="⚡", layout="centered")

st.title("⚡ NEXUS AI")
st.caption("Autonomous Multi-Agent Chat System")

# ── Session state (CHAT MEMORY) ────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Load agents ─────────────────────────────
@st.cache_resource
def load_agents():
    return {
        "planner": PlannerAgent(),
        "researcher": ResearcherAgent(),
        "coder": CoderAgent(),
        "analyst": AnalystAgent(),
        "critic": CriticAgent(),
        "optimizer": OptimizerAgent(),
        "validator": ValidatorAgent(),
        "reporter": ReporterAgent(),
        "memory": LongTermMemory(),
        "vector": VectorStore()
    }

agents = load_agents()

# ── Pipeline ────────────────────────────────
def run_task(task):

    plan = agents["planner"].plan(task)
    if isinstance(plan, str):
        plan = [plan]

    outputs = []
    for step in plan:
        try:
            outputs.append(agents["researcher"].research(step, ""))
        except:
            pass

    combined = "\n".join(outputs)

    if any(k in task.lower() for k in ["code", "python", "api", "backend"]):
        draft = agents["coder"].code(combined, task)
    else:
        draft = agents["analyst"].analyze(combined, task)

    critique = agents["critic"].critique(draft)
    improved = agents["optimizer"].optimize(draft, critique)

    final = agents["reporter"].report(task, {"result": improved})
    return final

# ── Show chat history ───────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Input box (CHAT INPUT) ──────────────────
user_input = st.chat_input("Ask something...")

if user_input:

    # show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # run pipeline
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = run_task(user_input)

        st.markdown(response)

    # save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )