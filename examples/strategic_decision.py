#!/usr/bin/env python3
"""
Example: Strategic Decision Making with Agent Council

This example demonstrates how to use the AI Agent Council to make
strategic business decisions with input from multiple executive perspectives.
"""

import sys
import os

# Add parent directory to path to import council modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from council.orchestrator import AgentCouncil


def main():
    """Run strategic decision example"""

    print("Initializing AI Agent Council...")
    print("-" * 80)

    # Initialize the council with Anthropic Claude
    council = AgentCouncil(model_provider="anthropic")

    # Display agent information
    print("\nCouncil Members:")
    agents_info = council.get_agent_info()
    for agent_type, info in agents_info.items():
        print(f"\n  {info['role']}:")
        print(f"    Goal: {info['goal'][:80]}...")
        print(f"    Expertise: {', '.join(info['expertise'][:3])}")

    print("\n" + "=" * 80)
    print("STRATEGIC DECISION EXAMPLE")
    print("=" * 80)

    # Example question
    question = """
    Should our company invest in developing an AI-powered customer service platform?
    This would require a $500K initial investment and 6 months of development time.
    """

    # Additional context
    context = {
        "Current State": "Using traditional customer service (phone + email)",
        "Customer Base": "50,000 active users, growing 10% monthly",
        "Support Team": "15 customer service representatives",
        "Budget Available": "$750K allocated for innovation projects",
        "Competition": "2 main competitors already using AI chatbots",
        "Timeline Pressure": "Board wants to see innovation within Q2"
    }

    # Conduct deliberation
    print("\nStarting council deliberation...\n")
    result = council.deliberate(question, context)

    print("\n" + "=" * 80)
    print("COUNCIL RECOMMENDATION")
    print("=" * 80)
    print(result)


def quick_question_example():
    """Example of asking a quick question to a single agent"""

    print("\n" + "=" * 80)
    print("QUICK POLL EXAMPLE")
    print("=" * 80)

    council = AgentCouncil(model_provider="anthropic")

    question = "What are the top 3 technology trends we should watch in 2024?"

    print(f"\nAsking CTO: {question}\n")
    response = council.quick_poll(question, agent_type="cto")

    print("\nCTO Response:")
    print(response)


if __name__ == "__main__":
    # Run main example
    main()

    # Optionally run quick poll example
    # Uncomment the line below to try it
    # quick_question_example()
