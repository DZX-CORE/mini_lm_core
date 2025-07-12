class ContextEngineInterface:
    def __init__(self):
        from EVA.context_engine.history_manager import HistoryManager
        from EVA.context_engine.plug import InternalPlug

        self.history_manager = HistoryManager(plug=InternalPlug())

    def send(self, data):
        # Implementar lógica para enviar dados ao history_manager
        self.history_manager.plug.send("input_data", data)

    def receive(self):
        # Implementar lógica para receber dados do history_manager
        return self.history_manager.plug.receive("output_data")
