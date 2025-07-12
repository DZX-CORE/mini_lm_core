from .plug import InternalPlug
from .isolation_runner import IsolationRunner
from .validator import Validator

class SandboxEngineInterface:
    """
    Interface externa do núcleo Sandbox Engine.
    Recebe código para execução e validação segura antes de responder.
    """

    def __init__(self):
        self.plug = InternalPlug()
        self.runner = IsolationRunner(self.plug)
        self.validator = Validator(self.plug)
        self.ultimo_resultado = None

    def receive(self, data):
        """
        Recebe dados de outro núcleo.
        Espera receber um código para executar na sandbox.
        """
        # Envia código para o plug
        self.plug.send("codigo_entrada", data)

        # Executa o código na sandbox
        self.runner.run(data)

        # Valida o resultado da execução
        resultado_validacao = self.validator.validate()

        self.ultimo_resultado = resultado_validacao
        return None  # receive não retorna nada diretamente

    def send(self):
        """
        Envia a resposta/resultados para outro núcleo.
        Retorna uma estrutura com status e saída do código.
        """
        saida = self.plug.receive("saida_sandbox")
        status = self.plug.receive("status_execucao")
        resultado_validacao = self.plug.receive("resultado_validacao")

        return {
            "saida_sandbox": saida,
            "status_execucao": status,
            "resultado_validacao": resultado_validacao,
        }

    def get_status(self):
        """
        Retorna estado atual do núcleo.
        """
        return {
            "ultimo_resultado": self.ultimo_resultado
        }


# ===============================
# ?? Teste simples executável
# ===============================
def test_core_interface():
    interface = SandboxEngineInterface()

    codigo_teste = "print('Teste completo sandbox')"
    interface.receive(codigo_teste)

    resposta = interface.send()
    print("Resposta do núcleo:", resposta)

    status = interface.get_status()
    print("Status atual:", status)

if __name__ == "__main__":
    test_core_interface()
