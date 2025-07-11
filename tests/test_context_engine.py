import sys
import os
sys.path.insert(0, '.')

from EVA.context_engine.core_interface import ContextEngineInterface

def test_emocao_triste():
    interface = ContextEngineInterface()
    interface.receive("Estou muito triste com tudo isso.")
    status = interface.get_status()
    assert status["emoção"] == "triste"
    assert "triste" in status["historico"][-1]["conteudo"]

def test_contexto_mudou():
    interface = ContextEngineInterface()
    interface.receive("Como está o clima hoje?")
    interface.receive("Aliás, preciso de um conselho sobre minha carreira.")
    status = interface.get_status()
    assert status["contexto_mudou"] is True

def test_historico_funcional():
    interface = ContextEngineInterface()
    interface.receive("Oi!")
    interface.receive("Tudo bem?")
    historico = interface.get_status()["historico"]
    assert len(historico) >= 2
    assert any(entry["tipo"] == "usuario" for entry in historico)
    assert any(entry["tipo"] == "eva" for entry in historico)
