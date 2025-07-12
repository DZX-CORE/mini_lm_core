class InternalPlug:
    def __init__(self):
        self._data = {}

    def send(self, key, value):
        self._data[key] = value

    def receive(self, key):
        return self._data.get(key)


# Teste simples
def test_internal_plug():
    plug = InternalPlug()
    plug.send("direito_fundamental", "liberdade de expressão")
    assert plug.receive("direito_fundamental") == "liberdade de expressão"
    assert plug.receive("inexistente") is None
    print("✅  Teste passou: InternalPlug envia e recebe corretamente.")

if __name__ == "__main__":
    test_internal_plug()
