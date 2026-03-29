#!/usr/bin/env python3
"""
Quick setup verification script
Checks that all components are properly installed and importable
"""

import sys


def verify_setup():
    """Verify all components are working"""
    print("Verifying AI Agent Council Setup...")
    print("=" * 60)

    checks = []

    # Check 1: Python version
    print("\n1. Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro}")
        checks.append(True)
    else:
        print(f"   ✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.10+)")
        checks.append(False)

    # Check 2: Core dependencies
    print("\n2. Checking core dependencies...")
    dependencies = [
        'crewai',
        'anthropic',
        'openai',
        'langchain',
        'langchain_anthropic',
        'langchain_openai',
        'yaml',
        'dotenv'
    ]

    all_deps_ok = True
    for dep in dependencies:
        try:
            if dep == 'yaml':
                __import__('yaml')
            elif dep == 'dotenv':
                __import__('dotenv')
            else:
                __import__(dep)
            print(f"   ✓ {dep}")
        except ImportError as e:
            print(f"   ✗ {dep}: {e}")
            all_deps_ok = False

    checks.append(all_deps_ok)

    # Check 3: Custom modules
    print("\n3. Checking custom modules...")
    try:
        from agents import CEOAgent, CFOAgent, CTOAgent, CMOAgent
        print("   ✓ Agent modules")
        checks.append(True)
    except ImportError as e:
        print(f"   ✗ Agent modules: {e}")
        checks.append(False)

    try:
        from council.orchestrator import AgentCouncil
        from council.decision_framework import DecisionFramework
        print("   ✓ Council modules")
        checks.append(True)
    except ImportError as e:
        print(f"   ✗ Council modules: {e}")
        checks.append(False)

    # Check 4: Configuration files
    print("\n4. Checking configuration files...")
    import os
    config_files = [
        'config/agent_profiles.yaml',
        '.env.example',
        'requirements.txt'
    ]

    all_configs_ok = True
    for config in config_files:
        if os.path.exists(config):
            print(f"   ✓ {config}")
        else:
            print(f"   ✗ {config} (missing)")
            all_configs_ok = False

    checks.append(all_configs_ok)

    # Check 5: Environment setup
    print("\n5. Checking environment setup...")
    if os.path.exists('.env'):
        print("   ✓ .env file exists")

        from dotenv import load_dotenv
        load_dotenv()

        has_key = False
        if os.getenv('ANTHROPIC_API_KEY'):
            print("   ✓ ANTHROPIC_API_KEY configured")
            has_key = True
        elif os.getenv('OPENAI_API_KEY'):
            print("   ✓ OPENAI_API_KEY configured")
            has_key = True
        else:
            print("   ⚠ No API key found in .env (add ANTHROPIC_API_KEY or OPENAI_API_KEY)")
            has_key = False

        checks.append(has_key)
    else:
        print("   ⚠ .env file not found (copy .env.example to .env and add your API key)")
        checks.append(False)

    # Summary
    print("\n" + "=" * 60)
    if all(checks):
        print("✓ All checks passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Make sure you have an API key in .env")
        print("2. Run an example: python examples/strategic_decision.py")
        return True
    else:
        print("✗ Some checks failed. Please review the issues above.")
        return False


if __name__ == "__main__":
    success = verify_setup()
    sys.exit(0 if success else 1)
