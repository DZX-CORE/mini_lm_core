from EVA.external_mentor.plug import InternalPlug

class MentorConnector:
    def __init__(self, plug):
        self.plug = plug
        self.mentor_name = None
        self.mentores_simulados = {
            "OpenAI": "Resposta do OpenAI simulada.",
            "HuggingFace": "Resposta do HuggingFace simulada.",
            "LocalModel": "Resposta do modelo local simulada."
        }

    def connect(self, mentor_name):
        if mentor_name in self.mentores_simulados:
            self.mentor_name = mentor_name
            self.plug.send("mentor", mentor_name)
            return True
        else:
            return False

    def ask(self, question):
        if not self.mentor_name:
            resposta = "Nenhum mentor conectado."
        else:
            # Resposta simulada básica
            resposta = f"[{self.mentor_name}] Pergunta: {question} -> {self.mentores_simulados[self.mentor_name]}"
        self.plug.send("resposta_mentor", resposta)
        return resposta

# Teste simples
if __name__ == "__main__":
    plug = InternalPlug()
    connector = MentorConnector(plug)

    conectado = connector.connect("OpenAI")
    print(f"Conectado ao mentor OpenAI? {conectado}")

    resposta = connector.ask("Qual o sentido da vida?")
    print("Resposta do mentor:", resposta)

    # Verificando dado salvo no plug
    resposta_armazenada = plug.receive("resposta_mentor")
    print("Resposta armazenada no plug:", resposta_armazenada)
