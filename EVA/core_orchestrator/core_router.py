class CoreRouter:
    def __init__(self, system_controller):
        self.system_controller = system_controller

    def route(self, core_name, data):
        # Encaminha a mensagem para o núcleo apropriado via SystemController
        try:
            response = self.system_controller.send_to_core(core_name, data)
            return response
        except Exception as e:
            return {"error": str(e)}

    def broadcast(self, data):
        # Envia dados para todos os núcleos via SystemController
        return self.system_controller.broadcast(data)
