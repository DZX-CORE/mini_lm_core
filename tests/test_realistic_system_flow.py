import pytest
from EVA.core_orchestrator.system_controller import SystemController

@pytest.fixture
def controller():
    return SystemController()

def test_realistic_flow(controller):
    pergunta = "Qual é a capital da França?"

    # Envia a pergunta para o núcleo linguístico
    controller.send_to_core("linguistic_core", pergunta)

    # Recebe a resposta do núcleo linguístico
    resposta_linguistica = controller.receive_from_core("linguistic_core")

    assert isinstance(resposta_linguistica, str), "Resposta deve ser string"
    assert len(resposta_linguistica) > 0, "Resposta não pode ser vazia"

    # Opcional: print para debug
    print("Resposta Linguística:", resposta_linguistica)

