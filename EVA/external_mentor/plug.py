class InternalPlug:
    def __init__(self):
        self.data = {}

    def send(self, key, value):
        self.data[key] = value

    def receive(self, key):
        return self.data.get(key)

# Teste simples
if __name__ == "__main__":
    plug = InternalPlug()
    plug.send("mensagem", "Olá, External Mentor!")
    resultado = plug.receive("mensagem")
    print("Resultado recebido:", resultado)
