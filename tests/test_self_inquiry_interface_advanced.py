import pytest
from EVA.self_inquiry.core_interface import SelfInquiryInterface

@pytest.mark.parametrize("caso", [
    {
        "entrada": {
            "pergunta": "Qual é a capital da França?",
            "resposta": "Paris é a capital da França.",
            "historico": ["Qual é a cidade mais importante da França?"],
            "topico": "geografia"
        },
        "esperado": {
            "decisao": {"usar_existente", "atualizar"},
        }
    },
    {
        "entrada": {
            "pergunta": "Onde fica Lyon?",
            "resposta": "Lyon é a capital da França.",
            "historico": ["Qual é a cidade mais importante da França?"],
            "topico": "geografia"
        },
        "esperado": {
            "decisao": {"criar_novo"},
            "status_comparacao": {"contraditório"}
        }
    },
    {
        "entrada": {
            "pergunta": "Paris ainda é a capital da França?",
            "resposta": "Paris é a capital da França.",
            "historico": ["Qual é a capital da França?"],
            "topico": "geografia"
        },
        "esperado": {
            "decisao": {"usar_existente", "atualizar"},
            "status_comparacao": {"redundante", "consistente"}
        }
    },
    {
        "entrada": {
            "pergunta": "Qual cidade é mais populosa na França?",
            "resposta": "Paris é a cidade mais populosa da França.",
            "historico": ["Qual a capital da França?"],
            "topico": "geografia"
        },
        "esperado": {
            "decisao": {"usar_existente", "atualizar", "criar_novo"},
        }
    },
])
def test_self_inquiry_advanced_flow(caso):
    interface = SelfInquiryInterface()
    interface.receive(caso["entrada"])
    resultado = interface.send()

    # Debug prints (opcional)
    print("\n[DEBUG] Entrada:", caso["entrada"])
    print("[DEBUG] Resultado:", resultado)

    # Verifica decisão
    if "decisao" in caso["esperado"]:
        assert resultado["decisao"] in caso["esperado"]["decisao"]

    # Verifica status_comparacao
    if "status_comparacao" in caso["esperado"]:
        assert resultado["status_comparacao"] in caso["esperado"]["status_comparacao"]
