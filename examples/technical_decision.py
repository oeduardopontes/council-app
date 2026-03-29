#!/usr/bin/env python3
"""
Example: Technical Architecture Decision

This example demonstrates using the council for technical decisions,
with emphasis on CTO perspective but including business considerations.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from council.orchestrator import AgentCouncil


def main():
    """Run technical decision example"""

    print("=" * 80)
    print("TECHNICAL ARCHITECTURE DELIBERATION")
    print("=" * 80)

    council = AgentCouncil(model_provider="anthropic")

    question = """
    Should we migrate our monolithic application to a microservices architecture?
    """

    context = {
        "Current Architecture": "Ruby on Rails monolith, 200K lines of code, 8 years old",
        "Performance Issues": "Response times degrading, scaling challenges",
        "Team Size": "12 engineers, mostly full-stack",
        "Estimated Effort": "18-24 months for complete migration",
        "Cost": "$2M in engineering time + $300K additional infrastructure",
        "Risk": "Service disruption during migration, learning curve for team",
        "Business Pressure": "Need to ship new features, can't afford long freeze",
        "Alternative": "Could optimize monolith for $500K and 6 months"
    }

    # Include CTO for technical expertise, CFO for cost analysis, CEO for strategic direction
    selected_agents = ['cto', 'cfo', 'ceo']

    print(f"\nConvening: {', '.join([a.upper() for a in selected_agents])}")
    print("\nAnalyzing technical and business implications...\n")

    result = council.deliberate(
        question=question,
        context=context,
        selected_agents=selected_agents
    )

    print("\n" + "=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)
    print(result)


if __name__ == "__main__":
    main()
