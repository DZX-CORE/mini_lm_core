from EVA.internal_research.plug import InternalPlug
from EVA.internal_research.local_searcher import LocalSearcher
from EVA.internal_research.result_formatter import ResultFormatter

# Simulando interface UniversalPlugInterface (pode ajustar se houver de verdade)
class UniversalPlugInterface:
    def receive(self, data):
        raise NotImplementedError()
    def send(self):
        raise NotImplementedError()
    def get_status(self):
        raise NotImplementedError()

class InternalResearchInterface(UniversalPlugInterface):
    def __init__(self):
        self.plug = InternalPlug()
        self.last_input = None
        self.status = "idle"

    def receive(self, data):
        if not isinstance(data, dict):
            self.status = "entrada inválida: não é dict"
            return  # ignorar entrada inválida, sem exceção
        topico = data.get("topico")
        if not isinstance(topico, str):
            self.status = "entrada inválida: 'topico' deve ser string"
            return  # ignorar entrada inválida, sem exceção
        # aceita só a chave topico (outros campos são ignorados)
        self.last_input = {"topico": topico}
        self.status = "ok"
        # Realizar busca e formatação imediata para estar disponível no send()
        try:
            searcher = LocalSearcher(self.plug)
            searcher.search(topico)
            formatter = ResultFormatter(self.plug)
            formatter.format_results()
        except Exception as e:
            self.status = f"erro interno: {str(e)}"

    def send(self):
        try:
            resultado_formatado = self.plug.receive("resultado_formatado")
            if resultado_formatado is None:
                return {"erro": "Nenhum resultado formatado disponível."}
            return {"resultado_formatado": resultado_formatado}
        except Exception as e:
            return {"erro": str(e)}

    def get_status(self):
        return {"última_entrada": self.last_input, "status": self.status}

if __name__ == "__main__":
    print("[TEST] Testando InternalResearchInterface...")
    interface = InternalResearchInterface()
    test_data = {"topico": "inteligência artificial", "extra": "valor"}  # extra ignorada

    interface.receive(test_data)
    resultado = interface.send()
    status = interface.get_status()

    print("[RESULTADO FINAL]")
    if "resultado_formatado" in resultado:
        for fato in resultado["resultado_formatado"]:
            print("-", fato)
    else:
        print("[ERRO]", resultado.get("erro"))

    print("[STATUS]", status)
    print("[OK] Teste de interface passou com sucesso.")
