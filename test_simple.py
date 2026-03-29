#!/usr/bin/env python3
"""
Simple test to verify the council is working
"""

from council.orchestrator import AgentCouncil

print("Initializing AI Agent Council...")
council = AgentCouncil(model_provider="anthropic")

print("\n✓ Council initialized successfully!")

print("\nCouncil Members:")
agents = council.get_agent_info()
for agent_type, info in agents.items():
    print(f"  • {info['role']}")

print("\n" + "=" * 60)
print("Testing with a simple question to the CEO...")
print("=" * 60)

response = council.quick_poll(
    "In one sentence, what's the most important factor for startup success?",
    agent_type="ceo"
)

print("\nCEO Response:")
print(response)

print("\n✓ Test completed successfully!")
print("\nYour council is ready to use. Try:")
print("  python demo.py (for full demo)")
print("  python examples/strategic_decision.py (for examples)")
