from EVA.linguistic_core.plug import InternalPlug
from EVA.linguistic_core.tokenizer import Tokenizer
from EVA.linguistic_core.intent_analyzer import IntentAnalyzer
from EVA.linguistic_core.response_generator import ResponseGenerator

class UniversalPlugInterface:
    def send(self, data):
        raise NotImplementedError

    def receive(self):
        raise NotImplementedError

class LinguisticCoreInterface(UniversalPlugInterface):
    def __init__(self):
        self.plug = InternalPlug()
        self.tokenizer = Tokenizer(self.plug)
        self.intent_analyzer = IntentAnalyzer(self.plug)
        self.response_generator = ResponseGenerator(self.plug)
        self._last_response = None

    def send(self, data):
        self.tokenizer.tokenize(data)
        self.intent_analyzer.analyze()
        self._last_response = self.response_generator.generate()

    def receive(self):
        return self._last_response

if __name__ == "__main__":
    core_interface = LinguisticCoreInterface()
    pergunta = "Olá, tudo bem?"
    print(f"Pergunta recebida: {pergunta}")
    core_interface.send(pergunta)
    resposta = core_interface.receive()
    print(f"Resposta gerada: {resposta}")
    assert resposta == "Olá! Como posso ajudar você hoje?", "Erro: resposta inesperada"
