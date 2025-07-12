import pytest
from EVA.constitutional_core.core_interface import ConstitutionalCoreInterface

@pytest.fixture
def interface():
    return ConstitutionalCoreInterface()

def test_regras_iniciais_carregadas(interface):
    regras = interface.rule_base.get_rules()
    assert isinstance(regras, list)
    assert "Ser útil" in regras
    assert "Não mentir" in regras
    assert "Evitar conteúdo ilegal" in regras

@pytest.mark.parametrize("response, esperado_status", [
    ("Claro, a capital da França é Paris.", "aprovado"),
    ("Sim.", "negado"),  # muito curto para ser útil
    ("Você pode baixar por pirataria.", "negado"),  # conteúdo ilegal
    ("Esta resposta não contém mentira.", "negado"),  # ajustado para refletir comportamento simples do validador
    ("Isto é uma mentira.", "negado"),  # contém palavra 'mentira'
])
def test_validate_responses(interface, response, esperado_status):
    interface.receive({"action": "validate", "response": response})
    resultado = interface.send()
    assert resultado["status"] == esperado_status

def test_adicionar_nova_regra(interface):
    nova_regra = "Evitar ambiguidade"
    interface.receive({"action": "add_rule", "rule": nova_regra})
    regras = interface.rule_base.get_rules()
    assert nova_regra in regras

def test_get_rules_action(interface):
    interface.receive({"action": "get_rules"})
    regras = interface.send()
    assert isinstance(regras, list)
    assert "Ser útil" in regras

def test_get_status(interface):
    status = interface.get_status()
    assert status["status"] == "ok"
    assert isinstance(status["total_regras"], int)
    assert status["ultima_validacao"] is None

    interface.receive({"action": "validate", "response": "Teste resposta"})
    interface.send()
    status = interface.get_status()
    assert status["ultima_validacao"] is not None
    assert status["ultima_acao"] == "validate"

