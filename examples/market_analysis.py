#!/usr/bin/env python3
"""
Example: Market Analysis and Expansion Decision

This example shows how to use the council for market expansion decisions,
focusing on perspectives from CEO, CFO, and CMO.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from council.orchestrator import AgentCouncil


def main():
    """Run market analysis example"""

    print("="* 80)
    print("MARKET EXPANSION DELIBERATION")
    print("=" * 80)

    # Initialize council
    council = AgentCouncil(model_provider="anthropic")

    # Market expansion question
    question = """
    Should we expand our SaaS product into the European market,
    specifically targeting the UK, Germany, and France?
    """

    context = {
        "Current Market": "US-only, $5M ARR, 500 customers",
        "Growth Rate": "25% YoY in US market",
        "Investment Required": "$1.2M for localization, compliance, marketing",
        "Expected Timeline": "12 months to profitability",
        "Market Research": "TAM of $50M in target markets",
        "Competition": "3 established local competitors, 2 US competitors already there",
        "Regulatory": "GDPR compliance required, data residency requirements",
        "Team Impact": "Need to hire 10-15 people across sales, support, compliance"
    }

    # For market expansion, focus on CEO, CFO, and CMO perspectives
    selected_agents = ['ceo', 'cfo', 'cmo']

    print(f"\nConvening council with: {', '.join([a.upper() for a in selected_agents])}")
    print("\nDeliberating...\n")

    result = council.deliberate(
        question=question,
        context=context,
        selected_agents=selected_agents
    )

    print("\n" + "=" * 80)
    print("COUNCIL DECISION")
    print("=" * 80)
    print(result)


if __name__ == "__main__":
    main()
