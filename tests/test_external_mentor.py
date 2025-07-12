import pytest
from EVA.external_mentor.plug import InternalPlug
from EVA.external_mentor.mentor_connector import MentorConnector
from EVA.external_mentor.knowledge_extractor import KnowledgeExtractor
from EVA.external_mentor.style_translator import StyleTranslator
from EVA.external_mentor.core_interface import ExternalMentorInterface

def test_internal_plug_basic():
    plug = InternalPlug()
    plug.send("chave", "valor")
    assert plug.receive("chave") == "valor"
    assert plug.receive("nao_existe") is None

def test_mentor_connector_simulation():
    plug = InternalPlug()
    connector = MentorConnector(plug)
    connector.connect("OpenAI")
    connector.ask("Qual o sentido da vida?")
    resposta = plug.receive("resposta_mentor")
    assert "OpenAI" in resposta
    assert "Qual o sentido da vida?" in resposta

def test_knowledge_extractor_basic():
    plug = InternalPlug()
    resposta = "A água ferve a 100°C no ponto de ebulição."
    plug.send("resposta_mentor", resposta)
    extractor = KnowledgeExtractor(plug)
    conhecimento = extractor.extract()
    assert "água" in conhecimento.lower() or "ferve" in conhecimento.lower()

def test_style_translator_basic():
    plug = InternalPlug()
    conhecimento = "Fatos extraídos: água, ferve, 100°C"
    plug.send("conhecimento_extraido", conhecimento)
    translator = StyleTranslator(plug)
    resposta = translator.translate()
    assert "Aqui está o que eu entendi" in resposta
    assert "água" in resposta

def test_external_mentor_interface_flow():
    interface = ExternalMentorInterface()
    dados = {"mentor": "OpenAI", "question": "Qual o sentido da vida?"}
    interface.receive(dados)
    resposta = interface.send()
    status = interface.get_status()
    assert resposta is not None
    assert "OpenAI" in status.get("last_mentor")
    assert "Qual o sentido da vida?" == status.get("last_question")

if __name__ == "__main__":
    pytest.main()
