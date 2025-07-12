from datetime import datetime
from EVA.knowledge_filter.plug import InternalPlug

class Updater:
    def __init__(self, plug: InternalPlug):
        self.plug = plug
        self.base = {}  # fatos armazenados por tópico

    def check_obsolete(self, topic):
        fato = self.base.get(topic)
        if not fato or fato.get("data") is None:
            return True
        # Considera obsoleto se não tiver fato salvo ou data for menor que a data armazenada (ou outra regra)
        # Aqui: retorna False se fato está atualizado (data >= base)
        return False

    def update(self, new_fact):
        topic = new_fact["topico"]
        existente = self.base.get(topic)
        if (existente is None or
            (new_fact.get("data") and existente.get("data") and new_fact["data"] > existente["data"]) or
            (new_fact.get("confianca", 0) > existente.get("confianca", 0))):
            self.base[topic] = new_fact
            self.plug.send("fato_atualizado", new_fact)
            self.plug.send("base_atualizada", self.base)
            return True
        return False

if __name__ == "__main__":
    from datetime import datetime
    plug = InternalPlug()
    updater = Updater(plug)
    old_fact = {'topico': 'água', 'valor': 'molhada', 'data': datetime(2020, 1, 1), 'confianca': 0.7}
    new_fact = {'topico': 'água', 'valor': 'essencial para vida', 'data': datetime(2025, 1, 1), 'confianca': 0.95}
    print("Obsoleto (água) antes update:", updater.check_obsolete('água'))
    updater.update(old_fact)
    print("Obsoleto (água) após update:", updater.check_obsolete('água'))
    print("Atualizou:", updater.update(new_fact))
    print("Fato atualizado no plug:", plug.receive("fato_atualizado"))
    print("Base atualizada no plug:", plug.receive("base_atualizada"))
