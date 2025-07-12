import pytest
from EVA.sandbox_engine.plug import InternalPlug
from EVA.sandbox_engine.isolation_runner import IsolationRunner
from EVA.sandbox_engine.validator import Validator
from EVA.sandbox_engine.core_interface import SandboxEngineInterface

@pytest.fixture
def plug():
    return InternalPlug()

@pytest.fixture
def runner(plug):
    return IsolationRunner(plug)

@pytest.fixture
def validator(plug):
    return Validator(plug)

@pytest.fixture
def interface():
    return SandboxEngineInterface()

def test_internal_plug_basic(plug):
    plug.send("chave", "valor")
    assert plug.receive("chave") == "valor"
    assert plug.receive("nao_existe") is None

def test_isolation_runner_success(runner, plug):
    code = "print('ok')"
    runner.run(code)
    assert plug.receive("saida_sandbox") == "ok"
    assert plug.receive("status_execucao") == "sucesso"

def test_isolation_runner_error(runner, plug):
    code = "raise Exception('fail')"
    runner.run(code)
    assert "fail" in plug.receive("saida_sandbox")
    assert plug.receive("status_execucao") == "erro"

def test_validator_approved(validator, plug):
    plug.send("saida_sandbox", "resultado ok")
    plug.send("status_execucao", "sucesso")
    resultado = validator.validate()
    assert resultado[0] == "aprovado"

def test_validator_rejected_error(validator, plug):
    plug.send("saida_sandbox", "erro")
    plug.send("status_execucao", "erro")
    resultado = validator.validate()
    assert resultado[0] == "rejeitado"

def test_validator_rejected_empty_output(validator, plug):
    plug.send("saida_sandbox", "")
    plug.send("status_execucao", "sucesso")
    resultado = validator.validate()
    assert resultado[0] == "rejeitado"

def test_core_interface_flow_success(interface):
    code = "print('teste completo')"
    interface.receive(code)
    resposta = interface.send()
    assert resposta["saida_sandbox"] == "teste completo"
    assert resposta["status_execucao"] == "sucesso"
    assert resposta["resultado_validacao"][0] == "aprovado"

def test_core_interface_flow_failure(interface):
    code = "raise Exception('erro intencional')"
    interface.receive(code)
    resposta = interface.send()
    assert resposta["status_execucao"] == "erro"
    assert resposta["resultado_validacao"][0] == "rejeitado"

def test_core_interface_get_status(interface):
    code = "print('status test')"
    interface.receive(code)
    status = interface.get_status()
    assert status["ultimo_resultado"][0] == "aprovado"
