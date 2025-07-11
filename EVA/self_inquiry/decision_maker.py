from EVA.self_inquiry.plug import InternalPlug

class DecisionMaker:
    def __init__(self, plug=None):
        self.plug = plug or InternalPlug()

    def make_decision(self):
        similaridade = self.plug.receive("similaridade")
        status = self.plug.receive("status_comparacao")

        # Validação simples
        if not isinstance(similaridade, (int, float)):
            similaridade = 0.0
        if not isinstance(status, str):
            status = ""

        decision = "criar_novo"
        if similaridade > 0.7 and status == "consistente":
            decision = "usar_existente"
        elif status in ["atualizado", "redundante"]:
            decision = "atualizar"

        self.plug.send("decisao", decision)
        return decision

if __name__ == "__main__":
    plug = InternalPlug()
    plug.send("similaridade", 0.8)
    plug.send("status_comparacao", "consistente")
    dm = DecisionMaker(plug)
    print("[TEST] Tomando decisão...")
    decision = dm.make_decision()
    print(f"[DECISÃO] {decision}")
    assert decision in ["usar_existente", "atualizar", "criar_novo"]
    print("[OK] Teste do módulo DecisionMaker passou com sucesso.")
