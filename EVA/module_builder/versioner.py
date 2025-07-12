import os
import shutil

class Versioner:
    def __init__(self, plug, base_dir="EVA/module_builder"):
        self.plug = plug
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def _get_versioned_path(self, module_name, version_tag):
        return os.path.join(self.base_dir, f"{module_name}_{version_tag}.py")

    def _get_latest_version(self, module_name):
        versions = []
        for filename in os.listdir(self.base_dir):
            if filename.startswith(module_name + "_") and filename.endswith(".py"):
                ver = filename[len(module_name)+1:-3]
                # Só considera versões que seguem o padrão vX.Y
                if ver.startswith("v") and ver.count(".") == 1:
                    major_minor = ver.lstrip('v').split('.')
                    if len(major_minor) == 2 and all(x.isdigit() for x in major_minor):
                        versions.append(ver)
        versions.sort()
        return versions[-1] if versions else None

    def create_version(self, module_name, module_content):
        latest_version = self._get_latest_version(module_name)
        if latest_version is None:
            new_version = "v1.0"
        else:
            major, minor = latest_version.lstrip('v').split('.')
            major, minor = int(major), int(minor)
            minor += 1
            new_version = f"v{major}.{minor}"

        path = self._get_versioned_path(module_name, new_version)
        with open(path, "w", encoding="utf-8") as f:
            f.write(module_content)

        self.plug.send("versao_atual", new_version)
        self.plug.send("modulo_versao", f"{module_name}_{new_version}")
        return new_version

    def get_version(self, module_name, version_tag):
        path = self._get_versioned_path(module_name, version_tag)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def rollback(self, module_name):
        latest_version = self._get_latest_version(module_name)
        if latest_version is None:
            return None
        # Remove latest version file
        path = self._get_versioned_path(module_name, latest_version)
        os.remove(path)
        # Atualiza plug para a versão anterior
        previous_version = self._get_latest_version(module_name)
        if previous_version:
            self.plug.send("versao_atual", previous_version)
            self.plug.send("modulo_versao", f"{module_name}_{previous_version}")
        else:
            self.plug.send("versao_atual", None)
            self.plug.send("modulo_versao", None)
        return previous_version


# ?? Teste simples de Versioner
def test_versioner():
    from EVA.module_builder.plug import InternalPlug

    plug = InternalPlug()
    versioner = Versioner(plug)

    nome_modulo = "modulo_teste"
    conteudo_v1 = "print('Versão 1')"
    conteudo_v2 = "print('Versão 2')"

    v1 = versioner.create_version(nome_modulo, conteudo_v1)
    assert v1 == "v1.0", f"Esperava v1.0, obteve {v1}"

    v2 = versioner.create_version(nome_modulo, conteudo_v2)
    assert v2 == "v1.1", f"Esperava v1.1, obteve {v2}"

    conteudo_recuperado = versioner.get_version(nome_modulo, v1)
    assert conteudo_recuperado == conteudo_v1

    rollback_ver = versioner.rollback(nome_modulo)
    assert rollback_ver == "v1.0"

    conteudo_recuperado_apos_rollback = versioner.get_version(nome_modulo, rollback_ver)
    assert conteudo_recuperado_apos_rollback == conteudo_v1

    print("✅ Teste passou: Versioner cria, recupera e faz rollback corretamente.")

if __name__ == "__main__":
    test_versioner()
