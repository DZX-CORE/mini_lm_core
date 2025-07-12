from EVA.constitutional_core.plug import InternalPlug
from EVA.constitutional_core.rule_base import RuleBase
from EVA.constitutional_core.response_validator import ResponseValidator

class ConstitutionalCoreInterface:
    def __init__(self):
        self.plug = InternalPlug()
        self.rule_base = RuleBase(self.plug)
        self.validator = ResponseValidator(self.plug)
        self.last_result = None
        self.last_action = None
        self.rule_base.load_rules()

    def receive(self, data):
        action = data.get("action")
        self.last_action = action

        if action == "validate":
            response = data.get("response", "")
            self.last_result = self.validator.validate(response)

        elif action == "get_rules":
            regras = self.rule_base.get_rules()
            self.last_result = regras

        elif action == "add_rule":
            nova_regra = data.get("rule")
            if nova_regra:
                self.rule_base.add_rule(nova_regra)
                self.last_result = self.rule_base.get_rules()

    def send(self):
        return self.last_result

    def get_status(self):
        return {
            "status": "ok",
            "ultima_acao": self.last_action,
            "ultima_validacao": self.last_result,
            "total_regras": len(self.rule_base.get_rules())
        }


# Teste simples
def test_constitutional_interface():
    interface = ConstitutionalCoreInterface()

    # Teste de validação de resposta
    interface.receive({"action": "validate", "response": "Baixe por pirataria!"})
    resultado = interface.send()
    assert resultado["status"] == "negado"

    # Teste de envio de regras
    interface.receive({"action": "get_rules"})
    regras = interface.send()
    assert isinstance(regras, list)
    assert "Não mentir" in regras

    # Teste de adição de regra
    interface.receive({"action": "add_rule", "rule": "Evitar ambiguidade"})
    interface.receive({"action": "get_rules"})
    regras = interface.send()
    assert "Evitar ambiguidade" in regras

    print("✅  Teste passou: ConstitutionalCoreInterface funciona corretamente.")

if __name__ == "__main__":
    test_constitutional_interface()
