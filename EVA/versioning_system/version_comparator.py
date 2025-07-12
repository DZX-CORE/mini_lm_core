from EVA.versioning_system.plug import InternalPlug

class VersionComparator:
    def __init__(self, plug):
        self.plug = plug
        self.changes_summary = ""

    def compare_versions(self, old_code: str, new_code: str):
        old_lines = old_code.splitlines()
        new_lines = new_code.splitlines()

        added = []
        removed = []

        for line in new_lines:
            if line not in old_lines:
                added.append(line)
        for line in old_lines:
            if line not in new_lines:
                removed.append(line)

        summary_parts = []
        if added:
            summary_parts.append(f"{len(added)} linha(s) adicionada(s)")
        if removed:
            summary_parts.append(f"{len(removed)} linha(s) removida(s)")

        self.changes_summary = ", ".join(summary_parts) if summary_parts else "Nenhuma mudança detectada"

        diff = {
            "added": added,
            "removed": removed,
        }
        self.plug.send("diferencas", diff)

        return diff

    def get_changes_summary(self):
        return self.changes_summary


def test_version_comparator():
    plug = InternalPlug()
    comparator = VersionComparator(plug)

    old_code = "def foo():\n    return 1\n"
    new_code = "def foo():\n    return 2\n\ndef bar():\n    pass\n"

    diff = comparator.compare_versions(old_code, new_code)
    summary = comparator.get_changes_summary()

    print(f"Resumo das mudanças: {summary}")
    print(f"Diferenças detectadas:\n Adicionadas: {diff['added']}\n Removidas: {diff['removed']}")

    # Verifica linhas adicionadas - aceita as que foram adicionadas indentadas
    assert "linha(s) adicionada(s)" in summary
    assert ("linha(s) removida(s)" in summary) or ("Nenhuma mudança detectada" == summary)
    # Checa se pelo menos uma das linhas adicionadas esperadas está lá
    assert any(x in diff["added"] for x in ["    return 2", "def bar():", "    pass", ""])
    # Agora verifica a linha removida exatamente com indentação
    assert "    return 1" in diff["removed"]

    print("✅   Teste passou: VersionComparator compara diferenças entre versões corretamente.")


if __name__ == "__main__":
    test_version_comparator()
