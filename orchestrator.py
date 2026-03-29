from typing import List, Dict, Any, Optional, Callable
from crewai import Crew, Task
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
import os
import time
from dotenv import load_dotenv

from agents import CEOAgent, CFOAgent, CTOAgent, CMOAgent
from .decision_framework import DecisionFramework, DecisionType


class AgentCouncil:
    """
    Orchestrates a council of AI agents for collaborative decision-making
    """

    def __init__(self, model_provider: str = "anthropic", model_name: Optional[str] = None):
        """
        Initialize the Agent Council

        Args:
            model_provider: "anthropic" or "openai"
            model_name: Specific model name (optional, uses defaults)
        """
        load_dotenv()

        self.model_provider = model_provider
        self.decision_framework = DecisionFramework()

        # Initialize agents (CrewAI will auto-detect models from environment)
        self.agents = self._initialize_agents()

    def _initialize_llm(self, provider: str, model_name: Optional[str]):
        """Initialize the language model"""
        if provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

            model = model_name or os.getenv("DEFAULT_MODEL", "claude-3-5-sonnet-20241022")
            return ChatAnthropic(
                model=model,
                api_key=api_key,
                temperature=float(os.getenv("TEMPERATURE", "0.7"))
            )

        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")

            model = model_name or "gpt-4-turbo-preview"
            return ChatOpenAI(
                model=model,
                api_key=api_key,
                temperature=float(os.getenv("TEMPERATURE", "0.7"))
            )

        else:
            raise ValueError(f"Unsupported model provider: {provider}")

    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all council agents"""
        return {
            'ceo': CEOAgent(),
            'cfo': CFOAgent(),
            'cto': CTOAgent(),
            'cmo': CMOAgent()
        }

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
        Conduct a council deliberation on a question or decision

        Args:
            question: The question or decision to deliberate
            context: Additional context information
            selected_agents: List of agent types to include (default: all)
            progress_callback: Function to call with progress updates
            delay_between_agents: Seconds to wait between each agent (default: 3)
            language: Language for responses ("en" or "pt")

        Returns:
            Council's deliberation result and recommendation
        """
        # Select agents for this deliberation
        if selected_agents:
            active_agents = {k: v for k, v in self.agents.items() if k in selected_agents}
        else:
            active_agents = self.agents

        # Structure the question with language instruction
        structured_question = self.decision_framework.structure_question(question, context)

        # Add language instruction to the question
        language_instruction = ""
        if language == "pt":
            language_instruction = "\n\nIMPORTANTE: Responda em português brasileiro (Portuguese from Brazil)."
        else:
            language_instruction = "\n\nIMPORTANT: Respond in English."

        structured_question = structured_question + language_instruction

        # Process agents sequentially with progress updates
        total_agents = len(active_agents)
        agent_responses = []

        print(f"\n{'='*80}")
        print(f"DELIBERAÇÃO DO CONSELHO EM SESSÃO")
        print(f"{'='*80}\n")
        print(f"Pergunta: {question}\n")
        print(f"Agentes consultando: {total_agents}\n")

        for idx, (agent_type, agent_wrapper) in enumerate(active_agents.items(), 1):
            # Update progress
            if progress_callback:
                progress_callback({
                    'current': idx,
                    'total': total_agents,
                    'agent': agent_wrapper.profile['role'],
                    'status': 'processing'
                })

            print(f"[{idx}/{total_agents}] Consultando {agent_wrapper.profile['role']}...")

            # Create task for this agent
            task = Task(
                description=structured_question,
                agent=agent_wrapper.agent,
                expected_output=f"Análise detalhada e recomendação da perspectiva de {agent_wrapper.profile['role']}"
            )

            # Execute single agent task
            crew = Crew(
                agents=[agent_wrapper.agent],
                tasks=[task],
                verbose=False
            )

            try:
                result = crew.kickoff()
                agent_responses.append({
                    'role': agent_wrapper.profile['role'],
                    'content': str(result)
                })
                print(f"✓ {agent_wrapper.profile['role']} respondeu\n")

                # Update progress
                if progress_callback:
                    progress_callback({
                        'current': idx,
                        'total': total_agents,
                        'agent': agent_wrapper.profile['role'],
                        'status': 'completed'
                    })

            except Exception as e:
                print(f"✗ Erro ao consultar {agent_wrapper.profile['role']}: {e}\n")
                agent_responses.append({
                    'role': agent_wrapper.profile['role'],
                    'content': f"Erro ao processar resposta: {str(e)}"
                })

            # Delay between agents (except after the last one)
            if idx < total_agents:
                print(f"Aguardando {delay_between_agents} segundos antes do próximo agente...\n")
                time.sleep(delay_between_agents)

        # Synthesize all responses
        print(f"\n{'='*80}")
        print(f"SINTETIZANDO RECOMENDAÇÕES")
        print(f"{'='*80}\n")

        synthesis_prompt = self.decision_framework.create_synthesis_prompt(agent_responses)
        synthesis_prompt = synthesis_prompt + language_instruction

        # Use CEO to synthesize (or first available agent)
        synthesizer = self.agents.get('ceo', list(self.agents.values())[0])

        expected_output = "Executive summary with final recommendation" if language == "en" else "Resumo executivo consolidado com recomendação final"

        synthesis_task = Task(
            description=synthesis_prompt,
            agent=synthesizer.agent,
            expected_output=expected_output
        )

        synthesis_crew = Crew(
            agents=[synthesizer.agent],
            tasks=[synthesis_task],
            verbose=False
        )

        final_result = synthesis_crew.kickoff()

        print(f"\n{'='*80}")
        print(f"DELIBERAÇÃO COMPLETA")
        print(f"{'='*80}\n")

        return str(final_result)

    def quick_poll(
        self,
        question: str,
        agent_type: str = 'ceo',
        language: str = "en"
    ) -> str:
        """
        Get a quick response from a single agent

        Args:
            question: The question to ask
            agent_type: Which agent to ask (ceo, cfo, cto, cmo)
            language: Language for responses ("en" or "pt")

        Returns:
            Agent's response
        """
        if agent_type not in self.agents:
            raise ValueError(f"Unknown agent type: {agent_type}")

        agent_wrapper = self.agents[agent_type]

        # Add language instruction
        language_instruction = ""
        if language == "pt":
            language_instruction = "\n\nIMPORTANTE: Responda em português brasileiro (Portuguese from Brazil)."
        else:
            language_instruction = "\n\nIMPORTANT: Respond in English."

        task = Task(
            description=question + language_instruction,
            agent=agent_wrapper.agent,
            expected_output=f"Brief response from {agent_wrapper.profile['role']}"
        )

        crew = Crew(
            agents=[agent_wrapper.agent],
            tasks=[task],
            verbose=True
        )

        result = crew.kickoff()
        return str(result)

    def get_agent_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all agents in the council"""
        info = {}
        for agent_type, agent_wrapper in self.agents.items():
            info[agent_type] = {
                'role': agent_wrapper.profile.get('role'),
                'goal': agent_wrapper.profile.get('goal'),
                'expertise': agent_wrapper.get_expertise(),
                'decision_weight': agent_wrapper.get_decision_weight()
            }
        return info
