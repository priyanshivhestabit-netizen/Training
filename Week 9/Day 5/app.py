import streamlit as st
import sys
import os

# ── Path setup 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)

# Import Orchestrator directly from main.py — no duplicate logic
from nexus_ai.main import Orchestrator

# ── Page config 
st.set_page_config(
    page_title="NEXUS AI",
    page_icon="⚡",
    layout="centered"
)

st.title(" NEXUS AI")
st.caption("Autonomous Multi-Agent System — powered by nexus_ai/main.py")

# ── Load Orchestrator once (cached across reruns) 
@st.cache_resource
def load_orchestrator():
    return Orchestrator()

orchestrator = load_orchestrator()

# ── Session state 
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Show chat history 
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat input 
user_input = st.chat_input("Enter your task...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Running pipeline..."):
            response = orchestrator.run(user_input.strip())
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})