from EVA.self_inquiry.decision_maker import DecisionMaker

class SelfInquiryInterface:
    def __init__(self):
        self.decision_maker = DecisionMaker()

    def send(self, data):
        # Implementação do envio
        pass

    def receive(self):
        # Implementação do recebimento
        pass
