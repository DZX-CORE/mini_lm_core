from EVA.constitutional_core.plug import InternalPlug

class ResponseValidator:
    def __init__(self, plug):
        self.plug = plug

    def validate(self, response):
        regras = self.plug.receive("regras_constitucionais") or []

        # Valida resposta com base nas regras
        problemas = []

        if "não mentir" in [r.lower() for r in regras]:
            if "mentira" in response.lower():
                problemas.append("Contém potencial mentira")

        if "evitar conteúdo ilegal" in [r.lower() for r in regras]:
            if "pirataria" in response.lower() or "crime" in response.lower():
                problemas.append("Pode conter conteúdo ilegal")

        if "ser útil" in [r.lower() for r in regras]:
            if len(response.strip()) < 10:
                problemas.append("Resposta curta demais para ser útil")

        if problemas:
            resultado = {"status": "negado", "motivos": problemas}
        else:
            resultado = {"status": "aprovado"}

        self.plug.send("resultado_validacao", resultado)
        return resultado


# Teste simples
def test_response_validator():
    plug = InternalPlug()
    plug.send("regras_constitucionais", ["Ser útil", "Não mentir", "Evitar conteúdo ilegal"])
    validador = ResponseValidator(plug)

    resposta_ok = "Claro! A capital da França é Paris."
    assert validador.validate(resposta_ok)["status"] == "aprovado"

    resposta_curta = "Sim."
    assert validador.validate(resposta_curta)["status"] == "negado"

    resposta_proibida = "Você pode baixar por pirataria."
    resultado = validador.validate(resposta_proibida)
    assert resultado["status"] == "negado"
    assert any("ilegal" in m.lower() for m in resultado["motivos"])

    print("✅  Teste passou: ResponseValidator valida respostas com base nas regras.")

if __name__ == "__main__":
    test_response_validator()
