class MemoryStore:
    def __init__(self, plug):
        self.plug = plug

    def save_fact(self, topico, conteudo):
        """Salva um fato relacionado ao tópico no plug."""
        chave = f"memoria_{topico}"
        fatos = self.plug.receive(chave)
        if fatos is None:
            fatos = []
        fatos.append(conteudo)
        self.plug.send(chave, fatos)

    def get_fact(self, topico):
        """Recupera fatos relacionados ao tópico do plug."""
        chave = f"memoria_{topico}"
        return self.plug.receive(chave) or []

# Teste básico
if __name__ == "__main__":
    from plug import InternalPlug

    plug = InternalPlug()
    mem = MemoryStore(plug)

    mem.save_fact("água", "A água ferve a 100°C")
    mem.save_fact("água", "A água é transparente")
    fatos = mem.get_fact("água")

    print("Fatos sobre água:", fatos)
