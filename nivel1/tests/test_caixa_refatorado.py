from decimal import Decimal as D

import pytest

from pdv.caixa import FormaPagamento as F
from pdv.caixa import Pagamento, Venda
from pdv.caixa_refatorado import FechamentoService, RepositorioEmMemoria


def _vendas():
    return [Venda(1, [Pagamento(F.DINHEIRO, D("80.00"))])]


def test_servico_calcula_e_salva_o_fechamento():
    repo = RepositorioEmMemoria()
    servico = FechamentoService(repo)

    fechamento_id, fechamento = servico.fechar_e_salvar(
        operador_id=7,
        fundo_troco=D("100.00"),
        vendas=_vendas(),
        movimentos=[],
        contado={F.DINHEIRO: D("180.00")},
    )

    assert fechamento.status == "CONFERE"
    assert repo.registros[fechamento_id] == (fechamento, 7)


def test_ids_gerados_sao_sequenciais():
    repo = RepositorioEmMemoria()
    servico = FechamentoService(repo)
    args = {"fundo_troco": D("0.00"), "vendas": [], "movimentos": [], "contado": {}}

    id1, _ = servico.fechar_e_salvar(operador_id=1, **args)
    id2, _ = servico.fechar_e_salvar(operador_id=1, **args)

    assert (id1, id2) == (1, 2)


def test_nada_e_salvo_quando_o_calculo_falha():
    repo = RepositorioEmMemoria()
    servico = FechamentoService(repo)

    with pytest.raises(AttributeError):
        # vendas inválidas (None) fazem o cálculo lançar erro antes de salvar
        servico.fechar_e_salvar(
            operador_id=1, fundo_troco=D("0.00"), vendas=[None], movimentos=[], contado={}
        )

    assert repo.registros == {}
