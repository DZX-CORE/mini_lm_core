from EVA.versioning_system.plug import InternalPlug
from EVA.versioning_system.version_logger import VersionLogger
from EVA.versioning_system.version_comparator import VersionComparator
from EVA.versioning_system.rollback_handler import RollbackHandler

class VersioningSystemInterface:
    def __init__(self, plug, logger, comparator, rollback_handler):
        self.plug = plug
        self.logger = logger
        self.comparator = comparator
        self.rollback_handler = rollback_handler

    def receive(self, data):
        action = data.get("action")

        if action == "log_change":
            self.logger.log_change(data["module"], data["old_version"], data["new_version"], data["description"])

        elif action == "compare":
            self.comparator.compare_versions(data["old_code"], data["new_code"])

        elif action == "rollback":
            self.rollback_handler.rollback(data["module"], data["version"])

    def send(self):
        return {
            "log": self.logger.get_log(),
            "diff": self.plug.receive("diferencas"),
            "rollback_status": self.rollback_handler.confirm_rollback()
        }

    def get_status(self):
        return {
            "ultima_versao": self.plug.receive("diferencas"),
            "rollback": self.plug.receive("status_rollback")
        }


def test_interface():
    plug = InternalPlug()
    logger = VersionLogger(plug)
    comparator = VersionComparator(plug)
    rollback_handler = RollbackHandler(plug)

    interface = VersioningSystemInterface(plug, logger, comparator, rollback_handler)

    interface.receive({
        "action": "log_change",
        "module": "mod_interface",
        "old_version": "v1.0",
        "new_version": "v2.0",
        "description": "Update"
    })

    assert any(e["module_name"] == "mod_interface" for e in logger.get_log())
    print("✅    Teste passou: VersioningSystemInterface funciona corretamente.")

if __name__ == "__main__":
    test_interface()
