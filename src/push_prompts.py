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
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_data.get('system_prompt', '')),
            ("human", prompt_data.get('user_prompt', '{bug_report}'))
        ])
        print(f"Push do prompt '{prompt_name}'...")
        url = hub.push(
            prompt_name,
            prompt,
            new_repo_is_public=True,
            api_key=os.getenv("LANGSMITH_API_KEY"),
            api_url=os.getenv("LANGSMITH_ENDPOINT")
        )
        print(f"✅ Push feito {url}")
        return True
    except Exception as e:
        print(f"❌ Erro no push: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt.

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    return validate_prompt_structure(prompt_data)


def main():
    """
    Função principal para validar e fazer push do prompt otimizado.
    """

    print_section_header("Push de prompts")
    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        print("⚠️ Variáveis de ambiente ausentes. Configure antes de continuar.")
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB")
    yaml_path = "../prompts/bug_to_user_story_v2.yml"

    print(f"📂 Carregando prompt de: {yaml_path}")
    data = load_yaml(yaml_path)
    if not data:
        print(f"❌ Falha ao carregar arquivo: {yaml_path}")
        return 1

    # Usa chave raiz se existir, senão assume estrutura compatível
    prompt_data = data.get("bug_to_user_story_v2", data)

    print("🔍 Validando estrutura do prompt...")
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ Prompt inválido:")
        for err in errors:
            print(f"   - {err}")
        return 1
    print("✅ Estrutura válida")

    prompt_name = f"{username}/bug_to_user_story_v2"
    if push_prompt_to_langsmith(prompt_name, prompt_data):
        print("\n🚀 Push concluído com sucesso!")
        return 0

    print("❌ Push falhou")
    return 1


if __name__ == "__main__":
    sys.exit(main())
