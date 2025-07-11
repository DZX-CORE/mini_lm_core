import re

class KeywordIndexer:
    def __init__(self, plug):
        self.plug = plug
        # índice no formato {palavra_chave: set([topico1, topico2, ...])}
        if self.plug.receive("indice_palavras") is None:
            self.plug.send("indice_palavras", {})

    def _extract_keywords(self, texto):
        # Extrai palavras relevantes simples: letras e números, ignorando stopwords básicas
        stopwords = {"a", "o", "e", "de", "do", "da", "em", "um", "uma", "por", "para", "com", "que", "os", "as"}
        palavras = re.findall(r'\b\w+\b', texto.lower())
        return [p for p in palavras if p not in stopwords]

    def index_fact(self, topico, conteudo):
        indice = self.plug.receive("indice_palavras")
        if indice is None:
            indice = {}
        keywords = self._extract_keywords(conteudo)
        for kw in keywords:
            if kw not in indice:
                indice[kw] = set()
            indice[kw].add(topico)
        self.plug.send("indice_palavras", indice)

    def search_by_keyword(self, palavra_chave):
        indice = self.plug.receive("indice_palavras")
        if not indice:
            return []
        return list(indice.get(palavra_chave.lower(), []))


if __name__ == "__main__":
    from EVA.knowledge_base.plug import InternalPlug

    plug = InternalPlug()
    indexer = KeywordIndexer(plug)

    # Indexa fatos
    indexer.index_fact("água", "A água ferve a 100°C e é transparente.")
    indexer.index_fact("fogo", "O fogo é quente e pode queimar.")
    indexer.index_fact("terra", "A terra é sólida e suporta vida.")

    # Busca por palavra-chave
    resultados = indexer.search_by_keyword("quente")
    print("Tópicos com a palavra-chave 'quente':", resultados)
