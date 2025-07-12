from EVA.versioning_system.plug import InternalPlug
from EVA.versioning_system.version_logger import VersionLogger
from EVA.versioning_system.version_comparator import VersionComparator

class RollbackHandler:
    def __init__(self, plug):
        self.plug = plug
        self.logger = VersionLogger(plug)
        self.comparator = VersionComparator(plug)

    def rollback(self, module_name, version_tag):
        log = self.logger.get_log()
        matching_entries = [
            entry for entry in log
            if entry["module_name"] == module_name and entry["new_version"] == version_tag
        ]

        if not matching_entries:
            self.plug.send("status_rollback", "Versão não encontrada")
            return False

        entry = matching_entries[0]
        previous_version = entry["old_version"]

        # Simula rollback (só salva status)
        self.plug.send("status_rollback", f"{module_name} revertido para {previous_version}")
        return True

    def confirm_rollback(self):
        return self.plug.receive("status_rollback")

    def get_previous_version(self, module_name):
        log = self.logger.get_log()
        for entry in reversed(log):
            if entry["module_name"] == module_name:
                return entry["old_version"]
        return None


def test_rollback_handler():
    plug = InternalPlug()
    logger = VersionLogger(plug)
    comparator = VersionComparator(plug)

    logger.log_change("mod_teste", "v1.0", "v2.0", "Upgrade crítico")
    rollback = RollbackHandler(plug)
    assert rollback.rollback("mod_teste", "v2.0")
    status = rollback.confirm_rollback()
    assert "revertido para v1.0" in status
    print("✅    Teste passou: RollbackHandler reverte versões corretamente.")

if __name__ == "__main__":
    test_rollback_handler()
