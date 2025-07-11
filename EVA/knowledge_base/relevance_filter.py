import difflib
from EVA.knowledge_base.plug import InternalPlug

class RelevanceFilter:
    def __init__(self, plug: InternalPlug):
        self.plug = plug

    def filter(self, topic, threshold=0.5):
        # Recupera fatos do tópico
        facts = self.plug.receive(f"memoria_{topic}") or []
        if not facts:
            return []

        # Remove duplicatas
        unique_facts = self.remove_duplicates(facts)

        # Ranqueia os fatos
        ranked_facts = self.rank_facts(unique_facts)

        # Filtra os fatos com base no threshold (simplificado como top N)
        cutoff = max(1, int(len(ranked_facts) * threshold))
        filtered = ranked_facts[:cutoff]

        # Salva fatos relevantes no plug
        self.plug.send(f"fatos_relevantes_{topic}", filtered)
        return filtered

    def rank_facts(self, facts):
        # Ranqueia fatos por clareza (tamanho) e número de palavras (simplificado)
        def score(fact):
            length_score = len(fact)
            word_count = len(fact.split())
            return length_score + word_count * 2  # pesos arbitrários
        return sorted(facts, key=score, reverse=True)

    def remove_duplicates(self, facts):
        unique = []
        for fact in facts:
            if not any(self.similar(fact, u) > 0.8 for u in unique):
                unique.append(fact)
        return unique

    def similar(self, a, b):
        return difflib.SequenceMatcher(None, a, b).ratio()

if __name__ == "__main__":
    plug = InternalPlug()
    plug.send("memoria_fogo", [
        "O fogo é quente.",
        "O fogo é quente e perigoso.",
        "O fogo pode causar queimaduras.",
        "Fogo é quente.",
        "O fogo é uma combustão rápida."
    ])

    rf = RelevanceFilter(plug)
    filtrados = rf.filter("fogo", threshold=0.6)
    print("Fatos filtrados relevantes sobre fogo:")
    for f in filtrados:
        print("-", f)
