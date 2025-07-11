class InternalPlug:
    def __init__(self):
        self.storage = {}

    def send(self, key, value):
        self.storage[key] = value

    def receive(self, key):
        return self.storage.get(key)


class ResultFormatter:
    def __init__(self, plug):
        self.plug = plug

    def format_results(self):
        brutos = self.plug.receive("resultados_pesquisa")
        if not isinstance(brutos, list):
            self.plug.send("resultado_formatado", [])
            return

        # Eliminar duplicatas (baseado em conteúdo textual)
        unicos = list(set(brutos))

        # Ordenação simples: por ordem alfabética (poderia ser por relevância real em produção)
        ordenados = sorted(unicos, key=lambda x: x.lower())

        # Formato estruturado: lista de fatos como dicionários
        formatado = [{"fato": texto} for texto in ordenados]

        self.plug.send("resultado_formatado", formatado)


# Teste isolado
if __name__ == "__main__":
    print("[TEST] Formatando resultados de pesquisa internos...")
    plug = InternalPlug()
    resultados_brutos = [
        "[CTX] Contexto recente sobre IA",
        "[KB] Informação relevante sobre IA",
        "[MEM] Memória armazenada sobre IA",
        "[KB] Informação relevante sobre IA",  # duplicado
    ]
    plug.send("resultados_pesquisa", resultados_brutos)

    formatter = ResultFormatter(plug)
    formatter.format_results()

    resultado_final = plug.receive("resultado_formatado")
    print("[RESULTADO FORMATADO]")
    for fato in resultado_final:
        print("-", fato)

    assert isinstance(resultado_final, list)
    assert all("fato" in item for item in resultado_final)
    assert len(resultado_final) == 3
    print("[OK] Teste de formatação passou com sucesso.")
