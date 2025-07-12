from EVA.knowledge_filter.plug import InternalPlug
from EVA.knowledge_filter.filter_engine import FilterEngine
from EVA.knowledge_filter.confidence_comparator import ConfidenceComparator
from EVA.knowledge_filter.contradiction_eliminator import ContradictionEliminator
from EVA.knowledge_filter.updater import Updater

class KnowledgeFilterInterface:
    def __init__(self):
        self.plug = InternalPlug()
        self.filter_engine = FilterEngine(plug=self.plug)
        self.confidence_comparator = ConfidenceComparator(plug=self.plug)
        self.contradiction_eliminator = ContradictionEliminator(plug=self.plug)
        self.updater = Updater(plug=self.plug)

    def send(self, data):
        # Exemplo simplificado do fluxo
        self.filter_engine.process(data)

    def receive(self):
        # Implementar se necessário
        pass
