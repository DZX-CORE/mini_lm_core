import re
from EVA.linguistic_core.plug import InternalPlug

class Tokenizer:
    def __init__(self, plug):
        self.plug = plug

    def tokenize(self, texto):
        tokens = re.findall(r'\w+|[^\w\s]', texto, re.UNICODE)
        self.plug.send("tokens", tokens)
        return tokens

if __name__ == "__main__":
    plug = InternalPlug()
    tokenizer = Tokenizer(plug)
    texto = "Olá, Eva! Tudo bem?"
    tokens = tokenizer.tokenize(texto)
    print("Tokens:", tokens)
    print("Do plug:", plug.receive("tokens"))
    assert tokens == ["Olá", ",", "Eva", "!", "Tudo", "bem", "?"], "Erro: tokenização incorreta"
    assert plug.receive("tokens") == tokens, "Erro: tokens não salvos corretamente no plug"
