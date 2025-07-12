class InternalPlug:
    def __init__(self):
        self._storage = {}

    def send(self, key, value):
        """Armazena temporariamente um valor associado a uma chave."""
        self._storage[key] = value

    def receive(self, key):
        """Recupera o valor associado à chave especificada."""
        return self._storage.get(key)

# Teste simples
if __name__ == "__main__":
    plug = InternalPlug()
    plug.send("filtro_resultado", {"relevante": True, "nível": 0.95})
    resultado = plug.receive("filtro_resultado")
    print("Teste InternalPlug (knowledge_filter):", resultado)
