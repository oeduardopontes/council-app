#!/usr/bin/env python3
"""
Ask your AI Agent Council a question
All 4 executives will deliberate and provide their perspectives
"""

from council.orchestrator import AgentCouncil

# Initialize the council
council = AgentCouncil()

# Your question - EDIT THIS to ask whatever you want
question = "Should we hire 5 engineers or outsource development?"

# Optional context - EDIT THIS to add relevant details
context = {
    "Budget": "$200K",
    "Timeline": "6 months",
    "Current Team": "3 developers",
    "Project": "Building a SaaS platform"
}

print("\n" + "="*80)
print("ASKING THE AI AGENT COUNCIL")
print("="*80)
print(f"\nQuestion: {question}")
print("\nContext:")
for key, value in context.items():
    print(f"  • {key}: {value}")
print("\n" + "="*80)
print("Council is deliberating...")
print("="*80 + "\n")

# Get the council's recommendation
result = council.deliberate(question=question, context=context)

print("\n" + "="*80)
print("COUNCIL RECOMMENDATION")
print("="*80)
print(result)
print("\n")
