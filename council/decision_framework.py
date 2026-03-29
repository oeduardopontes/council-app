from typing import List, Dict, Any
from enum import Enum


class DecisionType(Enum):
    """Types of decisions the council can make"""
    STRATEGIC = "strategic"
    FINANCIAL = "financial"
    TECHNICAL = "technical"
    MARKET = "market"
    OPERATIONAL = "operational"
    GENERAL = "general"


class DecisionFramework:
    """Framework for structuring council deliberations"""

    @staticmethod
    def structure_question(question: str, context: Dict[str, Any] = None) -> str:
        """
        Structure a question for council deliberation

        Args:
            question: The main question or decision to be made
            context: Additional context information

        Returns:
            Formatted question with context
        """
        structured = f"# Deliberação do Conselho\n\n## Pergunta\n{question}\n\n"

        if context:
            structured += "## Contexto\n"
            for key, value in context.items():
                structured += f"- **{key}**: {value}\n"
            structured += "\n"

        structured += """## Análise Necessária

Por favor, forneça sua perspectiva considerando:
1. Principais oportunidades e riscos
2. Impacto na sua área de responsabilidade
3. Requisitos e restrições de recursos
4. Considerações de prazo e implementação
5. Sua recomendação (Apoio Fortemente / Apoio / Neutro / Contra / Fortemente Contra)

Seja específico, orientado por dados quando possível, e destaque quaisquer preocupações ou dependências.
"""
        return structured

    @staticmethod
    def create_synthesis_prompt(agent_responses: List[Dict[str, str]]) -> str:
        """
        Create a prompt for synthesizing agent responses into a final recommendation

        Args:
            agent_responses: List of agent responses with role and content

        Returns:
            Synthesis prompt
        """
        synthesis = "# Resumo da Deliberação do Conselho\n\n"
        synthesis += "O conselho deliberou sobre a pergunta. Aqui estão as perspectivas:\n\n"

        for response in agent_responses:
            role = response.get('role', 'Desconhecido')
            content = response.get('content', '')
            synthesis += f"## {role}\n{content}\n\n"

        synthesis += """---

Com base nas perspectivas acima, forneça um resumo executivo abrangente que inclua:

1. **Áreas de Consenso**: Onde os executivos concordam?
2. **Principais Preocupações**: Quais são os principais riscos ou desafios identificados?
3. **Visões Divergentes**: Onde as opiniões diferem e por quê?
4. **Recomendação**: Qual é a recomendação geral do conselho?
5. **Itens de Ação**: Se seguir em frente, quais são os próximos passos?
6. **Métricas de Sucesso**: Como esta decisão deve ser medida?

Forneça uma recomendação clara e acionável que equilibre todas as perspectivas.
"""
        return synthesis

    @staticmethod
    def classify_decision(question: str) -> DecisionType:
        """
        Classify the type of decision being made

        Args:
            question: The question or decision to classify

        Returns:
            DecisionType enum
        """
        question_lower = question.lower()

        keywords = {
            DecisionType.STRATEGIC: ['strategy', 'vision', 'direction', 'pivot', 'expand', 'market entry'],
            DecisionType.FINANCIAL: ['budget', 'cost', 'revenue', 'investment', 'funding', 'roi', 'financial'],
            DecisionType.TECHNICAL: ['technology', 'technical', 'architecture', 'platform', 'engineering', 'infrastructure'],
            DecisionType.MARKET: ['market', 'customer', 'marketing', 'brand', 'competition', 'positioning'],
            DecisionType.OPERATIONAL: ['process', 'operations', 'efficiency', 'workflow', 'hiring', 'team']
        }

        for decision_type, keywords_list in keywords.items():
            if any(keyword in question_lower for keyword in keywords_list):
                return decision_type

        return DecisionType.GENERAL
