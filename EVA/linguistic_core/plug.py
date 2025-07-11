class InternalPlug:
    def __init__(self):
        self.data = {}

    def send(self, key, value):
        """Armazena temporariamente um valor com a chave especificada."""
        self.data[key] = value

    def receive(self, key):
        """Recupera o valor associado à chave especificada."""
        return self.data.get(key)

# Teste básico de funcionalidade
if __name__ == "__main__":
    plug = InternalPlug()
    plug.send("mensagem", "Olá, Eva!")
    resultado = plug.receive("mensagem")
    print("Plug funcionando:", resultado)
    assert resultado == "Olá, Eva!", "Erro: valor recebido diferente do enviado"
