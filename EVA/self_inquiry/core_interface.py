from EVA.self_inquiry.plug import InternalPlug
from EVA.self_inquiry.similarity_checker import SimilarityChecker
from EVA.self_inquiry.knowledge_comparator import KnowledgeComparator
from EVA.self_inquiry.decision_maker import DecisionMaker

class SelfInquiryInterface:
    def __init__(self):
        self.plug = InternalPlug()
        self.similarity_checker = SimilarityChecker(self.plug)
        self.knowledge_comparator = KnowledgeComparator(self.plug)
        self.decision_maker = DecisionMaker(self.plug)
        self._last_decision = None

    def receive(self, data):
        # Validação básica de entrada
        pergunta = data.get("pergunta")
        resposta = data.get("resposta")
        historico = data.get("historico")
        topico = data.get("topico")

        # Sanitização
        pergunta = str(pergunta) if pergunta is not None else ""
        resposta = str(resposta) if resposta is not None else ""
        if not isinstance(historico, list):
            historico = []
        topico = str(topico) if topico is not None else ""

        similaridade = self.similarity_checker.check_similarity(pergunta, historico)
        status_comparacao = self.knowledge_comparator.compare(resposta, topico)
        decisao = self.decision_maker.make_decision()

        self._last_decision = decisao

    def send(self):
        return {
            "similaridade": self.plug.receive("similaridade"),
            "status_comparacao": self.plug.receive("status_comparacao"),
            "decisao": self.plug.receive("decisao"),
        }

    def get_status(self):
        return self._last_decision or "nenhuma_decisao"

if __name__ == "__main__":
    interface = SelfInquiryInterface()
    entrada = {
        "pergunta": "Qual é a capital da França?",
        "resposta": "Paris é a capital da França.",
        "historico": ["Qual a capital da França?"],
        "topico": "geografia"
    }
    print("[TEST] Testando SelfInquiryInterface...")
    interface.receive(entrada)
    resultado = interface.send()
    print("[RESULTADO]")
    print(f"Similaridade: {resultado['similaridade']}")
    print(f"Status Comparação: {resultado['status_comparacao']}")
    print(f"Decisão: {resultado['decisao']}")
    print("[OK] Teste de interface passou com sucesso.")
