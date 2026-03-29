# Conselho de Agentes IA

Um sistema de tomada de decisão multi-agente alimentado por IA, projetado para fornecer insights e recomendações estratégicas de negócios através de deliberação colaborativa de agentes.

## Visão Geral

Este sistema cria um conselho de agentes alimentados por IA, cada um representando diferentes funções executivas (CEO, CFO, CTO, CMO). Estes agentes colaboram para analisar cenários de negócios, debater opções e fornecer recomendações abrangentes.

## Funcionalidades

- Múltiplos agentes de IA especializados com personalidades e expertise distintas
- Framework de tomada de decisão colaborativa
- Recomendações estratégicas e analíticas
- Perfis de agentes fáceis de configurar
- Construído com CrewAI para orquestração robusta multi-agente

## Configuração

1. **Criar ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

2. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar ambiente:**
   ```bash
   cp .env.example .env
   # Edite .env e adicione sua chave API da Anthropic
   ```

## Uso

Veja o diretório `examples/` para casos de uso de exemplo.

```python
from council.orchestrator import AgentCouncil

council = AgentCouncil()
result = council.deliberate("Devemos expandir para o mercado europeu?")
print(result)
```

## Estrutura do Projeto

```
├── agents/          # Implementações de agentes individuais
├── council/         # Lógica de orquestração do conselho
├── config/          # Perfis de agentes e configurações
├── examples/        # Casos de uso de exemplo
└── requirements.txt # Dependências Python
```

## Licença

MIT
