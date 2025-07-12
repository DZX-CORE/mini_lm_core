class InternalPlug:
    """
    Classe responsável pela comunicação interna entre os módulos do núcleo Sandbox Engine.
    Armazena dados temporariamente utilizando um dicionário.
    """

    def __init__(self):
        self.data = {}

    def send(self, key, value):
        """
        Armazena um valor com a chave especificada.
        """
        self.data[key] = value

    def receive(self, key):
        """
        Retorna o valor associado à chave, se existir.
        """
        return self.data.get(key)

# ===============================
# ?? Teste Simples (executável)
# ===============================
def test_internal_plug():
    plug = InternalPlug()
    plug.send("mensagem", "Olá, EVA!")
    resultado = plug.receive("mensagem")
    print("Resultado recebido:", resultado)

if __name__ == "__main__":
    test_internal_plug()
