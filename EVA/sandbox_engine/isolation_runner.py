import subprocess
from .plug import InternalPlug

class IsolationRunner:
    """
    Executa código em um ambiente isolado usando subprocessos.
    Evita impacto no núcleo principal da Eva.
    """

    def __init__(self, plug):
        self.plug = plug

    def run(self, code):
        try:
            process = subprocess.run(
                ['python3', '-c', code],
                capture_output=True,
                text=True,
                timeout=5  # Limite de tempo para segurança
            )
            if process.returncode == 0:
                # Sucesso, saída normal
                self.plug.send("saida_sandbox", process.stdout.strip())
                self.plug.send("status_execucao", "sucesso")
            else:
                # Erro, captura stderr
                self.plug.send("saida_sandbox", process.stderr.strip())
                self.plug.send("status_execucao", "erro")

        except Exception as e:
            self.plug.send("saida_sandbox", str(e))
            self.plug.send("status_execucao", "falha")

# ===============================
# ?? Teste Simples (executável)
# ===============================
def test_isolation_runner():
    plug = InternalPlug()
    runner = IsolationRunner(plug)
    
    codigo_teste = "print('Execução segura na sandbox!')"
    runner.run(codigo_teste)

    saida = plug.receive("saida_sandbox")
    status = plug.receive("status_execucao")

    print("Saída:", saida)
    print("Status:", status)

if __name__ == "__main__":
    test_isolation_runner()
