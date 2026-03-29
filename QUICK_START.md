# Guia de Início Rápido

## Como Usar Seu Conselho Executivo de IA

### Método 1: Executar a Demo Interativa

A maneira mais fácil de ver seu conselho em ação:

```bash
source venv/bin/activate
python demo.py
```

Isso mostrará uma deliberação completa do conselho sobre uma decisão empresarial de exemplo.

---

## Método 2: Usar os Exemplos Pré-construídos

Execute qualquer um dos scripts de exemplo:

```bash
# Decisão estratégica sobre investimento em IA
python examples/strategic_decision.py

# Análise de expansão de mercado
python examples/market_analysis.py

# Decisão de arquitetura técnica
python examples/technical_decision.py
```

---

## Método 3: Escrever Seu Próprio Script

Crie um novo arquivo Python (ex: `minha_decisao.py`):

```python
from council.orchestrator import AgentCouncil

# Inicializar o conselho
council = AgentCouncil(model_provider="anthropic")

# Faça sua pergunta
question = "Devemos contratar mais 5 engenheiros ou terceirizar o desenvolvimento?"

# Forneça contexto (opcional)
context = {
    "Equipe Atual": "10 engenheiros",
    "Orçamento": "R$ 2,5 milhões",
    "Prazo": "Precisamos entregar em 6 meses",
    "Complexidade do Projeto": "Alta - construindo nova plataforma"
}

# Obtenha a recomendação do conselho
result = council.deliberate(question, context)

print(result)
```

Então execute:
```bash
python minha_decisao.py
```

---

## Método 4: Perguntas Rápidas a um Único Agente

Pergunte a apenas um executivo para consultoria rápida:

```python
from council.orchestrator import AgentCouncil

council = AgentCouncil(model_provider="anthropic")

# Pergunte ao CFO sobre finanças
response = council.quick_poll(
    "Quais são as métricas financeiras chave para uma startup SaaS?",
    agent_type="cfo"
)
print(response)

# Pergunte ao CTO sobre tecnologia
response = council.quick_poll(
    "Devemos usar arquitetura de microsserviços ou monolito?",
    agent_type="cto"
)
print(response)

# Pergunte ao CMO sobre marketing
response = council.quick_poll(
    "Quais canais de marketing funcionam melhor para SaaS B2B?",
    agent_type="cmo"
)
print(response)

# Pergunte ao CEO para consultoria estratégica
response = council.quick_poll(
    "Como priorizamos entre crescimento e lucratividade?",
    agent_type="ceo"
)
print(response)
```

---

## Método 5: Seleção Personalizada de Agentes

Inclua apenas agentes específicos para certas decisões:

```python
from council.orchestrator import AgentCouncil

council = AgentCouncil(model_provider="anthropic")

# Para decisões técnicas, consulte CTO, CFO e CEO
result = council.deliberate(
    question="Devemos migrar para Kubernetes?",
    context={"Configuração Atual": "Instâncias EC2", "Tamanho da Equipe": "3 engenheiros DevOps"},
    selected_agents=['cto', 'cfo', 'ceo']  # Pular CMO para isso
)

# Para decisões de marketing, consulte CMO e CEO
result = council.deliberate(
    question="Devemos fazer rebranding do nosso produto?",
    selected_agents=['cmo', 'ceo']  # Pular CTO e CFO
)
```

---

## Que Perguntas Você Pode Fazer?

Seu conselho pode ajudar com:

### Decisões Estratégicas
- "Devemos pivotar nosso modelo de negócio?"
- "É o momento certo para levantar financiamento Série A?"
- "Devemos expandir internacionalmente?"

### Decisões Financeiras
- "Devemos aumentar os preços em 20%?"
- "Vale a pena investir R$ 2,5 milhões em marketing?"
- "Devemos fazer bootstrap ou buscar capital de risco?"

### Decisões Técnicas
- "Devemos reconstruir nosso app em React Native?"
- "É hora de contratar um engenheiro DevOps dedicado?"
- "Devemos construir ou comprar um sistema CRM?"

### Decisões de Mercado/Crescimento
- "Devemos focar em clientes enterprise ou PME?"
- "Vale a pena expor em grandes conferências?"
- "Devemos lançar um plano freemium?"

---

## Dicas para Melhores Resultados

1. **Seja Específico**: Forneça contexto e restrições claras
2. **Inclua Números**: Orçamento, prazo, tamanho da equipe, métricas
3. **Declare as Consequências**: O que acontece se você escolher errado?
4. **Faça Perguntas Reais**: O conselho funciona melhor em decisões genuínas
5. **Use Contexto**: Quanto mais informação de fundo, melhor a consultoria

---

## O Que Acontece Durante a Deliberação?

Quando você chama `council.deliberate()`:

1. Cada agente recebe a pergunta e o contexto
2. Agentes analisam de sua perspectiva (CEO=estratégia, CFO=finanças, etc.)
3. Agentes podem delegar tarefas uns aos outros se necessário
4. Você recebe uma recomendação abrangente que equilibra todos os pontos de vista

Isso normalmente leva 30-60 segundos dependendo da complexidade da pergunta.

---

## Próximos Passos

1. **Comece com a demo**: `python demo.py`
2. **Experimente um exemplo**: `python examples/strategic_decision.py`
3. **Faça sua própria pergunta**: Crie um script com sua decisão empresarial real
4. **Personalize agentes**: Edite `config/agent_profiles.yaml` para ajustar personalidades

Boa deliberação!
