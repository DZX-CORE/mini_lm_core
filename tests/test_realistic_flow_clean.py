import pytest

@pytest.fixture
def controller():
    from EVA.core_orchestrator.system_controller import SystemController
    ctrl = SystemController()
    yield ctrl

def test_realistic_flow_clean(controller):
    # Pergunta básica para núcleo linguístico
    pergunta = "Qual é a capital da França?"
    controller.send_to_core("linguistic_core", pergunta)
    resposta_linguistica = controller.receive_from_core("linguistic_core")
    assert isinstance(resposta_linguistica, str) and len(resposta_linguistica) > 0

    # Passar resultado para knowledge_base
    controller.send_to_core("knowledge_base", {"consulta": resposta_linguistica})
    resposta_kb = controller.receive_from_core("knowledge_base")
    assert resposta_kb is not None

    # Passar dados para knowledge_filter
    controller.send_to_core("knowledge_filter", {"entrada": resposta_kb})
    resposta_filter = controller.receive_from_core("knowledge_filter")
    assert resposta_filter is not None

    # Usar núcleo self_inquiry para introspecção simples
    inquiry_data = {
        "pergunta": pergunta,
        "resposta": resposta_filter,
        "historico": [],
        "topico": "geografia"
    }
    controller.send_to_core("self_inquiry", inquiry_data)
    resposta_self_inquiry = controller.receive_from_core("self_inquiry")
    assert resposta_self_inquiry is not None

    # Internal research pode ser chamado com tópico
    controller.send_to_core("internal_research", {"topico": "capitais"})
    resposta_research = controller.receive_from_core("internal_research")
    assert resposta_research is not None

    # Finalmente, validar status do context engine
    status = controller.get_core_status("context_engine")
    assert status is not None
    assert "status" in status

