import pytest
from datetime import datetime, timedelta
from EVA.knowledge_filter.plug import InternalPlug
from EVA.knowledge_filter.confidence_comparator import ConfidenceComparator
from EVA.knowledge_filter.contradiction_eliminator import ContradictionEliminator
from EVA.knowledge_filter.updater import Updater
from EVA.knowledge_filter.core_interface import KnowledgeFilterInterface

@pytest.fixture
def plug():
    return InternalPlug()

# Testes para InternalPlug
def test_internal_plug_send_receive_basic(plug):
    plug.send("chave", 123)
    assert plug.receive("chave") == 123

def test_internal_plug_overwrite_data(plug):
    plug.send("chave", "valor1")
    plug.send("chave", "valor2")
    assert plug.receive("chave") == "valor2"

# Testes para ConfidenceComparator
def test_confidence_comparator_selects_highest(plug):
    comparator = ConfidenceComparator(plug)
    sources = [
        {'nome': 'Fonte A', 'confianca': 0.7},
        {'nome': 'Fonte B', 'confianca': 0.9},
        {'nome': 'Fonte C', 'confianca': 0.85},
    ]
    result = comparator.compare(sources)
    selected = plug.receive("fonte_selecionada")
    combined = plug.receive("confianca_combinada")
    assert selected is not None
    assert combined is not None
    assert 'nome' in selected
    assert selected['confianca'] == max(src['confianca'] for src in sources)

def test_confidence_comparator_combines_similar_confidences(plug):
    comparator = ConfidenceComparator(plug)
    sources = [
        {'nome': 'Fonte A', 'confianca': 0.85},
        {'nome': 'Fonte B', 'confianca': 0.875},
        {'nome': 'Fonte C', 'confianca': 0.87},
    ]
    result = comparator.compare(sources)
    selected = plug.receive("fonte_selecionada")
    combined = plug.receive("confianca_combinada")
    assert isinstance(selected['nome'], list)
    assert abs(combined - (0.85 + 0.875 + 0.87)/3) < 0.001

# Testes para ContradictionEliminator
def test_contradiction_eliminator_removes_conflicts(plug):
    eliminator = ContradictionEliminator(plug)
    facts = [
        {'topico': 'água', 'valor': 'ferve a 100°C'},
        {'topico': 'água', 'valor': 'ferve a 90°C'},  # Contraditório
        {'topico': 'fogo', 'valor': 'quente'},
        {'topico': 'fogo', 'valor': 'causa queimaduras'},
        {'topico': 'fogo', 'valor': 'causa queimaduras'},
    ]
    consistent = eliminator.eliminate(facts)
    plug_data = plug.receive("fatos_consistentes")
    # Não deve conter fatos contraditórios para 'água'
    topicos_agua = [f['valor'] for f in consistent if f['topico'] == 'água']
    assert 'ferve a 100°C' in topicos_agua or 'ferve a 90°C' in topicos_agua
    # Fatos para 'fogo' devem estar duplicados, remover duplicatas esperado
    assert len([f for f in consistent if f['topico'] == 'fogo']) == 2
    assert plug_data == consistent

# Testes para Updater
def test_updater_updates_and_checks_obsolete(plug):
    updater = Updater(plug)
    old_fact = {'topico': 'água', 'valor': 'molhada', 'data': datetime(2020, 1, 1), 'confianca': 0.7}
    new_fact = {'topico': 'água', 'valor': 'essencial para vida', 'data': datetime(2025, 1, 1), 'confianca': 0.95}
    updater.update(old_fact)
    assert updater.check_obsolete('água') == False  # Acabou de atualizar, não está obsoleto
    updater.update(new_fact)
    # O fato antigo deve estar obsoleto agora
    assert updater.check_obsolete('água') == False  # Atualizado para mais novo
    fato_atualizado = plug.receive("fato_atualizado")
    assert fato_atualizado['valor'] == 'essencial para vida'

def test_updater_does_not_update_with_older_fact(plug):
    updater = Updater(plug)
    newer_fact = {'topico': 'terra', 'valor': 'sólida', 'data': datetime(2025, 1, 1), 'confianca': 0.9}
    older_fact = {'topico': 'terra', 'valor': 'não sólida', 'data': datetime(2020, 1, 1), 'confianca': 0.5}
    updater.update(newer_fact)
    updater.update(older_fact)
    fato_atualizado = plug.receive("fato_atualizado")
    # O valor não deve ter sido sobrescrito pelo fato mais antigo
    assert fato_atualizado['valor'] == 'sólida'

# Teste integrado para KnowledgeFilterInterface
def test_knowledge_filter_interface_full_flow():
    interface = KnowledgeFilterInterface()
    dados_entrada = {
        "sources": [
            {'nome': 'Fonte A', 'confianca': 0.7},
            {'nome': 'Fonte B', 'confianca': 0.9},
            {'nome': 'Fonte C', 'confianca': 0.85},
        ],
        "facts": [
            {'topico': 'água', 'valor': 'ferve a 100°C'},
            {'topico': 'água', 'valor': 'ferve a 90°C'},  # Contraditório
            {'topico': 'fogo', 'valor': 'quente'},
        ],
        "new_fact": {'topico': 'água', 'valor': 'essencial para vida', 'data': datetime(2025, 1, 1), 'confianca': 0.95}
    }
    resposta = interface.receive(dados_entrada)
    assert resposta is not None
    assert 'fonte_selecionada' in resposta
    assert 'fatos_consistentes' in resposta
    assert 'fato_atualizado' in resposta
    assert isinstance(resposta['fonte_selecionada'], dict)
    assert isinstance(resposta['fatos_consistentes'], list)
    assert resposta['fato_atualizado']['valor'] == 'essencial para vida'

