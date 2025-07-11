from EVA.linguistic_core.plug import InternalPlug

class IntentAnalyzer:
    def __init__(self, plug):
        self.plug = plug
        self.rules = {
            "saudacao": {"oi", "olá", "bom", "boa", "salve"},
            "despedida": {"tchau", "adeus", "até", "valeu"},
            "agradecimento": {"obrigado", "valeu", "agradeço"},
            "pergunta_geral": {"como", "por", "que", "qual", "quando", "onde"},
        }

    def analyze(self):
        tokens = self.plug.receive("tokens") or []
        intent_detected = None
        for token in tokens:
            token_lower = token.lower()
            for intent, keywords in self.rules.items():
                if token_lower in keywords:
                    intent_detected = intent
                    break
            if intent_detected:
                break
        if not intent_detected:
            intent_detected = "indefinida"
        self.plug.send("intent", intent_detected)
        return intent_detected

if __name__ == "__main__":
    plug = InternalPlug()
    plug.send("tokens", ["Oi", "tudo", "bem", "?"])
    analyzer = IntentAnalyzer(plug)
    resultado = analyzer.analyze()
    print("Intenção detectada:", resultado)
    assert resultado == "saudacao", "Erro: intenção incorreta para saudação"
