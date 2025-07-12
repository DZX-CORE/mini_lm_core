import sys
import os

# Adiciona o diretório EVA/self_inquiry ao caminho
sys.path.insert(0, os.path.abspath("EVA/self_inquiry"))

from core_interface import SelfInquiryInterface

def test_self_inquiry_decision_flow():
    interface = SelfInquiryInterface()

    entrada = {
        "pergunta": "Qual é a capital da França?",
        "resposta": "Paris é a capital da França.",
        "historico": ["Qual é a cidade mais importante da França?"],
        "topico": "geografia"
    }

    interface.receive(entrada)
    resultado = interface.send()
    status = interface.get_status()

    # Verificações
    assert 0 <= resultado["similaridade"] <= 1
    assert resultado["status_comparacao"] in {
        "atualizado", "redundante", "contraditório", "consistente"
    }
    assert resultado["decisao"] in {
        "usar_existente", "atualizar", "criar_novo"
    }

    # Diagnóstico opcional
    print("[TESTE] Resultado do núcleo:")
    print("Similaridade:", resultado["similaridade"])
    print("Status:", resultado["status_comparacao"])
    print("Decisão:", resultado["decisao"])
    print("Status Global:", status)
