import pytest
from EVA.knowledge_base.core_interface import KnowledgeBaseInterface

class MockPlug:
    def __init__(self):
        # Simula armazenamento interno
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

@pytest.fixture
def kb_interface():
    plug = MockPlug()
    return KnowledgeBaseInterface(plug)

def test_get_status_isolated(kb_interface):
    status = kb_interface.get_status()
    assert isinstance(status, dict)
    assert status["num_fatos_armazenados"] == 4  # 2 fatos fogo + 2 fatos água
    assert status["num_palavras_indexadas"] > 0

def test_receive_and_send_isolated(kb_interface):
    input_data = {"topico": "fogo"}
    response = kb_interface.receive(input_data)
    assert "fatos" in response
    assert len(response["fatos"]) == 2

def test_receive_no_topic(kb_interface):
    response = kb_interface.receive({})
    assert "error" in response or response == {}
