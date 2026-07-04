"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Fluxo:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull do prompt do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml
"""

import sys
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """
    Faz pull do prompt base do LangSmith Hub e salva localmente.
    """
    prompt_name = "lelis685/bug_to_user_story_v2"
    output_path = "prompts/bug_to_user_story_v1.yml"

    print(f"🔗 Conectando ao LangSmith Hub...")
    prompt = hub.pull(prompt_name)
    print(f"📥 Prompt '{prompt_name}' carregado com sucesso")

    system_content, user_content = "", ""
    if hasattr(prompt, "messages"):
        for message in prompt.messages:
            template = getattr(message.prompt, "template", str(message))
            if "System" in type(message).__name__:
                system_content = template
            elif "Human" in type(message).__name__ or "User" in type(message).__name__:
                user_content = template
    elif hasattr(prompt, "template"):
        user_content = prompt.template

    prompt_data = {
        "bug_to_user_story_v1": {
            "description": "Prompt para converter relatos de bugs em User Stories",
            "system_prompt": system_content,
            "user_prompt": user_content,
            "version": "v1",
            "created_at": "2025-01-15",
            "tags": ["bug-analysis", "user-story", "product-management"],
            "source": f"LangSmith Hub: {prompt_name}",
        }
    }

    print(f"💾 Salvando em: {output_path}")
    save_yaml(prompt_data, output_path)


def main():
    """Função principal"""
    pull_prompts_from_langsmith()

if __name__ == "__main__":
    sys.exit(main())
