import pytest
from EVA.core_orchestrator.system_controller import SystemController

@pytest.fixture
def controller():
    return SystemController()

def test_send_to_core_basic(controller):
    data = {"topico": "água"}
    resposta = controller.send_to_core("knowledge_base", data)
    assert isinstance(resposta, dict)
    assert "fatos" in resposta or "message" in resposta

def test_broadcast_all_cores(controller):
    data = {"pergunta": "Qual a capital da França?"}
    respostas = controller.broadcast(data)
    assert isinstance(respostas, dict)
    assert "linguistic_core" in respostas
    assert isinstance(respostas["linguistic_core"], (dict, str))

def test_send_to_core_self_inquiry(controller):
    entrada = {
        "pergunta": "Qual é a capital da França?",
        "resposta": "Paris",
        "historico": ["Qual é a capital da França?"],
        "topico": "geografia"
    }
    resultado = controller.send_to_core("self_inquiry", entrada)
    assert "decisao" in resultado or "erro" not in resultado
