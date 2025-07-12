from datetime import datetime, timezone

class VersionLogger:
    def __init__(self, plug):
        self.plug = plug
        self.history = []

    def log_change(self, module_name, old_version, new_version, description):
        entry = {
            "module_name": module_name,
            "old_version": old_version,
            "new_version": new_version,
            "description": description,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.history.append(entry)
        self.plug.send("historico_versionamento", self.history)

    def get_log(self):
        return self.plug.receive("historico_versionamento") or []

if __name__ == "__main__":
    from EVA.versioning_system.plug import InternalPlug
    plug = InternalPlug()
    logger = VersionLogger(plug)
    logger.log_change("modulo_teste", "v1.0", "v1.1", "Atualização de bug")
    log = logger.get_log()
    assert len(log) == 1, "Erro: log deve conter 1 registro"
    assert log[0]["module_name"] == "modulo_teste", "Erro: nome do módulo incorreto"
    print("✅  Teste passou: VersionLogger registra e retorna histórico corretamente.")
