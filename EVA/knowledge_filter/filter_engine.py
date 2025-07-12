class FilterEngine:
    def __init__(self, plug):
        self.plug = plug

    def run(self, facts, new_fact, sources):
        # Simulação de filtragem e seleção
        fato_valido = all(isinstance(f, dict) for f in facts)
        fonte = sources[0] if sources else {"nome": "desconhecida"}

        resultado = {
            "fonte_selecionada": fonte,
            "fatos_consistentes": facts if fato_valido else []
        }

        self.plug.send("fatos_filtrados", resultado)
        self.plug.send("log", "Filtro executado com sucesso.")
