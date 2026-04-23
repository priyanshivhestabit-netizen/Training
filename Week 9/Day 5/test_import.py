#!/usr/bin/env python
"""Test the module structure and imports"""

print("Testing imports...")

try:
    from nexus_ai.config import GROK_API_KEY, MODEL
    print(f"✅ Config loaded: MODEL={MODEL}, API_KEY={'SET' if GROK_API_KEY else 'NOT SET'}")
except Exception as e:
    print(f"❌ Config import failed: {e}")

try:
    from nexus_ai.core import llm
    print(f"✅ LLM module loaded successfully")
except Exception as e:
    print(f"❌ LLM import failed: {e}")

# Test actual call if API key exists
if GROK_API_KEY:
    print("\nTesting LLM call...")
    try:
        result = llm("You are a test", "Say 'OK' if you work", max_tokens=20)
        print(f"✅ LLM response: {result}")
    except Exception as e:
        print(f"❌ LLM call failed: {e}")