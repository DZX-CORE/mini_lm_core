from EVA.self_inquiry.plug import InternalPlug

class SimilarityChecker:
    def __init__(self, plug=None):
        self.plug = plug or InternalPlug()

    def check_similarity(self, nova_pergunta, historico):
        # Validação e sanitização
        if not isinstance(nova_pergunta, str):
            nova_pergunta = str(nova_pergunta) if nova_pergunta is not None else ""
        if not isinstance(historico, list):
            historico = []

        if not historico:
            self.plug.send("similaridade", 0.0)
            return 0.0

        nova_tokens = set(nova_pergunta.lower().split())
        max_sim = 0.0
        for pergunta in historico:
            if not isinstance(pergunta, str):
                continue
            hist_tokens = set(pergunta.lower().split())
            common = nova_tokens.intersection(hist_tokens)
            sim = len(common) / max(len(nova_tokens), 1)
            if sim > max_sim:
                max_sim = sim

        self.plug.send("similaridade", max_sim)
        return max_sim

if __name__ == "__main__":
    plug = InternalPlug()
    print("[TEST] Verificando similaridade com histórico...")
    sim_checker = SimilarityChecker(plug)
    sim = sim_checker.check_similarity("Qual é a capital da França?", ["Qual a capital da França?", "Qual é a maior cidade?"])
    print(f"[RESULTADO] Similaridade: {sim}")
    assert 0 <= sim <= 1, "Erro no teste de similaridade"
    print("[OK] Teste de similaridade passou com sucesso.")
