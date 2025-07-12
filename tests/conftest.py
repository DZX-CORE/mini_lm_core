import pytest
from EVA.core_orchestrator.system_controller import SystemController

@pytest.fixture(scope="module")
def controller():
    return SystemController()
