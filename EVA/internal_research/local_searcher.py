class InternalPlug:
    def __init__(self):
        self._data = {}

    def send(self, key, value):
        self._data[key] = value

    def receive(self, key):
        return self._data.get(key)


# Mock de interfaces dos outros núcleos (para fins de teste)
class KnowledgeBaseInterface:
    def search(self, topic):
        return [f"[KB] Informação relevante sobre '{topic}'"]

class ContextEngineInterface:
    def search(self, topic):
        return [f"[CTX] Contexto recente sobre '{topic}'"]

class MemoryEngineInterface:
    def search(self, topic):
        return [f"[MEM] Memória armazenada sobre '{topic}'"]


class LocalSearcher:
    def __init__(self, plug):
        self.plug = plug
        # Conexões locais com outros núcleos via interface simulada
        self.kb = KnowledgeBaseInterface()
        self.ctx = ContextEngineInterface()
        self.mem = MemoryEngineInterface()

    def search(self, topic):
        resultados = []
        resultados += self.kb.search(topic)
        resultados += self.ctx.search(topic)
        resultados += self.mem.search(topic)

        self.plug.send("resultados_pesquisa", resultados)
        return resultados


# ?? Teste local
if __name__ == "__main__":
    print("[TEST] Realizando busca local sobre o tema 'inteligência artificial'...")
    plug = InternalPlug()
    searcher = LocalSearcher(plug)

    resultados = searcher.search("inteligência artificial")
    print("[RESULTADO] Resultados combinados:")
    for r in resultados:
        print(" -", r)

    assert isinstance(resultados, list)
    assert len(resultados) == 3
    assert plug.receive("resultados_pesquisa") == resultados

    print("[OK] Teste de busca local passou com sucesso.")
