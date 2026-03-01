"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Extrai conteúdo legível do ChatPromptTemplate
4. Salva localmente em prompts/raw_prompts.yml

SIMPLIFICADO: Extração de dados legíveis do LangChain ChatPromptTemplate.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

def extract_prompt_content(prompt_template):
    """
    Extrai conteúdo legível de um ChatPromptTemplate.

    Args:
        prompt_template: Objeto ChatPromptTemplate do LangChain

    Returns:
        Dicionário com estrutura legível do prompt
    """
    system_prompt = ""
    user_prompt = ""

    # Extrair mensagens do template
    if hasattr(prompt_template, 'messages'):
        for msg in prompt_template.messages:
            # Extrair SystemMessagePromptTemplate
            if msg.__class__.__name__ == 'SystemMessagePromptTemplate':
                if hasattr(msg.prompt, 'template'):
                    system_prompt = msg.prompt.template

            # Extrair HumanMessagePromptTemplate
            elif msg.__class__.__name__ == 'HumanMessagePromptTemplate':
                if hasattr(msg.prompt, 'template'):
                    user_prompt = msg.prompt.template

    prompt_data = {
        "bug_to_user_story_v1": {
            "description": "Prompt para converter relatos de bugs em User Stories",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "version": "v1",
            "created_at": "2025-01-15",
            "tags": ["bug-analysis", "user-story", "product-management"]
        }
    }

    return prompt_data


def pull_prompts_from_langsmith():
    """
    Conecta ao LangSmith e baixa o prompt de baixa qualidade.

    Retorna:
        True se o arquivo foi salvo com sucesso, False caso contrário.
    """
    prompt_name = "leonanluppi/bug_to_user_story_v1"

    print_section_header("PULL DO PROMPT INICIAL")

    try:
        print(f"   Solicitando prompt: {prompt_name}")
        prompt = hub.pull(prompt_name)
        print("   ✓ Prompt recebido do LangSmith")

        # Extrair conteúdo legível do ChatPromptTemplate
        prompt_data = extract_prompt_content(prompt)

        output_path = "prompts/raw_prompts.yml"
        if save_yaml(prompt_data, output_path):
            print(f"   ✓ Prompt salvo em {output_path}")
            return True
        else:
            print("   ✗ Falha ao salvar o prompt localmente")
            return False
    except Exception as e:
        print(f"✗ Erro ao puxar prompt do LangSmith: {e}")
        return False


def main():
    """Função principal"""
    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return 1

    success = pull_prompts_from_langsmith()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
