from decimal import Decimal as D

import pytest

from pdv.carrinho import Cupom, Item, calcular_carrinho


def test_subtotal_sem_promocoes():
    itens = [
        Item("CAM-01", "Camiseta", 2, D("49.90")),
        Item("MEI-01", "Meia", 1, D("15.00")),
    ]
    r = calcular_carrinho(itens)
    assert r.subtotal == D("114.80")
    assert r.desconto_leve3pague2 == D("0.00")
    assert r.desconto_progressivo == D("0.00")
    assert r.desconto_cupom == D("0.00")
    assert r.total == D("114.80")


def test_leve3_pague2_da_uma_unidade_gratis_a_cada_tres():
    itens = [Item("MEI-01", "Meia", 7, D("15.00"))]
    r = calcular_carrinho(itens, skus_leve3pague2={"MEI-01"})
    assert r.subtotal == D("105.00")
    assert r.desconto_leve3pague2 == D("30.00")  # 7 // 3 = 2 grátis
    assert r.total == D("75.00")


def test_leve3_pague2_soma_linhas_repetidas_do_mesmo_sku():
    itens = [
        Item("MEI-01", "Meia", 2, D("15.00")),
        Item("MEI-01", "Meia", 1, D("15.00")),
    ]
    r = calcular_carrinho(itens, skus_leve3pague2={"MEI-01"})
    assert r.desconto_leve3pague2 == D("15.00")


def test_leve3_pague2_so_vale_para_o_sku_em_promocao():
    itens = [Item("CAM-01", "Camiseta", 3, D("49.90"))]
    r = calcular_carrinho(itens, skus_leve3pague2={"MEI-01"})
    assert r.desconto_leve3pague2 == D("0.00")


def test_desconto_progressivo_nao_vale_com_exatamente_200():
    itens = [Item("CAL-01", "Calça", 1, D("200.00"))]
    r = calcular_carrinho(itens)
    assert r.desconto_progressivo == D("0.00")
    assert r.total == D("200.00")


def test_desconto_progressivo_de_10_porcento_acima_de_200():
    itens = [Item("CAL-01", "Calça", 1, D("200.01"))]
    r = calcular_carrinho(itens)
    assert r.desconto_progressivo == D("20.00")  # 20.001 arredondado
    assert r.total == D("180.01")


def test_progressivo_e_calculado_depois_do_leve3_pague2():
    # subtotal 240, leve3 tira 60 -> sobra 180, que NÃO passa de 200
    itens = [Item("BON-01", "Boné", 4, D("60.00"))]
    r = calcular_carrinho(itens, skus_leve3pague2={"BON-01"})
    assert r.desconto_leve3pague2 == D("60.00")
    assert r.desconto_progressivo == D("0.00")
    assert r.total == D("180.00")


def test_ordem_completa_leve3_depois_progressivo_depois_cupom():
    itens = [
        Item("CAM-01", "Camiseta", 3, D("50.00")),
        Item("JAQ-01", "Jaqueta", 1, D("199.90")),
    ]
    r = calcular_carrinho(itens, skus_leve3pague2={"CAM-01"}, cupom=Cupom("BEMVINDO", D("25.00")))
    assert r.subtotal == D("349.90")
    assert r.desconto_leve3pague2 == D("50.00")
    assert r.desconto_progressivo == D("29.99")  # 10% de 299.90
    assert r.desconto_cupom == D("25.00")
    assert r.total == D("244.91")


def test_cupom_nunca_deixa_o_total_negativo():
    itens = [Item("MEI-01", "Meia", 1, D("15.00"))]
    r = calcular_carrinho(itens, cupom=Cupom("VALE50", D("50.00")))
    assert r.desconto_cupom == D("15.00")
    assert r.total == D("0.00")


def test_quantidade_zero_ou_negativa_gera_erro():
    with pytest.raises(ValueError):
        calcular_carrinho([Item("MEI-01", "Meia", 0, D("15.00"))])


def test_carrinho_vazio_gera_erro():
    with pytest.raises(ValueError):
        calcular_carrinho([])
