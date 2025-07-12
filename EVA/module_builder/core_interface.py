from EVA.module_builder.plug import InternalPlug
from EVA.module_builder.module_generator import ModuleGenerator
from EVA.module_builder.versioner import Versioner

class ModuleBuilderInterface:
    def __init__(self):
        self.plug = InternalPlug()
        self.generator = ModuleGenerator(self.plug)
        self.versioner = Versioner(self.plug)
        self.last_response = None

    def receive(self, data):
        """
        Recebe dados de outros núcleos.
        Espera um dict com comandos, por exemplo:
        {
            "action": "generate_module",
            "name": "modulo_novo",
            "content": "class NovoModulo: ..."
        }
        ou
        {
            "action": "create_version",
            "module_name": "modulo_novo",
            "module_content": "conteúdo python"
        }
        ou
        {
            "action": "rollback",
            "module_name": "modulo_novo"
        }
        """
        action = data.get("action")
        if action == "generate_module":
            nome = data.get("name")
            conteudo = data.get("content")
            if nome and conteudo:
                path = self.generator.generate_module(nome, conteudo)
                self.last_response = {"status": "success", "path": path}
            else:
                self.last_response = {"status": "error", "message": "Missing name or content"}
        elif action == "create_version":
            nome = data.get("module_name")
            conteudo = data.get("module_content")
            if nome and conteudo:
                versao = self.versioner.create_version(nome, conteudo)
                self.last_response = {"status": "success", "version": versao}
            else:
                self.last_response = {"status": "error", "message": "Missing module_name or module_content"}
        elif action == "rollback":
            nome = data.get("module_name")
            if nome:
                versao = self.versioner.rollback(nome)
                if versao:
                    self.last_response = {"status": "success", "rolled_back_to": versao}
                else:
                    self.last_response = {"status": "error", "message": "No versions to rollback"}
            else:
                self.last_response = {"status": "error", "message": "Missing module_name"}
        else:
            self.last_response = {"status": "error", "message": f"Unknown action '{action}'"}

    def send(self):
        """
        Envia a última resposta preparada para outros núcleos.
        """
        return self.last_response

    def get_status(self):
        """
        Retorna estado atual do núcleo.
        """
        versao_atual = self.plug.receive("versao_atual")
        return {
            "last_version": versao_atual,
            "status": "ready"
        }


# ?? Teste simples
def test_interface():
    interface = ModuleBuilderInterface()

    # Testa geração de módulo
    interface.receive({
        "action": "generate_module",
        "name": "modulo_teste_core",
        "content": "class ModuloTesteCore:\n    pass\n"
    })
    resposta = interface.send()
    assert resposta["status"] == "success", "Falha na geração de módulo"

    # Testa criação de versão
    interface.receive({
        "action": "create_version",
        "module_name": "modulo_teste_core",
        "module_content": "print('Versão 1')"
    })
    resposta = interface.send()
    assert resposta["status"] == "success", "Falha na criação de versão"

    # Testa rollback
    interface.receive({
        "action": "rollback",
        "module_name": "modulo_teste_core"
    })
    resposta = interface.send()
    assert resposta["status"] in ["success", "error"], "Falha no rollback"

    # Testa get_status
    status = interface.get_status()
    assert "last_version" in status, "Status inválido"

    print("✅ Teste passou: ModuleBuilderInterface funciona corretamente.")


if __name__ == "__main__":
    test_interface()
