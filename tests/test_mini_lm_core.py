import pytest
from EVA.linguistic_core.plug import InternalPlug
from EVA.linguistic_core.tokenizer import Tokenizer
from EVA.linguistic_core.intent_analyzer import IntentAnalyzer
from EVA.linguistic_core.response_generator import ResponseGenerator
from EVA.linguistic_core.core_interface import LinguisticCoreInterface

@pytest.fixture
def core_interface():
    return LinguisticCoreInterface()

@pytest.mark.parametrize("input_text, expected_intent, expected_response", [
    ("Oi, tudo bem?", "saudacao", "Olá! Como posso ajudar você hoje?"),
    ("Qual é o horário?", "pergunta_geral", "Essa é uma ótima pergunta. Deixe-me pensar..."),
    ("Obrigado pela ajuda!", "agradecimento", "De nada! Estou aqui para ajudar."),
    ("Tchau, até mais!", "despedida", "Até logo! Foi um prazer conversar com você."),
    ("Isso é estranho.", "indefinida", "Desculpe, não entendi sua intenção."),
])
def test_full_flow(core_interface, input_text, expected_intent, expected_response):
    core_interface.send(input_text)
    response = core_interface.receive()
    # Verifica resposta correta
    assert response == expected_response

    # Verifica se a intenção foi armazenada corretamente no plug interno
    intent = core_interface.plug.receive("intent")
    assert intent == expected_intent

    # Verifica se os tokens existem no plug
    tokens = core_interface.plug.receive("tokens")
    assert tokens is not None and len(tokens) > 0
