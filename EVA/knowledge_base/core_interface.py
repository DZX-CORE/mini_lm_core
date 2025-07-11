class KnowledgeBaseInterface:
    def __init__(self, plug):
        self.plug = plug

    def receive(self, data):
        topico = data.get("topico")
        if not topico:
            return {"error": "Nenhum tópico fornecido."}

        fatos = self.plug.receive(f"memoria_{topico}")
        if not fatos:
            return {"message": f"Nenhum fato encontrado para tópico '{topico}'."}

        return {"fatos": fatos}

    def send(self, data):
        # Exemplo simples: apenas retorna os dados enviados
        return data

    def get_status(self):
        memoria_keys = [k for k in self.plug._storage.keys() if k.startswith("memoria_")]
        num_fatos = sum(len(self.plug.receive(k)) for k in memoria_keys)

        indice = self.plug.receive("indice_palavras")
        num_palavras = len(indice) if indice else 0

        return {
            "num_fatos_armazenados": num_fatos,
            "num_palavras_indexadas": num_palavras
        }

if __name__ == "__main__":
    class MockPlug:
        def __init__(self):
            self._storage = {
                "memoria_fogo": ["O fogo é uma combustão rápida.", "O fogo pode causar queimaduras."],
                "memoria_água": ["A água ferve a 100°C", "A água é transparente"],
                "indice_palavras": {
                    "fogo": ["memoria_fogo"],
                    "combustão": ["memoria_fogo"],
                    "queimaduras": ["memoria_fogo"],
                    "água": ["memoria_água"],
                    "ferve": ["memoria_água"],
                    "transparente": ["memoria_água"]
                }
            }
        def receive(self, key):
            return self._storage.get(key, [])
        def send(self, key, value):
            self._storage[key] = value

    plug = MockPlug()
    kb_interface = KnowledgeBaseInterface(plug)

    print("Status do núcleo:", kb_interface.get_status())
    print("Receive com tópico fogo:", kb_interface.receive({"topico": "fogo"}))
    print("Receive com tópico desconhecido:", kb_interface.receive({"topico": "terra"}))
    print("Receive sem tópico:", kb_interface.receive({}))
