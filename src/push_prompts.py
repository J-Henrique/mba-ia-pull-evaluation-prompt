"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header
from langchain_core.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.prompts.prompt import PromptTemplate

load_dotenv()

def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt.

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    # Verificar campos obrigatórios
    required_fields = ['description', 'system_prompt', 'version']
    for field in required_fields:
        if field not in prompt_data:
            errors.append(f"Campo obrigatório faltando: {field}")

    # Verificar se system_prompt não está vazio
    system_prompt = prompt_data.get('system_prompt', '').strip()
    if not system_prompt:
        errors.append("system_prompt está vazio")

    # Verificar se há TODOs remanescentes
    if '[TODO]' in system_prompt:
        errors.append("system_prompt ainda contém [TODO]s não preenchidos")

    # Verificar técnicas aplicadas
    techniques = prompt_data.get('techniques_applied', [])
    if not techniques or len(techniques) < 2:
        errors.append(f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques) if techniques else 0}")

    return (len(errors) == 0, errors)


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt (ex: "username/bug_to_user_story_v2")
        prompt_data: Dados do prompt (dict com system_prompt, user_prompt, metadata)

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        # Reconstruir object ChatPromptTemplate a partir do YAML
        system_prompt = prompt_data.get('system_prompt', '')
        user_prompt = prompt_data.get('user_prompt', '')

        system_template = PromptTemplate(
            template=system_prompt,
            input_variables=[]
        )
        human_template = PromptTemplate(
            template=user_prompt,
            input_variables=['bug_report']
        )

        system_msg = SystemMessagePromptTemplate(prompt=system_template)
        human_msg = HumanMessagePromptTemplate(prompt=human_template)

        prompt_template = ChatPromptTemplate(
            messages=[system_msg, human_msg],
            input_variables=['bug_report'],
            tags=prompt_data.get('tags', []),
            metadata={
                "version": prompt_data.get('version', 'v2'),
                "techniques": prompt_data.get('techniques_applied', []),
                "description": prompt_data.get('description', ''),
                "optimizations": prompt_data.get('optimizations', [])
            }
        )

        # Fazer push para LangSmith
        print(f"\n   Fazendo push do prompt para LangSmith Hub: {prompt_name}")
        hub.push(prompt_name, object=prompt_template, new_repo_is_public=True)
        print(f"   ✓ Prompt '{prompt_name}' foi publicado com sucesso (PÚBLICO)")

        return True

    except Exception as e:
        error_msg = str(e).lower()
        print(f"\n✗ Erro ao fazer push: {e}")

        if "already exists" in error_msg or "conflict" in error_msg:
            print("   → O prompt já existe. Use uma versão diferente ou delete antes de fazer push novamente.")
        elif "permission" in error_msg or "unauthorized" in error_msg:
            print("   → Erro de autenticação. Verifique se LANGSMITH_API_KEY está correta no .env")
        else:
            print("   → Verifique sua conexão e credenciais do LangSmith.")

        return False


def main():
    """Função principal"""
    print_section_header("PUSH DOS PROMPTS OTIMIZADOS")

    # Validar credenciais
    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        return 1

    # Carregar prompt otimizado
    yaml_path = "prompts/bug_to_user_story_v2.yml"
    prompt_data = load_yaml(yaml_path)

    if not prompt_data:
        print(f"✗ Não foi possível carregar {yaml_path}")
        return 1

    # Extrair dados do topo-level da estrutura
    if isinstance(prompt_data, dict) and 'bug_to_user_story_v2' in prompt_data:
        prompt_content = prompt_data['bug_to_user_story_v2']
    else:
        print("✗ Estrutura do YAML inválida. Esperado: bug_to_user_story_v2: {...}")
        return 1

    # Validar prompt
    is_valid, errors = validate_prompt(prompt_content)
    if not is_valid:
        print("\n✗ Validação do prompt falhou:")
        for error in errors:
            print(f"   - {error}")
        return 1

    print("\n✓ Prompt carregado e validado")

    # Fazer push
    username = os.getenv("USERNAME_LANGSMITH_HUB")
    prompt_name = f"{username}/bug_to_user_story_v2"

    success = push_prompt_to_langsmith(prompt_name, prompt_content)

    if success:
        print(f"\n✓ ======================================")
        print(f"✓ Prompt '{prompt_name}' foi publicado com sucesso!")
        print(f"✓ Acesse em: https://smith.langchain.com/prompts")
        print(f"✓ ======================================\n")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
