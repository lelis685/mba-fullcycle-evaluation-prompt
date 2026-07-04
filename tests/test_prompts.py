"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils  import validate_prompt_structure

PROMPT_PATH = str(Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml")


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_prompt_data() -> dict:
    """Retorna o dict interno do prompt (desempacota a chave raiz se necessário)."""
    data = load_prompts(PROMPT_PATH)
    return data.get("bug_to_user_story_v2", data)


class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se 'system_prompt' existe e não está vazio."""
        prompt = get_prompt_data()
        assert "system_prompt" in prompt, "❌ Campo 'system_prompt' não encontrado"
        assert prompt["system_prompt"].strip(), "❌ Campo 'system_prompt' está vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: Product Manager)."""
        system_prompt = get_prompt_data().get("system_prompt", "").lower()
        role_keywords = ["product manager", "gerente de produto", "você é um", "você é uma"]
        assert any(k in system_prompt for k in role_keywords), (
            f"❌ Nenhuma persona encontrada. Esperado algum de: {role_keywords}"
        )

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato User Story ou Markdown."""
        system_prompt = get_prompt_data().get("system_prompt", "").lower()
        format_keywords = ["user story", "como um", "critérios de aceitação", "markdown", "as a"]
        assert any(k in system_prompt for k in format_keywords), (
            f"❌ Nenhuma referência ao formato encontrada. Esperado algum de: {format_keywords}"
        )

    def test_prompt_has_examples(self):
        """Verifica se o prompt contém exemplos (Few-shot)."""
        system_prompt = get_prompt_data().get("system_prompt", "")
        example_keywords = ["exemplo", "input:", "output:"]
        assert any(k.lower() in system_prompt.lower() for k in example_keywords), (
            "❌ Nenhum exemplo encontrado. Adicione pelo menos um Input/Output."
        )

    def test_prompt_no_todos(self):
        """Garante que não há [TODO] no texto."""
        full_text = str(get_prompt_data())
        assert "[TODO]" not in full_text, "❌ Marcador [TODO] encontrado — remova antes de publicar"

    def test_minimum_techniques(self):
        """Verifica se pelo menos 2 técnicas foram listadas."""
        techniques = get_prompt_data().get("techniques_applied", [])
        assert len(techniques) >= 2, (
            f"❌ Mínimo de 2 técnicas requeridas. Encontradas: {len(techniques)} → {techniques}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
