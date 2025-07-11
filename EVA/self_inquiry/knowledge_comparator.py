from EVA.self_inquiry.plug import InternalPlug

class KnowledgeComparator:
    def __init__(self, plug=None):
        self.plug = plug or InternalPlug()
        # Simula KB simples: tópico -> lista de respostas
        self.knowledge_base = {}

    def compare(self, new_response, topic):
        if not isinstance(new_response, str):
            new_response = str(new_response) if new_response is not None else ""
        if not isinstance(topic, str):
            topic = str(topic) if topic is not None else "unknown"

        old_responses = self.knowledge_base.get(topic, [])

        # Tokenização simples
        new_tokens = set(new_response.lower().split())
        statuses = []

        for old_resp in old_responses:
            if not isinstance(old_resp, str):
                continue
            old_tokens = set(old_resp.lower().split())

            # Detecta redundância (new subset old)
            if new_tokens.issubset(old_tokens):
                statuses.append("redundante")
            # Detecta contradição por palavras-chave diferentes - simplificado
            elif len(new_tokens.intersection(old_tokens)) / max(len(new_tokens), 1) < 0.3:
                statuses.append("contraditório")
            else:
                statuses.append("consistente")

        # Decidir status geral
        if not statuses:
            status = "atualizado"
            # Atualiza KB
            self.knowledge_base.setdefault(topic, []).append(new_response)
        elif "contraditório" in statuses:
            status = "contraditório"
        elif "redundante" in statuses:
            status = "redundante"
        else:
            status = "consistente"

        self.plug.send("status_comparacao", status)
        return status

if __name__ == "__main__":
    plug = InternalPlug()
    comp = KnowledgeComparator(plug)
    print("[TEST] Comparando novo conhecimento...")
    comp.knowledge_base = {
        "geografia": [
            "Paris é a capital da França.",
            "A França é um país europeu."
        ]
    }
    status1 = comp.compare("Paris é a capital da França.", "geografia")
    print(f"[1] Status: {status1}")
    status2 = comp.compare("A França é a capital da Europa.", "geografia")
    print(f"[2] Status: {status2}")
    status3 = comp.compare("Paris é a maior cidade da França.", "geografia")
    print(f"[3] Status: {status3}")
    status4 = comp.compare("Lyon é a capital da França.", "geografia")
    print(f"[4] Status: {status4}")
    assert status4 == "contraditório", "Erro no teste de contradição"
    print("[OK] Testes de comparação de conhecimento passaram com sucesso.")
