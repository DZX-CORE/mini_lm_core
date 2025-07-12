from EVA.external_mentor.plug import InternalPlug

class KnowledgeExtractor:
    def __init__(self, plug):
        self.plug = plug
        # Palavras-chave simples para simular extração de conhecimento
        self.palavras_chave = ["água", "ferve", "100°C", "temperatura", "ponto de ebulição"]

    def extract(self):
        resposta = self.plug.receive("resposta_mentor")
        if not resposta:
            conhecimento = "Nenhuma resposta disponível para extrair."
        else:
            # Extração simples baseada em palavras-chave
            fatos_relevantes = []
            for palavra in self.palavras_chave:
                if palavra.lower() in resposta.lower():
                    fatos_relevantes.append(palavra)
            if fatos_relevantes:
                conhecimento = "Fatos extraídos: " + ", ".join(fatos_relevantes)
            else:
                conhecimento = "Nenhum fato relevante encontrado."
        self.plug.send("conhecimento_extraido", conhecimento)
        return conhecimento

# Teste simples
if __name__ == "__main__":
    plug = InternalPlug()
    # Simula uma resposta longa do mentor
    resposta_simulada = (
        "A água ferve a 100°C ao nível do mar, que é o ponto de ebulição normal. "
        "Essa temperatura pode variar com a pressão atmosférica."
    )
    plug.send("resposta_mentor", resposta_simulada)

    extractor = KnowledgeExtractor(plug)
    conhecimento = extractor.extract()
    print("Conhecimento extraído:", conhecimento)

    # Verifica dado salvo no plug
    conhecimento_armazenado = plug.receive("conhecimento_extraido")
    print("Conhecimento armazenado no plug:", conhecimento_armazenado)
