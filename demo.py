#!/usr/bin/env python3
"""
Simple Interactive Demo - AI Agent Council

This shows you the basic ways to use your council.
"""

from council.orchestrator import AgentCouncil


def main():
    print("=" * 80)
    print("AI AGENT COUNCIL - INTERACTIVE DEMO")
    print("=" * 80)

    # Initialize the council
    print("\nInitializing council with Anthropic Claude...")
    council = AgentCouncil(model_provider="anthropic")

    print("\n✓ Council ready!")
    print("\nYour council members:")
    agents = council.get_agent_info()
    for agent_type, info in agents.items():
        print(f"  • {info['role']}")
        print(f"    Focus: {', '.join(info['expertise'][:3])}")

    print("\n" + "=" * 80)
    print("EXAMPLE 1: Full Council Deliberation")
    print("=" * 80)

    # Example question
    question = """
    Should we invest $200K to build an AI-powered chatbot for customer support?
    This would replace our current email-based support system.
    """

    context = {
        "Current Support Cost": "$150K/year (3 support staff)",
        "Customer Base": "5,000 active users",
        "Average Response Time": "24-48 hours",
        "Customer Complaints": "30% mention slow support",
        "Development Time": "4 months",
        "Maintenance": "$30K/year"
    }

    print(f"\nQuestion: {question.strip()}")
    print("\nContext:")
    for key, value in context.items():
        print(f"  • {key}: {value}")

    print("\n" + "-" * 80)
    print("Starting council deliberation...")
    print("-" * 80)

    # Run the deliberation
    result = council.deliberate(question, context)

    print("\n" + "=" * 80)
    print("COUNCIL RECOMMENDATION:")
    print("=" * 80)
    print(result)

    print("\n" + "=" * 80)
    print("EXAMPLE 2: Quick Poll (Single Agent)")
    print("=" * 80)

    print("\nAsking just the CTO for technical advice...")
    tech_question = "What are the top 3 AI trends we should watch in 2024?"

    print(f"Question: {tech_question}")
    print("\n" + "-" * 80)

    cto_response = council.quick_poll(tech_question, agent_type="cto")

    print("\nCTO Response:")
    print("-" * 80)
    print(cto_response)

    print("\n" + "=" * 80)
    print("DEMO COMPLETE!")
    print("=" * 80)
    print("\nYou can now:")
    print("1. Modify this demo.py file to ask your own questions")
    print("2. Check out examples/ for more use cases")
    print("3. Import council in your own Python scripts")
    print("\nHappy deliberating!")


if __name__ == "__main__":
    main()
