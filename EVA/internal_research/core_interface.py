from EVA.internal_research.plug import InternalPlug
from EVA.internal_research.local_searcher import LocalSearcher
from EVA.internal_research.result_formatter import ResultFormatter

class InternalResearchInterface:
    def __init__(self):
        self.plug = InternalPlug()
        self.searcher = LocalSearcher(self.plug)
        self.formatter = ResultFormatter(self.plug)

    def send(self, data):
        self.plug.send("consulta", data)
        resultados = self.searcher.buscar()
        self.plug.send("resultados_crus", resultados)

    def receive(self):
        return self.formatter.formatar()
