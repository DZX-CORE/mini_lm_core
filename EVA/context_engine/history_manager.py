from EVA.context_engine.plug import InternalPlug

class HistoryManager:
    def __init__(self, plug):
        self.plug = plug
        if self.plug.receive("historico") is None:
            self.plug.send("historico", [])

    def add_entry(self, tipo, conteudo):
        """Adiciona uma entrada ao histórico da conversa."""
        historico = self.plug.receive("historico")
        historico.append({"tipo": tipo, "conteudo": conteudo})
        self.plug.send("historico", historico)

    def get_history(self, limit=5):
        """Retorna as últimas N entradas do histórico."""
        historico = self.plug.receive("historico")
        return historico[-limit:]


# Teste básico
if __name__ == "__main__":
    plug = InternalPlug()
    history = HistoryManager(plug)

    history.add_entry("usuario", "Olá, tudo bem?")
    history.add_entry("eva", "Olá! Em que posso ajudar?")
    history.add_entry("usuario", "Qual o clima hoje?")
    history.add_entry("eva", "Está ensolarado em São Paulo.")
    history.add_entry("usuario", "Obrigado!")
    history.add_entry("eva", "De nada!")

    ultimas = history.get_history(limit=3)
    print("Últimas 3 mensagens:")
    for entrada in ultimas:
        print(entrada)
