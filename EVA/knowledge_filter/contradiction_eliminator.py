from EVA.knowledge_filter.plug import InternalPlug

class ContradictionEliminator:
    def __init__(self, plug: InternalPlug):
        self.plug = plug

    def eliminate(self, facts):
        grupos_topico = {}
        for f in facts:
            grupos_topico.setdefault(f['topico'], []).append(f)

        resultado = []
        for topico, fatos in grupos_topico.items():
            # Agrupa por valor para detectar duplicatas e consenso
            grupos_valor = {}
            for f in fatos:
                grupos_valor.setdefault(f['valor'], []).append(f)

            if len(grupos_valor) == 1:
                # Apenas um valor, mantém todos os fatos (incluindo duplicatas)
                resultado.extend(fatos)
            else:
                # Contradição: mantém só o grupo com maior número de fatos (maior consenso)
                grupo_mais_forte = max(grupos_valor.values(), key=len)
                resultado.extend(grupo_mais_forte)

        self.plug.send("fatos_consistentes", resultado)
        return resultado


if __name__ == "__main__":
    plug = InternalPlug()
    eliminator = ContradictionEliminator(plug)
    fatos = [
        {'topico': 'água', 'valor': 'ferve a 100°C'},
        {'topico': 'água', 'valor': 'ferve a 90°C'},
        {'topico': 'fogo', 'valor': 'quente'},
        {'topico': 'fogo', 'valor': 'causa queimaduras'},
        {'topico': 'fogo', 'valor': 'causa queimaduras'},
    ]
    resultado = eliminator.eliminate(fatos)
    print("Fatos consistentes:", resultado)
    print("Dados no plug:", plug._data)
