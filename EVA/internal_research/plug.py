class InternalPlug:
    def __init__(self):
        self._storage = {}

    def send(self, key, value):
        """Armazena temporariamente o valor associado à chave."""
        self._storage[key] = value

    def receive(self, key):
        """Recupera o valor associado à chave, ou None se não existir."""
        return self._storage.get(key, None)


if __name__ == "__main__":
    plug = InternalPlug()
    print("[TEST] Enviando chave 'example' com valor 123...")
    plug.send("example", 123)
    print("[TEST] Recebendo chave 'example'...")
    val = plug.receive("example")
    print(f"[RESULT] Valor recebido: {val}")
    assert val == 123, "Teste falhou: valor recebido diferente do enviado."
    print("[OK] Teste passou com sucesso.")
