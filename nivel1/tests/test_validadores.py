import pytest

from pdv.validadores import validar_cep, validar_cnpj, validar_cpf, validar_ean13

# ---------- CPF ----------


@pytest.mark.parametrize("cpf", ["529.982.247-25", "52998224725", "123.456.789-09"])
def test_cpf_valido(cpf):
    assert validar_cpf(cpf) is True


@pytest.mark.parametrize(
    "cpf",
    [
        "529.982.247-26",  # dígito verificador errado
        "111.111.111-11",  # todos iguais passam na conta, mas são inválidos
        "000.000.000-00",
        "5299822472",  # 10 dígitos
        "529.982.247-2a",
        "",
    ],
)
def test_cpf_invalido(cpf):
    assert validar_cpf(cpf) is False


# ---------- CNPJ ----------


@pytest.mark.parametrize("cnpj", ["11.222.333/0001-81", "11222333000181", "11.444.777/0001-61"])
def test_cnpj_valido(cnpj):
    assert validar_cnpj(cnpj) is True


@pytest.mark.parametrize(
    "cnpj",
    ["11.222.333/0001-82", "00.000.000/0000-00", "1122233300018", "11.222.333/0001-8X", ""],
)
def test_cnpj_invalido(cnpj):
    assert validar_cnpj(cnpj) is False


# ---------- EAN-13 (código de barras) ----------


@pytest.mark.parametrize("ean", ["7891000315507", "7897025021195", "4006381333931"])
def test_ean13_valido(ean):
    assert validar_ean13(ean) is True


@pytest.mark.parametrize(
    "ean", ["7891000315508", "789100031550", "78910003155070", "789100031550A", ""]
)
def test_ean13_invalido(ean):
    assert validar_ean13(ean) is False


# ---------- CEP (só formato) ----------


@pytest.mark.parametrize("cep", ["50030-230", "50030230"])
def test_cep_valido(cep):
    assert validar_cep(cep) is True


@pytest.mark.parametrize("cep", ["5003-0230", "5003023", "500302300", "50030 230", "ABCDE-FGH", ""])
def test_cep_invalido(cep):
    assert validar_cep(cep) is False
