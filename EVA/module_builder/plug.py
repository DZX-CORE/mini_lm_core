class InternalPlug:
    def __init__(self):
        self.data = {}

    def send(self, key, value):
        self.data[key] = value

    def receive(self, key):
        return self.data.get(key)


# ?? Teste simples de envio e recebimento
def test_internal_plug():
    plug = InternalPlug()
    plug.send("mensagem", "Olá, EVA!")
    resultado = plug.receive("mensagem")
    assert resultado == "Olá, EVA!", f"Erro: esperado 'Olá, EVA!', obtido {resultado}"
    print("✅ Teste passou: InternalPlug envia e recebe corretamente.")


if __name__ == "__main__":
    test_internal_plug()
