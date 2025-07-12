import pytest
from EVA.internal_research.core_interface import InternalResearchInterface

def test_internal_research_interface_flow():
    interface = InternalResearchInterface()

    entrada = {
        "topico": "inteligência artificial"
    }

    # Envia o tópico para a interface
    interface.receive(entrada)

    # Recupera a resposta processada
    resultado = interface.send()

    # Recupera o status atual
    status = interface.get_status()

    # Validações básicas
    assert isinstance(resultado, list), "Resultado deve ser uma lista"
    assert len(resultado) == 3, "Deve retornar 3 fatos formatados"
    for item in resultado:
        assert isinstance(item, dict), "Cada item deve ser um dicionário"
        assert "fato" in item, "Cada dicionário deve conter a chave 'fato'"
        assert "inteligência artificial" in item["fato"], "O fato deve conter o tópico buscado"

    assert status["última_entrada"]["topico"] == "inteligência artificial"
    assert status["status"] == "ok"
