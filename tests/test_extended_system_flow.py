import pytest
from EVA.core_orchestrator.system_controller import SystemController

@pytest.fixture
def controller():
    return SystemController()

def test_realistic_flow(controller):
    pergunta = "Qual é a capital da França?"
    controller.send_to_core("linguistic_core", {"mensagem": pergunta})
    resposta_linguistica = controller.receive_from_core("linguistic_core")
    assert isinstance(resposta_linguistica, str)
    assert "ajudar" in resposta_linguistica.lower()

def test_context_engine_status(controller):
    status = controller.get_core_status("context_engine")
    assert isinstance(status, dict)
    assert "estado_contextual" in status

def test_internal_research_flow(controller):
    controller.send_to_core("internal_research", {"topico": "machine learning"})
    resposta = controller.receive_from_core("internal_research")
    assert "resultado_formatado" in resposta
    assert isinstance(resposta["resultado_formatado"], list)

def test_knowledge_filter_flow(controller):
    controller.send_to_core("knowledge_filter", {"entrada": ["fato 1", "fato 2"]})
    resposta = controller.receive_from_core("knowledge_filter")
    assert "filtrados" in resposta
    assert isinstance(resposta["filtrados"], list)

def test_self_inquiry_flow(controller):
    entrada = {
        "pergunta": "Qual é a capital da França?",
        "resposta": "Paris",
        "historico": ["Qual é a capital da Alemanha?"],
        "topico": "geografia"
    }
    controller.send_to_core("self_inquiry", entrada)
    resposta = controller.receive_from_core("self_inquiry")
    assert isinstance(resposta, dict)
    assert "decisao" in resposta
    assert resposta["decisao"] in ["aceita", "rejeita", "indefinido"]

def test_knowledge_base_consulta(controller):
    controller.cores["knowledge_base"].plug.send("memoria_franca", ["Paris é a capital da França."])
    controller.send_to_core("knowledge_base", {"topico": "franca"})
    resposta = controller.receive_from_core("knowledge_base")
    assert "fatos" in resposta
    assert "Paris" in resposta["fatos"][0]

