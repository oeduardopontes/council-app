from typing import Dict, Any, List
from crewai import Agent
import yaml
import os


class BaseAgent:
    """Base class for all council agents"""

    def __init__(self, agent_type: str):
        """
        Initialize a base agent

        Args:
            agent_type: Type of agent (ceo, cfo, cto, cmo, analyst)
        """
        self.agent_type = agent_type
        self.profile = self._load_profile()
        self.agent = self._create_agent()

    def _load_profile(self) -> Dict[str, Any]:
        """Load agent profile from configuration"""
        config_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'config',
            'agent_profiles.yaml'
        )

        with open(config_path, 'r') as f:
            profiles = yaml.safe_load(f)

        return profiles.get(self.agent_type, {})

    def _create_agent(self) -> Agent:
        """Create CrewAI agent instance"""
        # Use Claude Haiku - tested and working
        return Agent(
            role=self.profile.get('role', ''),
            goal=self.profile.get('goal', ''),
            backstory=self.profile.get('backstory', ''),
            verbose=True,
            allow_delegation=True,
            llm="anthropic/claude-3-haiku-20240307"
        )

    def get_expertise(self) -> List[str]:
        """Get agent's areas of expertise"""
        return self.profile.get('expertise', [])

    def get_decision_weight(self) -> float:
        """Get agent's decision weight in council deliberation"""
        return self.profile.get('decision_weight', 1.0)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} role='{self.profile.get('role', 'Unknown')}'>"
