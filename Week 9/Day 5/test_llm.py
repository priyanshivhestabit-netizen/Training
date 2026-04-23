#!/usr/bin/env python
"""
Test the LLM connection
"""
import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("=" * 50)
print("Testing LLM Configuration")
print("=" * 50)

# Check environment variables
grok_key = os.getenv("GROQ_API_KEY") or os.getenv("XAI_API_KEY")
print(f"\n1. Environment Check:")
print(f"   GROK_API_KEY set: {'✅ YES' if grok_key else '❌ NO'}")
if grok_key:
    print(f"   Key starts with: {grok_key[:10]}...")

# Test imports
print(f"\n2. Import Check:")
try:
    from nexus_ai.config import GROQ_API_KEY, GROQ_API_URL, MODEL, MAX_RETRIES
    print(f"   ✅ Config imported successfully")
    print(f"   Model: {MODEL}")
    print(f"   URL: {GROQ_API_URL}")
    print(f"   Max retries: {MAX_RETRIES}")
    print(f"   API Key loaded: {'✅ YES' if GROQ_API_KEY else '❌ NO'}")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test LLM call
print(f"\n3. Testing LLM Call:")
try:
    from nexus_ai.core.llm import call_llm
    result = call_llm(
        system="You are a test assistant. Respond with 'OK' if you receive this message.",
        user="Say 'API is working' if you can read this.",
        max_tokens=50
    )
    print(f"   ✅ LLM call successful!")
    print(f"   Response: {result}")
except Exception as e:
    print(f"   ❌ LLM call failed: {e}")

print("\n" + "=" * 50)
