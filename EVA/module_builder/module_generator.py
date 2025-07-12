import os

class ModuleGenerator:
    def __init__(self, plug):
        self.plug = plug

    def generate_module(self, name, content, directory="EVA/module_builder"):
        # Assegura que o diretório existe
        os.makedirs(directory, exist_ok=True)
        
        # Caminho completo do novo arquivo
        filepath = os.path.join(directory, f"{name}.py")
        
        # Escreve o conteúdo no arquivo
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

        # Notifica o plug
        self.plug.send("modulo_gerado", name)
        return filepath


# ?? Teste simples do ModuleGenerator
def test_module_generator():
    from EVA.module_builder.plug import InternalPlug

    plug = InternalPlug()
    generator = ModuleGenerator(plug)

    nome_modulo = "modulo_teste_gerado"
    conteudo = '''class ModuloTeste:
    def executar(self):
        print("Este é um módulo de teste gerado automaticamente.")
'''

    caminho = generator.generate_module(nome_modulo, conteudo)

    # Verifica se o arquivo foi criado
    assert os.path.exists(caminho), f"Erro: Arquivo {caminho} não foi criado."

    # Verifica se o conteúdo está correto
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo_arquivo = f.read()
        assert "ModuloTeste" in conteudo_arquivo

    # Verifica comunicação com o plug
    assert plug.receive("modulo_gerado") == nome_modulo

    print("✅ Teste passou: ModuleGenerator criou módulo corretamente.")

if __name__ == "__main__":
    test_module_generator()
