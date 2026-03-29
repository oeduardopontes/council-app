# Gerenciamento do Serviço do App do Conselho

## Informações do Serviço

O aplicativo web AI Council está implantado no seu Mac Mini (edumini.local) e funciona como um serviço LaunchAgent que inicia automaticamente na inicialização e continua funcionando 24/7.

**URL de Acesso:** `http://edumini.local:8080`

---

## Comandos de Gerenciamento do Serviço

### Verificar Status do Serviço
```bash
ssh dwardo@edumini.local "launchctl list | grep council"
```

### Parar o Serviço
```bash
ssh dwardo@edumini.local "launchctl stop com.council.app"
```

### Iniciar o Serviço
```bash
ssh dwardo@edumini.local "launchctl start com.council.app"
```

### Reiniciar o Serviço
```bash
ssh dwardo@edumini.local "launchctl stop com.council.app && launchctl start com.council.app"
```

### Descarregar o Serviço (Desabilitar Início Automático)
```bash
ssh dwardo@edumini.local "launchctl unload ~/Library/LaunchAgents/com.council.app.plist"
```

### Carregar o Serviço (Habilitar Início Automático)
```bash
ssh dwardo@edumini.local "launchctl load ~/Library/LaunchAgents/com.council.app.plist"
```

---

## Visualizar Logs

### Logs de Erro
```bash
ssh dwardo@edumini.local "tail -f ~/council-app/error.log"
```

### Logs de Acesso (Requisições HTTP)
```bash
ssh dwardo@edumini.local "tail -f ~/council-app/access.log"
```

### Logs de Saída Padrão
```bash
ssh dwardo@edumini.local "tail -f ~/council-app/stdout.log"
```

### Logs de Erro Padrão
```bash
ssh dwardo@edumini.local "tail -f ~/council-app/stderr.log"
```

---

## Atualizar Código da Aplicação

Se você fizer alterações no código localmente, sincronize-as com o Mac Mini e reinicie:

```bash
# Sincronizar arquivos (da máquina local)
rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '*.pyc' --exclude '.git' --exclude '.DS_Store' /Users/dwardo/Claude/eduardopontes.com/ dwardo@edumini.local:~/council-app/

# Reiniciar o serviço
ssh dwardo@edumini.local "launchctl stop com.council.app && launchctl start com.council.app"
```

---

## Atualizar Dependências Python

Se você atualizar requirements.txt:

```bash
ssh dwardo@edumini.local "cd ~/council-app && source venv/bin/activate && pip install -r requirements.txt"
ssh dwardo@edumini.local "launchctl stop com.council.app && launchctl start com.council.app"
```

---

## Localizações de Arquivos no Mac Mini

- **Diretório da Aplicação:** `/Users/dwardo/council-app/`
- **Configuração LaunchAgent:** `/Users/dwardo/Library/LaunchAgents/com.council.app.plist`
- **Script de Inicialização:** `/Users/dwardo/council-app/start_council.sh`
- **Variáveis de Ambiente:** `/Users/dwardo/council-app/.env`
- **Ambiente Virtual:** `/Users/dwardo/council-app/venv/`

---

## Solução de Problemas

### Serviço Não Está Funcionando
```bash
# Verificar se processos gunicorn estão rodando
ssh dwardo@edumini.local "ps aux | grep gunicorn | grep -v grep"

# Verificar logs de erro
ssh dwardo@edumini.local "tail -50 ~/council-app/error.log"
ssh dwardo@edumini.local "tail -50 ~/council-app/stderr.log"
```

### Testar App Manualmente
```bash
ssh dwardo@edumini.local
cd ~/council-app
source venv/bin/activate
python app.py
```

### Recarregar LaunchAgent Após Mudanças de Configuração
```bash
ssh dwardo@edumini.local "launchctl unload ~/Library/LaunchAgents/com.council.app.plist && launchctl load ~/Library/LaunchAgents/com.council.app.plist"
```

---

## Pontos de Acesso

- **Da rede local:** `http://edumini.local:8080`
- **Do próprio Mac Mini:** `http://localhost:8080`
- **API de Verificação de Saúde:** `http://edumini.local:8080/api/health`
- **API de Agentes:** `http://edumini.local:8080/api/agents`

---

## Backup do Arquivo .env

Suas chaves API estão armazenadas em `/Users/dwardo/council-app/.env`. Certifique-se de fazer backup:

```bash
ssh dwardo@edumini.local "cat ~/council-app/.env" > council-app-env-backup.txt
```
