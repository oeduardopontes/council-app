# Começando com o Conselho de Agentes IA

Este guia irá ajudá-lo a configurar e executar sua primeira deliberação do conselho de agentes.

## Pré-requisitos

- Python 3.9 ou superior
- Uma chave API da Anthropic Claude

## Passo 1: Configurar o Ambiente

### Criar Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### Instalar Dependências

```bash
pip install -r requirements.txt
```

## Passo 2: Configurar Chaves API

### Copiar Template de Ambiente

```bash
cp .env.example .env
```

### Adicionar Sua Chave API

Edite `.env` e adicione sua chave API da Anthropic:

```env
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
DEFAULT_MODEL=claude-3-haiku-20240307
```

## Passo 3: Executar Seu Primeiro Exemplo

### Exemplo de Decisão Estratégica

```bash
python examples/strategic_decision.py
```

Isso demonstrará uma deliberação completa do conselho com todos os agentes (CEO, CFO, CTO, CMO) discutindo se devem investir em uma plataforma de atendimento ao cliente alimentada por IA.

### Outros Exemplos

**Análise de Expansão de Mercado:**
```bash
python examples/market_analysis.py
```

**Decisão de Arquitetura Técnica:**
```bash
python examples/technical_decision.py
```

## Passo 4: Criar Sua Própria Deliberação

Aqui está um exemplo simples para começar:

```python
from council.orchestrator import AgentCouncil

# Inicializar o conselho
council = AgentCouncil(model_provider="anthropic")

# Fazer uma pergunta
question = "Devemos adotar uma semana de trabalho de 4 dias?"

# Fornecer contexto (opcional)
context = {
    "Tamanho da Equipe": "25 funcionários",
    "Indústria": "Desenvolvimento de software",
    "Produtividade": "Atualmente alta, 95% de taxa de conclusão de sprint"
}

# Obter recomendação do conselho
result = council.deliberate(question, context)

print(result)
```

## Entendendo o Conselho

### Funções dos Agentes

O conselho inclui quatro executivos principais:

1. **CEO** - Visão estratégica e decisões finais
   - Foco: Sucesso a longo prazo, missão da empresa, panorama geral
   - Peso de Decisão: 1.5x

2. **CFO** - Análise financeira e ROI
   - Foco: Custos, receitas, viabilidade financeira
   - Peso de Decisão: 1.2x

3. **CTO** - Viabilidade técnica e inovação
   - Foco: Tecnologia, escalabilidade, implementação
   - Peso de Decisão: 1.2x

4. **CMO** - Insights de mercado e impacto no cliente
   - Foco: Oportunidades de mercado, percepção do cliente, marca
   - Peso de Decisão: 1.0x

### Selecionando Agentes Específicos

Você nem sempre precisa de todos os agentes. Selecione os mais relevantes:

```python
# Para decisões técnicas
result = council.deliberate(
    question="Devemos reescrever nosso app em Rust?",
    selected_agents=['cto', 'cfo', 'ceo']
)

# Para decisões de mercado
result = council.deliberate(
    question="Devemos fazer rebranding do nosso produto?",
    selected_agents=['cmo', 'ceo']
)
```

### Consultas Rápidas

Para perguntas simples a um único agente:

```python
# Perguntar apenas ao CTO
response = council.quick_poll(
    "Quais são as melhores práticas para design de API?",
    agent_type="cto"
)
```

## Personalização

### Modificar Perfis de Agentes

Edite `config/agent_profiles.yaml` para personalizar:
- Funções e objetivos dos agentes
- Histórias de fundo e personalidades
- Áreas de expertise
- Pesos de decisão

### Adicionar Novos Agentes

1. Crie um novo perfil em `config/agent_profiles.yaml`
2. Crie uma nova classe de agente em `agents/`
3. Adicione ao conselho em `council/orchestrator.py`

## Solução de Problemas

### "Chave API não encontrada"
- Certifique-se de que o arquivo `.env` existe e contém sua chave API
- Verifique se a chave começa com o prefixo correto (sk-ant- para Anthropic, sk- para OpenAI)

### Erros de importação
- Ative seu ambiente virtual: `source venv/bin/activate`
- Reinstale as dependências: `pip install -r requirements.txt`

### Respostas dos agentes são muito curtas
- Ajuste `TEMPERATURE` em `.env` (tente 0.7-0.9 para respostas mais criativas)
- Forneça mais contexto detalhado em suas perguntas

## Próximos Passos

- Revise os scripts de exemplo para entender diferentes casos de uso
- Experimente com diferentes perguntas e contextos
- Personalize os perfis de agentes para corresponder às necessidades da sua empresa
- Construa seus próprios fluxos de trabalho de tomada de decisão

## Obtendo Ajuda

- Verifique o README.md principal para detalhes de arquitetura
- Revise os comentários do código em `council/` e `agents/`
- Experimente com os exemplos para entender os padrões

Boa deliberação!
