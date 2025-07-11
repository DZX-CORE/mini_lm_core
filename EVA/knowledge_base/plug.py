class InternalPlug:
    def __init__(self):
        self.data = {}

    def send(self, key, value):
        """Armazena temporariamente um valor com a chave especificada."""
        self.data[key] = value

    def receive(self, key):
        """Recupera o valor associado à chave especificada."""
        return self.data.get(key)

# Teste simples
if __name__ == "__main__":
    plug = InternalPlug()
    plug.send("fato", {"entidade": "água", "propriedade": "molhada"})
    resultado = plug.receive("fato")
    print("Plug funcionando:", resultado)
