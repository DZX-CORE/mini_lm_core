from EVA.context_engine.plug import InternalPlug
from EVA.context_engine.history_manager import HistoryManager

class EmotionalContext:
    def __init__(self, plug):
        self.plug = plug
        self.history = HistoryManager(self.plug)

        # Dicionários básicos de palavras por emoção
        self.emotion_keywords = {
            "alegre": {"feliz", "ótimo", "maravilha", "bom", "legal", "content"},
            "triste": {"triste", "chateado", "deprimido", "mal", "cansado"},
            "urgente": {"urgente", "agora", "rápido", "imediato", "socorro"},
            "neutro": set()  # fallback
        }

    def analyze(self):
        """Analisa o estado emocional da última fala do usuário."""
        historico = self.history.get_history(limit=3)
        ultimas_msgs = [h["conteudo"] for h in historico if h["tipo"] == "usuario"]

        if not ultimas_msgs:
            self.plug.send("emoção", "neutro")
            return "neutro"

        texto = ultimas_msgs[-1].lower()
        tokens = set(texto.split())

        for emocao, palavras in self.emotion_keywords.items():
            if palavras & tokens:
                self.plug.send("emoção", emocao)
                return emocao

        # Nenhuma emoção detectada: neutro
        self.plug.send("emoção", "neutro")
        return "neutro"


# Teste básico
if __name__ == "__main__":
    plug = InternalPlug()
    hist = HistoryManager(plug)

    hist.add_entry("usuario", "Estou muito feliz com o resultado!")
    hist.add_entry("eva", "Que bom saber disso!")

    ec = EmotionalContext(plug)
    detected = ec.analyze()

    print("Emoção detectada:", detected)
