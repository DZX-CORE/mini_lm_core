from EVA.context_engine.plug import InternalPlug
from EVA.context_engine.history_manager import HistoryManager
from EVA.context_engine.context_detector import ContextDetector
from EVA.context_engine.emotional_context import EmotionalContext

# Simulação da interface padrão universal do núcleo central
class UniversalPlugInterface:
    def receive(self, data): pass
    def send(self): pass
    def get_status(self): pass


class ContextEngineInterface(UniversalPlugInterface):
    def __init__(self):
        self.plug = InternalPlug()
        self.history = HistoryManager(self.plug)
        self.context_detector = ContextDetector(self.plug)
        self.emotional_context = EmotionalContext(self.plug)

    def receive(self, data):
        """Recebe dados de outro núcleo (ex: mensagem do usuário)."""
        self.history.add_entry("usuario", data)
        contexto_mudou = self.context_detector.detect_change()
        emocao = self.emotional_context.analyze()
        self.history.add_entry("eva", f"[Interno] Contexto mudado: {contexto_mudou}, Emoção: {emocao}")

    def send(self):
        """Retorna a última mensagem da Eva (gerada internamente)."""
        historico = self.history.get_history(limit=1)
        if historico and historico[-1]["tipo"] == "eva":
            return historico[-1]["conteudo"]
        return "[Sem resposta gerada]"

    def get_status(self):
        """Retorna uma visão geral do estado atual de contexto."""
        return {
            "historico": self.plug.receive("historico") or [],
            "contexto_mudou": self.plug.receive("contexto_mudou"),
            "emoção": self.plug.receive("emoção")
        }


# Teste simples
if __name__ == "__main__":
    interface = ContextEngineInterface()
    pergunta = "Estou me sentindo muito triste hoje"
    print("?? Recebendo:", pergunta)
    interface.receive(pergunta)

    resposta = interface.send()
    status = interface.get_status()

    print("?? Resposta gerada:", resposta)
    print("?? Status do Núcleo:")
    for k, v in status.items():
        print(f" - {k}: {v}")
