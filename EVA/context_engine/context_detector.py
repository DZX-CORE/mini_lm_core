from EVA.context_engine.plug import InternalPlug
from EVA.context_engine.history_manager import HistoryManager

class ContextDetector:
    def __init__(self, plug):
        self.plug = plug
        self.history = HistoryManager(self.plug)

    def detect_change(self):
        """Detecta mudança de contexto analisando o histórico recente."""
        historico = self.history.get_history(limit=4)
        if len(historico) < 2:
            self.plug.send("contexto_mudou", False)
            return False

        # Extrair conteúdo do usuário mais recente e anterior
        usuario_msgs = [h["conteudo"] for h in historico if h["tipo"] == "usuario"]
        if len(usuario_msgs) < 2:
            self.plug.send("contexto_mudou", False)
            return False

        ultima = usuario_msgs[-1].lower()
        penultima = usuario_msgs[-2].lower()

        # Regras simples: se não compartilharem nenhuma palavra-chave, mudou
        palavras_chave_ultima = set(ultima.split())
        palavras_chave_penultima = set(penultima.split())
        intersecao = palavras_chave_ultima.intersection(palavras_chave_penultima)

        mudou = len(intersecao) < 2  # Heurística básica
        self.plug.send("contexto_mudou", mudou)
        return mudou


# Teste básico
if __name__ == "__main__":
    plug = InternalPlug()
    hist = HistoryManager(plug)
    
    hist.add_entry("usuario", "Qual é o clima hoje?")
    hist.add_entry("eva", "Está ensolarado.")
    hist.add_entry("usuario", "Você sabe quem inventou o avião?")
    hist.add_entry("eva", "Foi Santos Dumont, segundo os brasileiros.")

    detector = ContextDetector(plug)
    mudou = detector.detect_change()

    print("Mudança de contexto detectada:", mudou)
