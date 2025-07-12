import os
import pytest

from EVA.module_builder.plug import InternalPlug
from EVA.module_builder.module_generator import ModuleGenerator
from EVA.module_builder.versioner import Versioner
from EVA.module_builder.core_interface import ModuleBuilderInterface

BASE_DIR = "EVA/module_builder"

@pytest.fixture(autouse=True)
def cleanup_files():
    # Limpa arquivos gerados antes e depois dos testes
    yield
    for filename in os.listdir(BASE_DIR):
        if filename.endswith(".py") and filename not in {
            "plug.py",
            "module_generator.py",
            "versioner.py",
            "core_interface.py",
            "__init__.py"
        }:
            os.remove(os.path.join(BASE_DIR, filename))


def test_internal_plug_send_receive():
    plug = InternalPlug()
    plug.send("chave_teste", "valor_teste")
    assert plug.receive("chave_teste") == "valor_teste"
    assert plug.receive("chave_inexistente") is None


def test_module_generator_creates_file():
    plug = InternalPlug()
    generator = ModuleGenerator(plug)

    nome = "modulo_gerado_pytest"
    conteudo = "print('Teste geração')"

    caminho = generator.generate_module(nome, conteudo)
    assert os.path.exists(caminho)

    with open(caminho, "r", encoding="utf-8") as f:
        assert "Teste geração" in f.read()


def test_versioner_create_get_rollback():
    plug = InternalPlug()
    versioner = Versioner(plug)

    nome = "modulo_versionado_pytest"
    conteudo_v1 = "print('Versão 1')"
    conteudo_v2 = "print('Versão 2')"

    v1 = versioner.create_version(nome, conteudo_v1)
    v2 = versioner.create_version(nome, conteudo_v2)

    assert v1 == "v1.0"
    assert v2 == "v1.1"

    rec_v1 = versioner.get_version(nome, v1)
    assert rec_v1 == conteudo_v1

    rollback_ver = versioner.rollback(nome)
    assert rollback_ver == v1


def test_core_interface_workflow():
    interface = ModuleBuilderInterface()

    # Gerar módulo
    interface.receive({
        "action": "generate_module",
        "name": "modulo_core_pytest",
        "content": "class TesteCore:\n    pass\n"
    })
    resposta = interface.send()
    assert resposta["status"] == "success"
    assert os.path.exists(resposta["path"])

    # Criar versão
    interface.receive({
        "action": "create_version",
        "module_name": "modulo_core_pytest",
        "module_content": "print('Versão 1')"
    })
    resposta = interface.send()
    assert resposta["status"] == "success"
    assert resposta["version"] == "v1.0"

    # Rollback
    interface.receive({
        "action": "rollback",
        "module_name": "modulo_core_pytest"
    })
    resposta = interface.send()
    assert resposta["status"] in ["success", "error"]

    # Status
    status = interface.get_status()
    assert "last_version" in status
    assert status["status"] == "ready"
