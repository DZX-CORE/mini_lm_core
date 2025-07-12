from EVA.knowledge_base.plug import InternalPlug
from EVA.knowledge_base.keyword_indexer import KeywordIndexer
from EVA.knowledge_base.memory_store import MemoryStore
from EVA.knowledge_base.relevance_filter import RelevanceFilter

class KnowledgeBaseInterface:
    def __init__(self):
        self.plug = InternalPlug()
        self.keyword_indexer = KeywordIndexer(plug=self.plug)
        self.memory_store = MemoryStore(plug=self.plug)
        self.relevance_filter = RelevanceFilter(plug=self.plug)

    def send(self, data):
        # Implementar fluxo de envio conforme necessidade, exemplo:
        self.keyword_indexer.index(data)
        self.memory_store.store(data)

    def receive(self):
        # Implementar fluxo de recebimento conforme necessidade, exemplo:
        return self.memory_store.retrieve()
