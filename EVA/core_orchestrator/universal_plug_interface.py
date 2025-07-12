class UniversalPlugInterface:
    def receive(self, data):
        raise NotImplementedError()

    def send(self):
        raise NotImplementedError()

    def get_status(self):
        raise NotImplementedError()
