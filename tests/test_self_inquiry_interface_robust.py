import pytest
from EVA.self_inquiry.core_interface import SelfInquiryInterface

@pytest.mark.parametrize("entrada", [
    # Falta 'historico'
    {
        "pergunta": "O que é IA?",
        "resposta": "Inteligência Artificial é o campo da ciência que estuda agentes inteligentes.",
        "topico": "tecnologia"
    },
    # 'historico' vazio
    {
        "pergunta": "O que é IA?",
        "resposta": "Inteligência Artificial é o campo da ciência que estuda agentes inteligentes.",
        "historico": [],
        "topico": "tecnologia"
    },
    # Falta 'resposta'
    {
        "pergunta": "O que é IA?",
        "historico": ["Defina IA."],
        "topico": "tecnologia"
    },
    # Falta 'topico'
    {
        "pergunta": "O que é IA?",
        "resposta": "Campo da ciência que estuda agentes inteligentes.",
        "historico": ["Defina IA."]
    },
    # Valores None
    {
        "pergunta": None,
        "resposta": None,
        "historico": None,
        "topico": None
    },
    # Tipos errados
    {
        "pergunta": 123,
        "resposta": 456,
        "historico": "isto não é lista",
        "topico": 789
    }
])
def test_self_inquiry_robust(entrada):
    interface = SelfInquiryInterface()
    try:
        interface.receive(entrada)
        resultado = interface.send()
        # Validações básicas
        assert "similaridade" in resultado
        assert 0 <= resultado["similaridade"] <= 1
        assert "status_comparacao" in resultado
        assert isinstance(resultado["status_comparacao"], str)
        assert "decisao" in resultado
        assert isinstance(resultado["decisao"], str)
    except Exception as e:
        pytest.fail(f"Falha ao processar entrada: {entrada} -> Erro: {e}")
