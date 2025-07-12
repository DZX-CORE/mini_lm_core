import pytest
from system_controller import SystemController

@pytest.fixture
def controller():
    return SystemController()

def test_external_mentor_flow(controller):
    pergunta = {
        "mentor": "OpenAI",
        "pergunta": "A água ferve a 100°C?"
    }

    controller.send_to_core("external_mentor", pergunta)
    resposta = controller.receive_from_core("external_mentor")

    assert isinstance(resposta, str)
    assert "água" in resposta or "100°C" in resposta or "entendi" in resposta.lower()
