import pytest
from EVA.internal_research.core_interface import InternalResearchInterface

@pytest.mark.parametrize("entrada", [
    # Entrada vazia
    {},
    # Falta 'topico'
    {"pergunta": "O que é IA?"},
    # 'topico' None
    {"topico": None},
    # 'topico' tipo errado
    {"topico": 12345},
    # Entrada com keys extras não esperadas
    {"topico": "tecnologia", "extra": "valor"},
    # Entrada parcialmente correta, mas com tipo errado
    {"topico": ["lista_invalida"]},
])
def test_internal_research_robust(entrada):
    interface = InternalResearchInterface()
    try:
        interface.receive(entrada)
        resultado = interface.send()
        assert "resultado_formatado" in resultado or "erro" in resultado
        assert isinstance(resultado, dict)
    except Exception as e:
        pytest.fail(f"Falha ao processar entrada: {entrada} -> Erro: {e}")
