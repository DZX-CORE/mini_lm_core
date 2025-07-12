from EVA.context_engine.core_interface import ContextEngineInterface
from EVA.linguistic_core.core_interface import LinguisticCoreInterface
from EVA.self_inquiry.core_interface import SelfInquiryInterface
from EVA.knowledge_base.core_interface import KnowledgeBaseInterface
from EVA.internal_research.core_interface import InternalResearchInterface
from EVA.knowledge_filter.core_interface import KnowledgeFilterInterface
from EVA.module_builder.core_interface import ModuleBuilderInterface
from EVA.constitutional_core.core_interface import ConstitutionalCoreInterface

# Importando Versioning System e seus módulos internos
from EVA.versioning_system.plug import InternalPlug
from EVA.versioning_system.version_logger import VersionLogger
from EVA.versioning_system.version_comparator import VersionComparator
from EVA.versioning_system.rollback_handler import RollbackHandler
from EVA.versioning_system.core_interface import VersioningSystemInterface


class SystemController:
    def __init__(self):
        # Inicializar componentes internos para versioning_system
        plug = InternalPlug()
        logger = VersionLogger(plug)
        comparator = VersionComparator(plug)
        rollback_handler = RollbackHandler(plug)  # Ajustado para receber só plug

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

    comando = {
        "action": "generate_module",
        "name": "modulo_teste_orquestrador",
        "content": "print('Gerado via orquestrador')"
    }
    print("Enviando comando para module_builder:", comando)
    controller.send_to_core("module_builder", comando)

    resposta = controller.receive_from_core("module_builder")
    print("Resposta recebida do module_builder:", resposta)
