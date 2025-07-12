from EVA.knowledge_filter.plug import InternalPlug

class ConfidenceComparator:
    def __init__(self, plug: InternalPlug):
        self.plug = plug

    def compare(self, sources):
        if not sources:
            return None
        
        # Critério simples: encontrar o máximo de confiança
        max_conf = max(src['confianca'] for src in sources)
        
        # Verifica quais fontes têm confiança muito próxima (dentro de 0.03)
        proximos = [src for src in sources if abs(src['confianca'] - max_conf) <= 0.03]

        if len(proximos) > 1:
            # Combina as fontes semelhantes
            nomes_combinados = [src['nome'] for src in proximos]
            confianca_combinada = sum(src['confianca'] for src in proximos) / len(proximos)
            resultado = {'nome': nomes_combinados, 'confianca': round(confianca_combinada, 3)}
            self.plug.send("fonte_selecionada", resultado)
            self.plug.send("confianca_combinada", resultado['confianca'])
            return resultado
        else:
            # Só uma fonte claramente superior
            selecionada = max(sources, key=lambda src: src['confianca'])
            self.plug.send("fonte_selecionada", selecionada)
            self.plug.send("confianca_combinada", selecionada['confianca'])
            return selecionada

if __name__ == "__main__":
    # Teste simples
    plug = InternalPlug()
    comparator = ConfidenceComparator(plug)
    fontes = [
        {'nome': 'Fonte A', 'confianca': 0.85},
        {'nome': 'Fonte B', 'confianca': 0.875},
        {'nome': 'Fonte C', 'confianca': 0.87},
    ]
    resultado = comparator.compare(fontes)
    print("Fonte selecionada:", resultado)
    print("Dados no plug:", plug._data)
