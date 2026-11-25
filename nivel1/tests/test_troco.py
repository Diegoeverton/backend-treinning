from decimal import Decimal as D

import pytest

from pdv.troco import ValorInsuficienteError, calcular_troco


def test_sem_troco_quando_pagamento_exato():
    assert calcular_troco(D("50.00"), D("50.00")) == {}


def test_troco_simples_com_uma_nota():
    assert calcular_troco(D("30.00"), D("50.00")) == {D("20"): 1}


def test_troco_usa_menor_quantidade_de_notas_e_moedas():
    # 100 - 12.35 = 87.65 -> 50 + 20 + 10 + 5 + 2 + 0.50 + 0.10 + 0.05
    assert calcular_troco(D("12.35"), D("100.00")) == {
        D("50"): 1,
        D("20"): 1,
        D("10"): 1,
        D("5"): 1,
        D("2"): 1,
        D("0.50"): 1,
        D("0.10"): 1,
        D("0.05"): 1,
    }


def test_troco_repete_a_mesma_nota():
    # 200 - 0.40 = 199.60 -> 100 + 50 + 20 + 20 + 5 + 2 + 2 + 0.50 + 0.10
    assert calcular_troco(D("0.40"), D("200.00")) == {
        D("100"): 1,
        D("50"): 1,
        D("20"): 2,
        D("5"): 1,
        D("2"): 2,
        D("0.50"): 1,
        D("0.10"): 1,
    }


def test_troco_arredonda_para_baixo_no_multiplo_de_5_centavos():
    # 20 - 10.02 = 9.98 -> arredonda para 9.95
    assert calcular_troco(D("10.02"), D("20.00")) == {
        D("5"): 1,
        D("2"): 2,
        D("0.50"): 1,
        D("0.25"): 1,
        D("0.10"): 2,
    }


def test_valor_pago_menor_que_o_total_gera_erro():
    with pytest.raises(ValorInsuficienteError):
        calcular_troco(D("50.00"), D("49.99"))


def test_valores_negativos_geram_erro():
    with pytest.raises(ValueError):
        calcular_troco(D("-10.00"), D("20.00"))


def test_float_nao_e_aceito():
    # Dinheiro nunca em float: 0.1 + 0.2 != 0.3
    with pytest.raises(TypeError):
        calcular_troco(10.5, 20.0)
