from EVA.context_engine.core_interface import ContextEngineInterface
from EVA.linguistic_core.core_interface import LinguisticCoreInterface
from EVA.self_inquiry.core_interface import SelfInquiryInterface
from EVA.knowledge_base.core_interface import KnowledgeBaseInterface
from EVA.internal_research.core_interface import InternalResearchInterface
from EVA.knowledge_filter.core_interface import KnowledgeFilterInterface
from EVA.module_builder.core_interface import ModuleBuilderInterface
from EVA.constitutional_core.core_interface import ConstitutionalCoreInterface

# Import versioning_system modules
from EVA.versioning_system.plug import InternalPlug
from EVA.versioning_system.version_logger import VersionLogger
from EVA.versioning_system.version_comparator import VersionComparator
from EVA.versioning_system.rollback_handler import RollbackHandler
from EVA.versioning_system.core_interface import VersioningSystemInterface

# Import sandbox_engine interface
from EVA.sandbox_engine.core_interface import SandboxEngineInterface

# Import external_mentor interface
from EVA.external_mentor.core_interface import ExternalMentorInterface


class SystemController:
    def __init__(self):
        # Inicializar componentes internos para versioning_system
        plug = InternalPlug()
        logger = VersionLogger(plug)
        comparator = VersionComparator(plug)
        rollback_handler = RollbackHandler(plug)

        self.cores = {
            "context_engine": ContextEngineInterface(),
            "linguistic_core": LinguisticCoreInterface(),
            "self_inquiry": SelfInquiryInterface(),
            "knowledge_base": KnowledgeBaseInterface(),
            "internal_research": InternalResearchInterface(),
            "knowledge_filter": KnowledgeFilterInterface(),
            "module_builder": ModuleBuilderInterface(),
            "constitutional_core": ConstitutionalCoreInterface(),
            "versioning_system": VersioningSystemInterface(plug, logger, comparator, rollback_handler),
            "sandbox_engine": SandboxEngineInterface(),
            "external_mentor": ExternalMentorInterface(),
        }
        print("[INIT] SystemController iniciado.")

    def send_to_core(self, core_name, data):
        if core_name not in self.cores:
            return {"erro": f"Núcleo '{core_name}' não encontrado."}
        core = self.cores[core_name]
        core.receive(data)

    def receive_from_core(self, core_name):
        if core_name not in self.cores:
            return None
        core = self.cores[core_name]
        return core.send()


if __name__ == "__main__":
    controller = SystemController()

    # Teste de sandbox_engine
    codigo = "print('Oi do orquestrador para sandbox!')"
    print("Enviando código para sandbox_engine...")
    controller.send_to_core("sandbox_engine", codigo)
    resposta = controller.receive_from_core("sandbox_engine")
    print("Resposta recebida do sandbox_engine:", resposta)

    # Teste de external_mentor
    pergunta = {"mentor": "OpenAI", "pergunta": "Qual o sentido da vida?"}
    print("Enviando pergunta para external_mentor...")
    controller.send_to_core("external_mentor", pergunta)
    resposta_mentor = controller.receive_from_core("external_mentor")
    print("Resposta recebida do external_mentor:", resposta_mentor)
