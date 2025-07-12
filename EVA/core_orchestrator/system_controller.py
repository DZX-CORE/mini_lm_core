from EVA.context_engine.core_interface import ContextEngineInterface
from EVA.linguistic_core.core_interface import LinguisticCoreInterface
from EVA.self_inquiry.core_interface import SelfInquiryInterface
from EVA.knowledge_base.core_interface import KnowledgeBaseInterface
from EVA.internal_research.core_interface import InternalResearchInterface
from EVA.knowledge_filter.core_interface import KnowledgeFilterInterface

class SystemController:
    def __init__(self):
        self.cores = {
            "context_engine": ContextEngineInterface(),
            "linguistic_core": LinguisticCoreInterface(),
            "self_inquiry": SelfInquiryInterface(),
            "knowledge_base": KnowledgeBaseInterface(),
            "internal_research": InternalResearchInterface(),
            "knowledge_filter": KnowledgeFilterInterface(),
        }
        print("[INIT] SystemController iniciado.")

    def send_to_core(self, core_name, data):
        if core_name not in self.cores:
            return {"erro": f"Núcleo '{core_name}' não encontrado."}
        core = self.cores[core_name]
        core.send(data)

    def receive_from_core(self, core_name):
        if core_name not in self.cores:
            return None
        core = self.cores[core_name]
        return core.receive()

if __name__ == "__main__":
    controller = SystemController()
    pergunta = "Qual é a capital da França?"
    print(f"Enviando pergunta para núcleo linguístico: {pergunta}")
    controller.send_to_core("linguistic_core", pergunta)
    resposta = controller.receive_from_core("linguistic_core")
    print(f"Resposta recebida do núcleo linguístico: {resposta}")
