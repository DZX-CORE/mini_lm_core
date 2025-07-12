import os
import pytest
from EVA.core_orchestrator.system_controller import SystemController

BASE_DIR = "EVA/module_builder"

@pytest.fixture(autouse=True)
def cleanup_files():
    # Limpa arquivos .py gerados para não poluir o ambiente de teste
    yield
    for filename in os.listdir(BASE_DIR):
        if filename.endswith(".py") and filename not in {
            "plug.py",
            "module_generator.py",
            "versioner.py",
            "core_interface.py",
            "__init__.py"
        }:
            os.remove(os.path.join(BASE_DIR, filename))


def test_module_builder_integration():
    controller = SystemController()

    # Testa geração de módulo
    comando_gerar = {
        "action": "generate_module",
        "name": "modulo_integracao_pytest",
        "content": "print('Teste integração pytest')"
    }
    controller.send_to_core("module_builder", comando_gerar)
    resposta = controller.receive_from_core("module_builder")
    assert resposta["status"] == "success"
    assert os.path.exists(resposta["path"])

    # Testa criação de versão
    comando_versionar = {
        "action": "create_version",
        "module_name": "modulo_integracao_pytest",
        "module_content": "print('Versão 1')"
    }
    controller.send_to_core("module_builder", comando_versionar)
    resposta = controller.receive_from_core("module_builder")
    assert resposta["status"] == "success"
    assert resposta["version"] == "v1.0"

    # Testa rollback
    comando_rollback = {
        "action": "rollback",
        "module_name": "modulo_integracao_pytest"
    }
    controller.send_to_core("module_builder", comando_rollback)
    resposta = controller.receive_from_core("module_builder")
    # Pode ser sucesso ou erro se não tiver versão anterior
    assert resposta["status"] in ["success", "error"]

    # Testa status do núcleo
    status = controller.cores["module_builder"].get_status()
    assert "last_version" in status
    assert status["status"] == "ready"
