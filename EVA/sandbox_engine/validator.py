from .plug import InternalPlug

class Validator:
    """
    Analisa a saída do código executado na sandbox e decide se está aprovado ou rejeitado.
    """

    def __init__(self, plug):
        self.plug = plug

    def validate(self):
        saida = self.plug.receive("saida_sandbox")
        status = self.plug.receive("status_execucao")

        # Critérios simples de validação
        if status != "sucesso":
            resultado = ("rejeitado", f"Execução com erro: status={status}")
        elif saida is None or saida.strip() == "":
            resultado = ("rejeitado", "Saída vazia ou nula")
        else:
            # Aqui você pode adicionar mais critérios (ex: conteúdo proibido)
            resultado = ("aprovado", "Código executado corretamente")

        self.plug.send("resultado_validacao", resultado)
        return resultado

# ===============================
# ?? Teste Simples (executável)
# ===============================
def test_validator():
    plug = InternalPlug()

    # Simula saída e status recebidos do isolation_runner
    plug.send("saida_sandbox", "Tudo certo")
    plug.send("status_execucao", "sucesso")

    validator = Validator(plug)
    resultado = validator.validate()
    print("Resultado da validação:", resultado)

    # Testa caso com erro
    plug.send("saida_sandbox", "Erro grave")
    plug.send("status_execucao", "erro")
    resultado_erro = validator.validate()
    print("Resultado da validação (erro):", resultado_erro)

if __name__ == "__main__":
    test_validator()
