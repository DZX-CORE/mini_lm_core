from EVA.core_orchestrator.system_controller import SystemController

def test_orchestrator_basic():
    controller = SystemController()

    # Testa envio para constitutional_core e resposta
    comando_const = {"action": "validate", "response": "Teste para validar."}
    controller.send_to_core("constitutional_core", comando_const)
    resposta_const = controller.receive_from_core("constitutional_core")
    assert resposta_const is not None
    assert "status" in resposta_const
    assert resposta_const["status"] in ["aprovado", "negado"]

    # Testa envio para module_builder e resposta
    comando_mod = {"action": "generate_module", "name": "mod_test", "content": "print('teste')"}
    controller.send_to_core("module_builder", comando_mod)
    resposta_mod = controller.receive_from_core("module_builder")
    assert resposta_mod is not None
    assert resposta_mod.get("status") == "success"
    assert "path" in resposta_mod
