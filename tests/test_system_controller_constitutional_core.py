import pytest
from EVA.core_orchestrator.system_controller import SystemController

@pytest.fixture
def controller():
    return SystemController()

def test_constitutional_core_validation_success(controller):
    comando = {
        "action": "validate",
        "response": "Esta é uma resposta para validar pelo núcleo constitucional."
    }
    controller.send_to_core("constitutional_core", comando)
    resultado = controller.receive_from_core("constitutional_core")
    assert resultado is not None
    assert resultado.get("status") == "aprovado"

def test_constitutional_core_validation_fail(controller):
    comando = {
        "action": "validate",
        "response": "Isto é uma mentira."
    }
    controller.send_to_core("constitutional_core", comando)
    resultado = controller.receive_from_core("constitutional_core")
    assert resultado is not None
    assert resultado.get("status") == "negado"

def test_core_name_invalid(controller):
    resposta = controller.send_to_core("non_existent_core", {"action": "test"})
    assert "erro" in resposta

