import pytest
from system_controller import SystemController

@pytest.fixture
def controller():
    return SystemController()

def test_sandbox_engine_execution(controller):
    codigo = "print('Teste sandbox_engine integração')"
    controller.send_to_core("sandbox_engine", codigo)
    resposta = controller.receive_from_core("sandbox_engine")
    assert resposta["status_execucao"] == "sucesso"
    assert "Teste sandbox_engine integração" in resposta["saida_sandbox"]
    assert resposta["resultado_validacao"][0] == "aprovado"

def test_module_builder_integration(controller):
    comando = {
        "action": "generate_module",
        "name": "modulo_teste",
        "content": "print('Módulo gerado via teste')"
    }
    controller.send_to_core("module_builder", comando)
    resposta = controller.receive_from_core("module_builder")
    assert resposta is not None
    # Ajuste asserts conforme resposta real do seu module_builder

def test_core_not_found(controller):
    result = controller.send_to_core("core_inexistente", "dados")
    assert result == {"erro": "Núcleo 'core_inexistente' não encontrado."}
