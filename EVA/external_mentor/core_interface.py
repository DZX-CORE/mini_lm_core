from EVA.external_mentor.plug import InternalPlug
from EVA.external_mentor.mentor_connector import MentorConnector
from EVA.external_mentor.knowledge_extractor import KnowledgeExtractor
from EVA.external_mentor.style_translator import StyleTranslator

class ExternalMentorInterface:
    def __init__(self):
        self.plug = InternalPlug()
        self.connector = MentorConnector(self.plug)
        self.extractor = KnowledgeExtractor(self.plug)
        self.translator = StyleTranslator(self.plug)
        self._last_status = {}

    def receive(self, data):
        # Espera um dict com chave 'mentor' e 'question'
        mentor_name = data.get("mentor", "OpenAI")
        question = data.get("question", "")
        
        self.connector.connect(mentor_name)
        self.connector.ask(question)
        self.extractor.extract()
        self.translator.translate()

        # Atualiza status
        self._last_status = {
            "last_question": question,
            "last_mentor": mentor_name,
            "last_response": self.plug.receive("resposta_eva"),
        }

    def send(self):
        return self.plug.receive("resposta_eva")

    def get_status(self):
        return self._last_status

# Teste simples
if __name__ == "__main__":
    interface = ExternalMentorInterface()
    dados = {
        "mentor": "OpenAI",
        "question": "Qual o sentido da vida?"
    }
    interface.receive(dados)
    resposta = interface.send()
    status = interface.get_status()

    print("Resposta do mentor traduzida para Eva:")
    print(resposta)
    print("Status atual do núcleo:")
    print(status)
