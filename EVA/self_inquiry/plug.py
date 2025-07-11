class InternalPlug:
    def __init__(self):
        self._storage = {}

    def send(self, key, value):
        if not isinstance(key, str):
            raise TypeError("Chave deve ser string.")
        if value is None:
            raise ValueError("Valor não pode ser None.")
        self._storage[key] = value

    def receive(self, key):
        if not isinstance(key, str):
            raise TypeError("Chave deve ser string.")
        return self._storage.get(key, None)

if __name__ == "__main__":
    plug = InternalPlug()
    print("[TEST] Enviando chave 'state' com valor 'active'...")
    plug.send("state", "active")
    print("[TEST] Recebendo chave 'state'...")
    val = plug.receive("state")
    assert val == "active", "Erro no teste"
    print("[OK] Teste passou com sucesso.")
