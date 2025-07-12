from EVA.constitutional_core.plug import InternalPlug

class RuleBase:
    def __init__(self, plug):
        self.plug = plug
        self.rules = []

    def load_rules(self):
        self.rules = [
            "Ser útil",
            "Não mentir",
            "Evitar conteúdo ilegal"
        ]
        self.plug.send("regras_constitucionais", self.rules)

    def add_rule(self, rule):
        self.rules.append(rule)
        self.plug.send("regras_constitucionais", self.rules)

    def get_rules(self):
        return self.rules


# Teste simples
def test_rule_base():
    plug = InternalPlug()
    rule_base = RuleBase(plug)

    rule_base.load_rules()
    regras = rule_base.get_rules()
    assert "Ser útil" in regras
    assert "Não mentir" in regras

    rule_base.add_rule("Promover transparência")
    assert "Promover transparência" in rule_base.get_rules()

    plug_regras = plug.receive("regras_constitucionais")
    assert isinstance(plug_regras, list)
    assert "Ser útil" in plug_regras
    assert "Promover transparência" in plug_regras

    print("✅  Teste passou: RuleBase carrega, adiciona e retorna regras corretamente.")

if __name__ == "__main__":
    test_rule_base()
