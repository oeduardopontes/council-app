#!/usr/bin/env python3
"""
Interactive Terminal UI for AI Agent Council
Simple text-based interface for asking questions
"""

from council.orchestrator import AgentCouncil
import sys


def print_header():
    print("\n" + "="*80)
    print("🏢  AI AGENT COUNCIL - Interactive Session")
    print("="*80)


def get_question():
    print("\n📝 What would you like to ask the council?")
    print("(Type your question, or 'quit' to exit)\n")
    question = input("Question: ").strip()

    if question.lower() in ['quit', 'exit', 'q']:
        print("\nThank you for consulting the council! Goodbye.\n")
        sys.exit(0)

    return question


def get_context():
    print("\n📊 Would you like to add context? (y/n)")
    add_context = input("> ").strip().lower()

    if add_context != 'y':
        return None

    context = {}
    print("\nAdd context items (press Enter with empty key to finish):")

    while True:
        key = input("  Key (e.g., 'Budget'): ").strip()
        if not key:
            break
        value = input(f"  Value for '{key}': ").strip()
        context[key] = value

    return context if context else None


def select_agents():
    print("\n👥 Which executives should deliberate?")
    print("1. All executives (CEO, CFO, CTO, CMO)")
    print("2. Just the CEO")
    print("3. CEO + CFO (strategic + financial)")
    print("4. CEO + CTO (strategic + technical)")
    print("5. Custom selection")

    choice = input("\nChoice (1-5): ").strip()

    if choice == '1':
        return None  # All agents
    elif choice == '2':
        return ['ceo']
    elif choice == '3':
        return ['ceo', 'cfo']
    elif choice == '4':
        return ['ceo', 'cto']
    elif choice == '5':
        print("\nSelect agents (comma-separated): ceo, cfo, cto, cmo")
        agents = input("> ").strip().split(',')
        return [a.strip() for a in agents]
    else:
        return None


def main():
    print_header()

    print("\n🚀 Initializing AI Agent Council...")
    council = AgentCouncil()

    print("✅ Council ready!")
    print("\n📋 Available executives:")
    agents = council.get_agent_info()
    for agent_type, info in agents.items():
        print(f"  • {info['role']} ({agent_type.upper()})")

    while True:
        try:
            # Get question
            question = get_question()

            # Get optional context
            context = get_context()

            # Select agents
            selected_agents = select_agents()

            # Show summary
            print("\n" + "-"*80)
            print("📌 DELIBERATION SUMMARY")
            print("-"*80)
            print(f"Question: {question}")
            if context:
                print("\nContext:")
                for k, v in context.items():
                    print(f"  • {k}: {v}")
            if selected_agents:
                print(f"\nExecutives: {', '.join([a.upper() for a in selected_agents])}")
            else:
                print("\nExecutives: All (CEO, CFO, CTO, CMO)")
            print("-"*80)

            # Ask for confirmation
            proceed = input("\nProceed with deliberation? (y/n): ").strip().lower()
            if proceed != 'y':
                print("Cancelled.\n")
                continue

            # Run deliberation
            print("\n⏳ Council is deliberating... (this may take 30-60 seconds)\n")

            if selected_agents and len(selected_agents) == 1:
                # Quick poll for single agent
                result = council.quick_poll(question, agent_type=selected_agents[0])
            else:
                # Full deliberation
                result = council.deliberate(
                    question=question,
                    context=context,
                    selected_agents=selected_agents
                )

            # Show result
            print("\n" + "="*80)
            print("💡 COUNCIL RECOMMENDATION")
            print("="*80)
            print(result)
            print("="*80 + "\n")

            # Ask if user wants to continue
            another = input("Ask another question? (y/n): ").strip().lower()
            if another != 'y':
                print("\nThank you for consulting the council! Goodbye.\n")
                break

        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            print("Let's try again...\n")


if __name__ == "__main__":
    main()
