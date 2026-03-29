# Entendendo Erros de Sobrecarga da API

## 🔄 O que é o erro "Overloaded"?

O erro `overloaded_error` da Anthropic significa que os servidores da API Claude estão temporariamente com alto volume de requisições e não conseguem processar sua solicitação no momento.

**Mensagem que você verá:**
```
A API do Claude está temporariamente sobrecarregada.
Por favor, aguarde alguns segundos e tente novamente. ⏳
```

---

## ✅ Como o Sistema Lida com Isso

O sistema agora está configurado para:

1. **Detectar automaticamente** erros de sobrecarga
2. **Mostrar mensagem clara** em português explicando o problema
3. **Sugerir ação** (aguardar alguns segundos)
4. **Manter o estado** - você não perde sua pergunta

---

## 🛠️ O que Fazer Quando Isso Acontecer

### Opção 1: Aguardar e Tentar Novamente (Recomendado)
1. Aguarde **10-30 segundos**
2. Clique em "Iniciar Deliberação" novamente
3. O sistema tentará processar sua pergunta

### Opção 2: Usar Menos Agentes
Em vez de consultar todos os agentes, selecione apenas um ou dois:
- **CEO apenas** - Para decisões estratégicas gerais
- **CFO + CEO** - Para decisões financeiras
- **CTO + CEO** - Para decisões técnicas
- **CMO + CEO** - Para decisões de marketing

Menos agentes = processamento mais rápido = menos chance de sobrecarga

### Opção 3: Simplificar a Pergunta
Perguntas mais curtas e diretas são processadas mais rapidamente:

**❌ Evite:**
```
"Preciso que o conselho analise detalhadamente todos os aspectos
financeiros, técnicos, estratégicos e de mercado sobre se devemos
expandir para 15 novos países considerando..."
```

**✅ Prefira:**
```
"Devemos expandir internacionalmente? Orçamento: R$ 2 milhões"
```

---

## 📊 Quando Acontece Mais Frequentemente

Os erros de sobrecarga são mais comuns:
- **Horários de pico** (geralmente horário comercial nos EUA)
- **Múltiplas deliberações simultâneas**
- **Perguntas muito complexas** que requerem muito processamento
- **Consulta a muitos agentes ao mesmo tempo**

---

## 🎯 Melhores Práticas

### 1. Use Rate Limiting
O sistema já tem um limite de 30 segundos entre requisições. Respeite esse limite!

### 2. Planeje Suas Perguntas
Prepare suas perguntas com antecedência e faça uma de cada vez.

### 3. Escolha os Agentes Certos
Não precisa consultar todos sempre:
- **Decisão financeira?** → CFO + CEO
- **Questão técnica?** → CTO + CEO
- **Estratégia de mercado?** → CMO + CEO
- **Visão geral?** → CEO apenas

### 4. Horários Alternativos
Considere usar o sistema em horários de menor movimento:
- **Madrugada/manhã cedo** (Brasil)
- **Fins de semana**
- **Fora do horário comercial dos EUA**

---

## 🔧 Configuração Atual do Sistema

### Tratamento de Erros Implementado

O sistema agora detecta e informa sobre:

✅ **Sobrecarga da API** (503)
- Mensagem: "A API do Claude está temporariamente sobrecarregada..."

✅ **Limite de Taxa** (429)
- Mensagem: "Limite de taxa atingido. Por favor, aguarde um momento..."

✅ **Erro de Autenticação** (401)
- Mensagem: "Erro de autenticação. Por favor, verifique a chave API..."

✅ **Erro de Configuração** (500)
- Mensagem: "Erro de configuração da API..."

✅ **Timeout** (504)
- Mensagem: "A deliberação demorou muito tempo..."

### Rate Limiting
- **Intervalo mínimo**: 30 segundos entre deliberações
- **Por IP**: Cada usuário tem seu próprio contador
- **Mensagem amigável**: Informa quanto tempo falta

---

## 📈 Monitoramento

### Como Verificar se a API Está Funcionando

```bash
# Teste rápido da API
ssh dwardo@edumini.local "cd ~/council-app && source venv/bin/activate && python test_api.py"

# Verificar logs de erro
ssh dwardo@edumini.local "tail -20 ~/council-app/error.log"

# Status do serviço
curl http://edumini.local:8080/api/health
```

---

## 💡 Dicas Extras

### Se os Erros Persistirem

1. **Verifique o status da Anthropic**
   - https://status.anthropic.com/

2. **Considere upgrade do plano**
   - Planos pagos têm prioridade e menos sobrecarga
   - Mais requisições por minuto

3. **Use cache local**
   - Salve respostas importantes
   - Revise antes de fazer nova pergunta similar

### Exemplo de Uso Eficiente

```javascript
// ✅ BOM - Uma pergunta, poucos agentes
Pergunta: "Devemos lançar o produto em Q1?"
Agentes: CEO, CFO
Tempo: ~5-10 segundos

// ⚠️ PODE SOBRECARREGAR - Muitos agentes
Pergunta: "Análise completa de expansão internacional"
Agentes: CEO, CFO, CTO, CMO, Analista
Contexto: 10+ itens
Tempo: ~30-60 segundos (mais chance de sobrecarga)
```

---

## 📞 Suporte

Se os erros de sobrecarga forem muito frequentes:

1. **Verifique seu plano Anthropic**: https://console.anthropic.com/settings/plans
2. **Considere upgrade**: Mais capacidade e prioridade
3. **Ajuste uso**: Espaçar deliberações, menos agentes

---

**Atualizado**: 2025-11-08
**Sistema**: Conselho de Agentes IA v1.0
**LLM**: Claude Haiku (Anthropic)
