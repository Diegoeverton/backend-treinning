from decimal import Decimal as D

from pdv.caixa import (
    FormaPagamento as F,
)
from pdv.caixa import (
    Movimento,
    Pagamento,
    TipoMovimento,
    Venda,
    fechar_caixa,
)


def _vendas_do_turno():
    return [
        Venda(1, [Pagamento(F.DINHEIRO, D("80.00"))]),
        Venda(2, [Pagamento(F.PIX, D("150.00"))]),
        # venda paga com duas formas
        Venda(3, [Pagamento(F.DEBITO, D("100.00")), Pagamento(F.DINHEIRO, D("29.90"))]),
        Venda(4, [Pagamento(F.CREDITO, D("259.80"))]),
        # cancelada: não entra no fechamento
        Venda(5, [Pagamento(F.DINHEIRO, D("500.00"))], cancelada=True),
    ]


def _movimentos():
    return [
        Movimento(TipoMovimento.SUPRIMENTO, D("50.00")),
        Movimento(TipoMovimento.SANGRIA, D("100.00")),
    ]


def test_valor_esperado_por_forma_de_pagamento():
    f = fechar_caixa(D("100.00"), _vendas_do_turno(), _movimentos(), contado={})
    # dinheiro = fundo 100 + vendas 109.90 + suprimento 50 - sangria 100
    assert f.esperado[F.DINHEIRO] == D("159.90")
    assert f.esperado[F.PIX] == D("150.00")
    assert f.esperado[F.DEBITO] == D("100.00")
    assert f.esperado[F.CREDITO] == D("259.80")


def test_total_de_vendas_ignora_canceladas():
    f = fechar_caixa(D("100.00"), _vendas_do_turno(), _movimentos(), contado={})
    assert f.total_vendas == D("619.70")


def test_caixa_que_confere():
    contado = {
        F.DINHEIRO: D("159.90"),
        F.PIX: D("150.00"),
        F.DEBITO: D("100.00"),
        F.CREDITO: D("259.80"),
    }
    f = fechar_caixa(D("100.00"), _vendas_do_turno(), _movimentos(), contado)
    assert all(v == D("0.00") for v in f.diferenca.values())
    assert f.status == "CONFERE"


def test_falta_e_sobra_aparecem_na_diferenca():
    contado = {
        F.DINHEIRO: D("149.90"),  # faltaram 10
        F.PIX: D("150.00"),
        F.DEBITO: D("100.00"),
        F.CREDITO: D("260.80"),  # sobrou 1
    }
    f = fechar_caixa(D("100.00"), _vendas_do_turno(), _movimentos(), contado)
    assert f.diferenca[F.DINHEIRO] == D("-10.00")
    assert f.diferenca[F.CREDITO] == D("1.00")
    assert f.diferenca[F.PIX] == D("0.00")
    assert f.status == "DIVERGENTE"


def test_forma_nao_informada_no_contado_vale_zero():
    contado = {F.DINHEIRO: D("159.90"), F.DEBITO: D("100.00"), F.CREDITO: D("259.80")}
    f = fechar_caixa(D("100.00"), _vendas_do_turno(), _movimentos(), contado)
    assert f.diferenca[F.PIX] == D("-150.00")


def test_turno_sem_vendas():
    f = fechar_caixa(D("100.00"), [], [], contado={F.DINHEIRO: D("100.00")})
    assert f.esperado[F.DINHEIRO] == D("100.00")
    assert f.esperado[F.PIX] == D("0.00")
    assert f.total_vendas == D("0.00")
    assert f.status == "CONFERE"
