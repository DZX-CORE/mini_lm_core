from EVA.external_mentor.plug import InternalPlug

class StyleTranslator:
    def __init__(self, plug):
        self.plug = plug

    def translate(self):
        conhecimento = self.plug.receive("conhecimento_extraido")
        if not conhecimento:
            resposta = "Nenhum conhecimento para traduzir."
        else:
            # Reformulação simples para o estilo da Eva
            resposta = (
                "Aqui está o que eu entendi:\n"
                + conhecimento.replace("Fatos extraídos:", "•")
                + "\nEspero que isso ajude!"
            )
        self.plug.send("resposta_eva", resposta)
        return resposta

# Teste simples
if __name__ == "__main__":
    plug = InternalPlug()
    plug.send("conhecimento_extraido", "Fatos extraídos: água, ferve, 100°C, temperatura, ponto de ebulição")

    translator = StyleTranslator(plug)
    resposta = translator.translate()
    print("Resposta traduzida para estilo Eva:")
    print(resposta)

    resposta_armazenada = plug.receive("resposta_eva")
    print("Resposta armazenada no plug:")
    print(resposta_armazenada)
