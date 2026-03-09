"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
import re
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    @pytest.fixture
    def prompt_data(self):
        """Retorna os dados do prompt otimizado (v2)."""
        file_path = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
        prompts = load_prompts(str(file_path))
        return prompts["bug_to_user_story_v2"]

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        file_path = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
        prompts = load_prompts(str(file_path))

        assert "bug_to_user_story_v2" in prompts
        assert "system_prompt" in prompts["bug_to_user_story_v2"]
        assert prompts["bug_to_user_story_v2"]["system_prompt"].strip() != ""

    def test_prompt_has_role_definition(self, prompt_data):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = prompt_data["system_prompt"].lower()
        role_patterns = [
            "você é um",
            "você é uma",
            "product manager",
            "senior product manager"
        ]

        assert any(pattern in system_prompt for pattern in role_patterns)

    def test_prompt_mentions_format(self, prompt_data):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = prompt_data["system_prompt"].lower()
        format_patterns = [
            "markdown",
            "user story",
            "como um/uma",
            "como um",
            "como uma",
            "critérios de aceitação"
        ]

        assert any(pattern in system_prompt for pattern in format_patterns)

    def test_prompt_has_few_shot_examples(self, prompt_data):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = prompt_data["system_prompt"].lower()
        has_few_shot_sections = "few-shot" in system_prompt or "few shot" in system_prompt
        has_input_output_examples = "entrada" in system_prompt and "saída esperada" in system_prompt

        assert has_few_shot_sections and has_input_output_examples

    def test_prompt_no_todos(self, prompt_data):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompt_text = yaml.safe_dump(prompt_data, allow_unicode=True)
        todo_markers = [
            r"\[TODO\]",
            r"\bTODO\b",
            r"TODO:"
        ]

        assert all(re.search(marker, prompt_text) is None for marker in todo_markers)

    def test_minimum_techniques(self, prompt_data):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = prompt_data.get("techniques_applied", [])

        assert isinstance(techniques, list)
        assert len(techniques) >= 2
        assert validate_prompt_structure(prompt_data)

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])