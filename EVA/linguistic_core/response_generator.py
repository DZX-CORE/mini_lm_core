from EVA.linguistic_core.plug import InternalPlug

class ResponseGenerator:
    def __init__(self, plug):
        self.plug = plug
        self.responses = {
            "saudacao": "Olá! Como posso ajudar você hoje?",
            "pergunta_geral": "Essa é uma ótima pergunta. Deixe-me pensar...",
            "despedida": "Até logo! Foi um prazer conversar com você.",
            "agradecimento": "De nada! Estou aqui para ajudar.",
        }

    def generate(self):
        intent = self.plug.receive("intent")
        resposta = self.responses.get(intent, "Desculpe, não entendi sua intenção.")
        return resposta

if __name__ == "__main__":
    plug = InternalPlug()
    plug.send("intent", "saudacao")
    generator = ResponseGenerator(plug)
    resposta = generator.generate()
    print("Resposta gerada:", resposta)
    assert resposta == "Olá! Como posso ajudar você hoje?", "Erro: Resposta incorreta para saudação"
