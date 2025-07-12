import pytest
from EVA.versioning_system.plug import InternalPlug
from EVA.versioning_system.version_logger import VersionLogger
from EVA.versioning_system.version_comparator import VersionComparator
from EVA.versioning_system.rollback_handler import RollbackHandler
from EVA.versioning_system.core_interface import VersioningSystemInterface

# Fixtures
@pytest.fixture
def plug():
    return InternalPlug()

@pytest.fixture
def logger(plug):
    return VersionLogger(plug)

@pytest.fixture
def comparator(plug):
    return VersionComparator(plug)

@pytest.fixture
def rollback_handler(plug):
    return RollbackHandler(plug)

@pytest.fixture
def core_interface(plug, logger, comparator, rollback_handler):
    return VersioningSystemInterface(plug, logger, comparator, rollback_handler)

# Testes individuais
def test_internal_plug_send_receive(plug):
    plug.send("teste", "valor")
    assert plug.receive("teste") == "valor"

def test_version_logger_log_and_get_log(logger):
    logger.log_change("mod_x", "v1", "v2", "desc")
    logs = logger.get_log()
    assert any(entry["module_name"] == "mod_x" for entry in logs)

def test_version_comparator_compare_versions_and_summary(comparator):
    old_code = "def f():\n    return 1\n"
    new_code = "def f():\n    return 2\n"
    diff = comparator.compare_versions(old_code, new_code)
    summary = comparator.get_changes_summary()
    assert "linha(s) adicionada(s)" in summary or "linha(s) removida(s)" in summary
    assert "return 2" in "".join(diff["added"]) or "return 1" in "".join(diff["removed"])

def test_rollback_handler_rollback_and_confirm(rollback_handler, logger):
    logger.log_change("mod_teste", "v1.0", "v2.0", "Upgrade")
    success = rollback_handler.rollback("mod_teste", "v2.0")
    assert success is True
    status = rollback_handler.confirm_rollback()
    assert "revertido para v1.0" in status

def test_core_interface_receive_send_get_status(core_interface):
    core_interface.receive({
        "action": "log_change",
        "module": "mod_interface",
        "old_version": "v0.1",
        "new_version": "v0.2",
        "description": "Initial upgrade"
    })
    output = core_interface.send()
    assert "log" in output
    assert any(e["module_name"] == "mod_interface" for e in output["log"])
