class InternalPlug:
    def __init__(self):
        self.data = {}

    def send(self, key, value):
        self.data[key] = value

    def receive(self, key):
        return self.data.get(key)

if __name__ == "__main__":
    plug = InternalPlug()
    plug.send("teste", "sucesso")
    recebido = plug.receive("teste")
    assert recebido == "sucesso", "Erro no InternalPlug: valor recebido diferente do esperado."
    print("✅  Teste passou: InternalPlug envia e recebe corretamente.")
