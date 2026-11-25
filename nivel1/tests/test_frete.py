from decimal import Decimal as D

import pytest

from pdv.frete import Pacote, calcular_frete, peso_cubado, peso_taxado, regiao_por_cep


def test_peso_cubado():
    # 40 x 30 x 20 / 6000 = 4.000 kg
    assert peso_cubado(Pacote(D("1.2"), D("40"), D("30"), D("20"))) == D("4.000")


def test_peso_cubado_arredonda_em_3_casas():
    # 10 x 10 x 7 / 6000 = 0.11666... -> 0.117 (ROUND_HALF_UP)
    assert peso_cubado(Pacote(D("0.05"), D("10"), D("10"), D("7"))) == D("0.117")


def test_peso_taxado_usa_o_maior_entre_real_e_cubado():
    caixa_leve_e_grande = Pacote(D("1.2"), D("40"), D("30"), D("20"))
    caixa_pesada_e_pequena = Pacote(D("8.0"), D("20"), D("20"), D("20"))
    assert peso_taxado(caixa_leve_e_grande) == D("4.000")
    assert peso_taxado(caixa_pesada_e_pequena) == D("8.0")


@pytest.mark.parametrize(
    ("cep", "regiao"),
    [
        ("01310-100", "SUDESTE"),
        ("30140071", "SUDESTE"),
        ("50030-230", "NORDESTE"),
        ("40020-000", "NORDESTE"),
        ("69005-010", "NORTE"),
        ("70040-010", "CENTRO_OESTE"),
        ("80010-000", "SUL"),
        ("90010-150", "SUL"),
    ],
)
def test_regiao_por_cep(cep, regiao):
    assert regiao_por_cep(cep) == regiao


@pytest.mark.parametrize("cep", ["5003-230", "50030-2300", "ABCDE-123", "", "50030 230"])
def test_cep_invalido_gera_erro(cep):
    with pytest.raises(ValueError):
        regiao_por_cep(cep)


def test_frete_nordeste_faixa_ate_5kg():
    cotacao = calcular_frete(Pacote(D("1.2"), D("40"), D("30"), D("20")), "50030-230")
    assert cotacao.regiao == "NORDESTE"
    assert cotacao.peso_taxado == D("4.000")
    assert cotacao.valor == D("22.00")
    assert cotacao.prazo_dias == 4


def test_limite_da_faixa_e_inclusivo():
    # exatamente 1 kg ainda é a faixa "até 1 kg"
    cotacao = calcular_frete(Pacote(D("1.000"), D("10"), D("10"), D("10")), "01310-100")
    assert cotacao.valor == D("20.00")
    assert cotacao.prazo_dias == 5


def test_um_grama_acima_muda_de_faixa():
    cotacao = calcular_frete(Pacote(D("1.001"), D("10"), D("10"), D("10")), "01310-100")
    assert cotacao.valor == D("30.00")


def test_acima_de_30kg_nao_e_atendido():
    with pytest.raises(ValueError):
        calcular_frete(Pacote(D("30.5"), D("10"), D("10"), D("10")), "80010-000")


def test_medidas_zeradas_geram_erro():
    with pytest.raises(ValueError):
        calcular_frete(Pacote(D("1.0"), D("0"), D("10"), D("10")), "80010-000")
