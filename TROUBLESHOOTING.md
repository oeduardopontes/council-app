# Guia de Solução de Problemas

## Problema Atual: Erros de Modelo Não Encontrado

Seu Conselho de Agentes IA está configurado corretamente, mas estamos encontrando erros de "modelo não encontrado" ao tentar usar modelos Claude.

### O Que Está Acontecendo

A API da Anthropic está retornando:
```
{"type":"error","error":{"type":"not_found_error","message":"model: claude-3-sonnet-20240229"}}
```

Isso normalmente significa um dos seguintes:

### Causas Possíveis

1. **Chave API Não Tem Acesso ao Modelo**
   - Sua chave API da Anthropic pode não ter acesso aos modelos Claude ainda
   - Novas contas às vezes requerem configuração de faturamento primeiro

2. **Faturamento Não Configurado**
   - Anthropic requer informações de faturamento mesmo para tier gratuito
   - Verifique https://console.anthropic.com/settings/billing

3. **Limitações de Tier da Chave API**
   - Algumas chaves API têm acesso limitado a modelos
   - Verifique seu plano em https://console.anthropic.com/settings/plans

### Soluções

#### Opção 1: Corrigir Acesso Anthropic (Recomendado)

1. Vá para https://console.anthropic.com/
2. Navegue para Configurações → Faturamento
3. Adicione método de pagamento se ainda não foi adicionado
4. Verifique se sua chave API tem acesso ao modelo
5. Gere uma nova chave API se necessário
6. Atualize `.env` com a nova chave


#### Opção 3: Testar Console Anthropic

Antes de executar o conselho, teste sua chave API diretamente:

```python
# test_anthropic.py
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Olá, Claude"}
    ]
)

print(message.content)
```

Execute: `python test_anthropic.py`

Se isso falhar, o problema está com sua conta/chave API da Anthropic.

### Comandos de Verificação Rápida

```bash
# Testar se a chave API está configurada
source venv/bin/activate
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Anthropic:', 'CONFIGURADA' if os.getenv('ANTHROPIC_API_KEY') else 'NÃO CONFIGURADA')"
```

### O Que Está Funcionando

- ✅ Ambiente Python (3.12.12)
- ✅ Todos os pacotes instalados
- ✅ Arquitetura do sistema de agentes
- ✅ Framework CrewAI
- ✅ Chave API detectada
- ❌ Acesso ao modelo (precisa de resolução)

### Próximos Passos

1. Escolha a Opção 1 ou 2 acima
2. Siga os passos para corrigir o acesso à API
3. Execute: `python test_simple.py`
4. Se funcionar, tente: `python demo.py`

### Obtendo Ajuda

- Console Anthropic: https://console.anthropic.com/
- Documentação CrewAI: https://docs.crewai.com/
- Documentação Claude: https://docs.anthropic.com/

### Alternativa: Usar a Arquitetura Sem Executá-la

Mesmo sem acesso à API, você pode:
- Revisar a estrutura do código em `agents/` e `council/`
- Personalizar perfis de agentes em `config/agent_profiles.yaml`
- Entender como o sistema funciona
- Preparar perguntas para quando o acesso à API estiver funcionando

O sistema está construído e pronto - só precisa de acesso válido à API para funcionar!
