from EVA.core_orchestrator.system_controller import SystemController

def test_system_controller_with_versioning_system():
    controller = SystemController()
    comando = {
        "action": "log_change",
        "module": "mod_test",
        "old_version": "v1.0",
        "new_version": "v1.1",
        "description": "Teste de registro via orquestrador"
    }
    controller.send_to_core("versioning_system", comando)

    resposta = controller.receive_from_core("versioning_system")
    assert resposta is not None
