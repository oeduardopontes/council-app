#!/usr/bin/env python3
"""
Teste simples da API Anthropic
"""
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"API Key configurada: {'Sim' if api_key else 'Não'}")
print(f"Primeiros caracteres: {api_key[:15] if api_key else 'N/A'}...")

if api_key:
    try:
        client = anthropic.Anthropic(api_key=api_key)
        print("\nTestando API...")

        # Testar modelos disponíveis
        models_to_test = [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-sonnet-20240620",
            "claude-3-sonnet-20240229",
            "claude-3-opus-20240229"
        ]

        working_model = None
        for model in models_to_test:
            try:
                print(f"\nTestando modelo: {model}")
                message = client.messages.create(
                    model=model,
                    max_tokens=100,
                    messages=[
                        {"role": "user", "content": "Diga olá em português em uma frase curta."}
                    ]
                )
                working_model = model
                break
            except Exception as e:
                print(f"  ❌ Erro com {model}: {str(e)[:80]}...")
                continue

        if working_model:
            print(f"\n✅ API funcionando com modelo: {working_model}")
            print(f"Resposta: {message.content[0].text}")
            print(f"\n📝 Use este modelo no seu .env:")
            print(f"DEFAULT_MODEL={working_model}")
        else:
            print("\n❌ Nenhum modelo funcionou!")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
else:
    print("\n❌ Chave API não encontrada!")
