# Creating New Councils and Agents

This guide explains how to create new AI agents and group them into specialized councils for different domains.

## Table of Contents

1. [Understanding the Agent Structure](#understanding-the-agent-structure)
2. [Creating a New Agent](#creating-a-new-agent)
3. [Creating a New Council](#creating-a-new-council)
4. [Adding Translations](#adding-translations)
5. [Examples](#examples)

---

## Understanding the Agent Structure

Each agent in the system has:

- **Profile**: Role, goal, and backstory that defines the agent's expertise
- **Expertise Areas**: List of specific skills/knowledge domains
- **Decision Weight**: How different decision types affect the agent's priority
- **CrewAI Agent**: The underlying AI agent powered by Claude

### Agent File Structure

Agents are defined in the `agents/` directory. Each agent type has its own file.

Example structure:
```
agents/
├── __init__.py          # Exports all agents
├── base_agent.py        # Base class for all agents
├── ceo_agent.py         # CEO agent implementation
├── cfo_agent.py         # CFO agent implementation
└── ...
```

---

## Creating a New Agent

### Step 1: Create the Agent File

Create a new file in the `agents/` directory. For example, `agents/coo_agent.py`:

```python
from crewai import Agent
from .base_agent import BaseAgent


class COOAgent(BaseAgent):
    """
    Chief Operating Officer - Operations and Process Excellence
    """

    def __init__(self):
        # Define the agent's profile
        profile = {
            'role': 'Chief Operating Officer',
            'goal': 'Optimize operations, improve processes, and ensure efficient execution',
            'backstory': """You are an experienced Chief Operating Officer with 20+ years
            of experience in operations management, process optimization, and operational
            excellence. You excel at identifying inefficiencies, streamlining workflows,
            and ensuring smooth day-to-day operations. You focus on scalability, quality
            control, and operational metrics."""
        }

        # Define areas of expertise
        expertise = [
            'Operations management',
            'Process optimization',
            'Supply chain',
            'Quality control',
            'Operational efficiency'
        ]

        # Define decision weights for different types
        decision_weight = {
            'strategic': 0.7,      # Less focused on high-level strategy
            'operational': 1.0,    # Primary focus on operations
            'financial': 0.6,      # Some financial considerations
            'technical': 0.7,      # Understands technical operations
            'marketing': 0.4,      # Less marketing focused
            'risk': 0.8           # Risk management is important
        }

        # Initialize the base agent
        super().__init__(profile, expertise, decision_weight)
```

### Step 2: Export the Agent

Add your new agent to `agents/__init__.py`:

```python
from .ceo_agent import CEOAgent
from .cfo_agent import CFOAgent
from .cto_agent import CTOAgent
from .cmo_agent import CMOAgent
from .coo_agent import COOAgent  # Add this line

__all__ = [
    'CEOAgent',
    'CFOAgent',
    'CTOAgent',
    'CMOAgent',
    'COOAgent'  # Add this line
]
```

### Step 3: Customize Decision Weights

Decision weights determine how relevant an agent is for different types of questions:

- **1.0** = Primary expertise (this is the agent's main focus)
- **0.7-0.9** = Secondary expertise (relevant but not primary)
- **0.4-0.6** = Tertiary expertise (some relevance)
- **0.0-0.3** = Minimal expertise (rarely relevant)

Common decision types:
- `strategic`: Long-term planning, vision, company direction
- `operational`: Day-to-day operations, processes, execution
- `financial`: Budgets, ROI, financial analysis
- `technical`: Technology, architecture, engineering
- `marketing`: Customers, brand, market analysis
- `risk`: Risk assessment, compliance, security
- `people`: HR, culture, team management
- `product`: Product development, features, roadmap

---

## Creating a New Council

### Step 1: Define the Council Purpose

Decide what domain or use case your council will serve. Examples:
- **Executive Council**: C-suite executives for business strategy
- **Product Council**: Product managers, designers, engineers for product decisions
- **Security Council**: Security experts for cybersecurity decisions
- **Healthcare Council**: Medical professionals for healthcare decisions
- **Legal Council**: Lawyers, compliance officers for legal matters

### Step 2: Create Council Configuration File

Create a new file in `council/` directory. For example, `council/product_council.py`:

```python
from typing import List, Dict, Any, Optional, Callable
from crewai import Crew, Task
import time

from agents import ProductManagerAgent, UXDesignerAgent, EngineerAgent, DataAnalystAgent
from .decision_framework import DecisionFramework


class ProductCouncil:
    """
    A council of product experts for product-related decisions
    """

    def __init__(self):
        self.decision_framework = DecisionFramework()

        # Initialize agents specific to this council
        self.agents = {
            'pm': ProductManagerAgent(),
            'ux': UXDesignerAgent(),
            'eng': EngineerAgent(),
            'data': DataAnalystAgent()
        }

    def get_agent_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all agents in this council"""
        info = {}
        for agent_type, agent_wrapper in self.agents.items():
            info[agent_type] = {
                'role': agent_wrapper.profile.get('role'),
                'goal': agent_wrapper.profile.get('goal'),
                'expertise': agent_wrapper.get_expertise(),
                'decision_weight': agent_wrapper.get_decision_weight()
            }
        return info

    def deliberate(
        self,
        question: str,
        context: Optional[Dict[str, Any]] = None,
        selected_agents: Optional[List[str]] = None,
        progress_callback: Optional[Callable] = None,
        delay_between_agents: int = 3,
        language: str = "en"
    ) -> str:
        """
        Conduct a council deliberation on a product question

        Args:
            question: The product question or decision
            context: Additional context (user data, metrics, etc.)
            selected_agents: List of agent types to include
            progress_callback: Callback for progress updates
            delay_between_agents: Delay between agent consultations
            language: Response language ("en" or "pt")

        Returns:
            Council's recommendation
        """
        # Use the same deliberation logic as AgentCouncil
        # (See council/orchestrator.py for the full implementation)
        # You can copy the deliberate() method from orchestrator.py
        pass

    def quick_poll(
        self,
        question: str,
        agent_type: str,
        language: str = "en"
    ) -> str:
        """Get quick response from a single agent"""
        if agent_type not in self.agents:
            raise ValueError(f"Unknown agent type: {agent_type}")

        agent_wrapper = self.agents[agent_type]

        # Add language instruction
        language_instruction = ""
        if language == "pt":
            language_instruction = "\n\nIMPORTANTE: Responda em português brasileiro."
        else:
            language_instruction = "\n\nIMPORTANT: Respond in English."

        task = Task(
            description=question + language_instruction,
            agent=agent_wrapper.agent,
            expected_output=f"Response from {agent_wrapper.profile['role']}"
        )

        crew = Crew(
            agents=[agent_wrapper.agent],
            tasks=[task],
            verbose=False
        )

        result = crew.kickoff()
        return str(result)
```

### Step 3: Council Types and Their Agents

Here are some suggested council compositions:

#### 1. Executive Council (Current)
**Use case**: Business strategy, high-level decisions
**Agents**:
- CEO (Chief Executive Officer)
- CFO (Chief Financial Officer)
- CTO (Chief Technology Officer)
- CMO (Chief Marketing Officer)
- COO (Chief Operating Officer) - optional

#### 2. Product Council
**Use case**: Product development, feature decisions, UX
**Agents**:
- Product Manager
- UX/UI Designer
- Software Engineer
- Data Analyst
- Customer Success Manager

#### 3. Security Council
**Use case**: Cybersecurity, compliance, risk assessment
**Agents**:
- Chief Information Security Officer (CISO)
- Security Engineer
- Compliance Officer
- Risk Manager
- Network Architect

#### 4. Healthcare Council
**Use case**: Medical decisions, healthcare advice
**Agents**:
- General Practitioner
- Specialist (Cardiologist, Neurologist, etc.)
- Pharmacist
- Nurse Practitioner
- Healthcare Administrator

#### 5. Marketing Council
**Use case**: Marketing campaigns, brand strategy
**Agents**:
- Brand Strategist
- Content Marketing Manager
- SEO/SEM Specialist
- Social Media Manager
- Growth Hacker

#### 6. Engineering Council
**Use case**: Technical architecture, engineering decisions
**Agents**:
- Solutions Architect
- Backend Engineer
- Frontend Engineer
- DevOps Engineer
- QA Engineer

#### 7. Financial Council
**Use case**: Investment, financial planning
**Agents**:
- Financial Advisor
- Investment Analyst
- Tax Specialist
- Accountant
- Risk Manager

#### 8. Legal Council
**Use case**: Legal matters, contracts, compliance
**Agents**:
- Corporate Lawyer
- Contract Specialist
- Compliance Officer
- Intellectual Property Attorney
- Employment Law Attorney

---

## Adding Translations

### Step 1: Add Agent Translations

Update `translations/en.json`:

```json
{
  "agents": {
    "coo": {
      "role": "Chief Operating Officer",
      "expertise": [
        "Operations management",
        "Process optimization",
        "Supply chain",
        "Quality control",
        "Operational efficiency"
      ]
    },
    "pm": {
      "role": "Product Manager",
      "expertise": [
        "Product strategy",
        "Roadmap planning",
        "Feature prioritization",
        "User research",
        "Stakeholder management"
      ]
    }
  }
}
```

Update `translations/pt.json`:

```json
{
  "agents": {
    "coo": {
      "role": "Diretor de Operações",
      "expertise": [
        "Gestão de operações",
        "Otimização de processos",
        "Cadeia de suprimentos",
        "Controle de qualidade",
        "Eficiência operacional"
      ]
    },
    "pm": {
      "role": "Gerente de Produto",
      "expertise": [
        "Estratégia de produto",
        "Planejamento de roadmap",
        "Priorização de funcionalidades",
        "Pesquisa de usuários",
        "Gestão de stakeholders"
      ]
    }
  }
}
```

### Step 2: Add Council Translations

Update `translations/en.json`:

```json
{
  "council": {
    "executive": {
      "title": "Executive Council",
      "subtitle": "Get strategic advice from your AI executive team",
      "description": "Get comprehensive business advice from C-suite executives.",
      "members": {
        "ceo": "CEO",
        "cfo": "CFO",
        "cto": "CTO",
        "cmo": "CMO"
      }
    },
    "product": {
      "title": "Product Council",
      "subtitle": "Get product insights from your AI product team",
      "description": "Get comprehensive product advice from product experts.",
      "members": {
        "pm": "PM",
        "ux": "UX Designer",
        "eng": "Engineer",
        "data": "Data Analyst"
      }
    }
  }
}
```

---

## Examples

### Example 1: Creating a Simple Agent

```python
# agents/designer_agent.py
from crewai import Agent
from .base_agent import BaseAgent


class DesignerAgent(BaseAgent):
    """UX/UI Designer focused on user experience"""

    def __init__(self):
        profile = {
            'role': 'UX/UI Designer',
            'goal': 'Create beautiful, intuitive, and accessible user experiences',
            'backstory': """You are a senior UX/UI designer with expertise in
            user-centered design, visual design, and accessibility. You prioritize
            user needs while balancing business goals and technical constraints."""
        }

        expertise = [
            'User experience design',
            'Visual design',
            'Accessibility',
            'Prototyping',
            'User research'
        ]

        decision_weight = {
            'strategic': 0.5,
            'operational': 0.6,
            'technical': 0.7,
            'product': 1.0,    # Primary focus
            'marketing': 0.7,
            'user_experience': 1.0  # Primary focus
        }

        super().__init__(profile, expertise, decision_weight)
```

### Example 2: Minimal Council Setup

```python
# council/minimal_council.py
from agents import CEOAgent, CFOAgent


class MinimalCouncil:
    """A simple two-person council"""

    def __init__(self):
        self.agents = {
            'ceo': CEOAgent(),
            'cfo': CFOAgent()
        }

    def get_agent_info(self):
        return {
            agent_type: {
                'role': agent.profile.get('role'),
                'expertise': agent.get_expertise()
            }
            for agent_type, agent in self.agents.items()
        }
```

---

## Best Practices

### 1. Agent Design

- **Be Specific**: Give agents clear, specific roles and expertise
- **Unique Perspectives**: Each agent should bring a unique viewpoint
- **Realistic Backstories**: Write believable professional backgrounds
- **Balanced Weights**: Don't make all weights 1.0 - differentiate agent strengths

### 2. Council Composition

- **3-5 Agents**: Ideal size for most councils (avoids too much overhead)
- **Complementary Skills**: Choose agents with complementary expertise
- **Clear Domain**: Each council should have a clear problem domain
- **Avoid Overlap**: Don't duplicate the same agent in multiple councils

### 3. Translation

- **Complete Coverage**: Translate all agent roles and expertise
- **Cultural Adaptation**: Adapt terminology for different cultures (not just literal translation)
- **Consistency**: Use consistent terminology across all translations

### 4. Testing

Before deploying:
1. Test each agent individually with `quick_poll()`
2. Test the full council with `deliberate()`
3. Test in both languages (EN and PT)
4. Verify that responses match the agent's expertise

---

## Quick Reference: File Locations

- **Agent Implementations**: `agents/[agent_name]_agent.py`
- **Agent Exports**: `agents/__init__.py`
- **Council Implementations**: `council/[council_name]_council.py`
- **English Translations**: `translations/en.json`
- **Portuguese Translations**: `translations/pt.json`
- **Web Integration**: `app.py` (you'll get help with this later)

---

## Next Steps

After creating your agents and council configuration:

1. Test the agents individually
2. Verify the council structure
3. Complete all translations
4. Ask for help integrating into the web app

The web app integration will involve:
- Adding routes in `app.py`
- Creating/updating HTML templates
- Updating the home page to show the new council

---

## Questions?

When you're ready to add your new council to the web app, provide:

1. Council name (e.g., "product", "security", "healthcare")
2. List of agents in the council
3. Council title and description (in both EN and PT)
4. Any custom behavior or features

I'll help you integrate everything into the web application!
