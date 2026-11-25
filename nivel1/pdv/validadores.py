"""Exercício 1.4 — Validadores.

Todas as funções devolvem True ou False (nunca lançam erro).

CPF
- Aceita com ou sem máscara: "529.982.247-25" ou "52998224725".
- 11 dígitos. Os dois últimos são dígitos verificadores (módulo 11):
    1º DV: multiplique os 9 primeiros dígitos por 10, 9, 8 ... 2, some,
           faça (soma * 10) % 11. Se der 10, vira 0.
    2º DV: o mesmo com os 10 primeiros dígitos e pesos 11, 10 ... 2.
- CPFs com todos os dígitos iguais (111.111.111-11) são inválidos.

CNPJ
- Aceita com ou sem máscara: "11.222.333/0001-81" ou "11222333000181".
- 14 dígitos, dois verificadores (módulo 11):
    1º DV: pesos 5,4,3,2,9,8,7,6,5,4,3,2 nos 12 primeiros dígitos.
    2º DV: pesos 6,5,4,3,2,9,8,7,6,5,4,3,2 nos 13 primeiros.
    Em ambos: resto = soma % 11; se resto < 2 o DV é 0, senão é 11 - resto.
- Todos os dígitos iguais -> inválido.

EAN-13 (código de barras dos produtos)
- Exatamente 13 dígitos, sem máscara.
- Nos 12 primeiros, posições ímpares (1ª, 3ª...) peso 1 e pares peso 3.
  DV = (10 - soma % 10) % 10.

CEP
- Só o formato: "50030-230" ou "50030230".

Rodar os testes:  pytest tests/test_validadores.py -v
"""

import re


def _digitos(texto: str) -> list[int]:
    """Converte '529.982' em [5, 2, 9, 9, 8, 2] (só os dígitos)."""
    return [int(c) for c in texto if c.isdigit()]


def validar_cpf(cpf: str) -> bool:
    # Aceita só "000.000.000-00" ou "00000000000" (nada de letras ou formatos estranhos).
    if not re.fullmatch(r"[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}|[0-9]{11}", cpf):
        return False
    d = _digitos(cpf)
    if len(set(d)) == 1:  # todos iguais (111.111.111-11) passam na conta, mas são inválidos
        return False

    for n_digitos, peso_inicial in ((9, 10), (10, 11)):
        pesos = range(peso_inicial, 1, -1)  # 10..2 no 1º DV, 11..2 no 2º
        soma = sum(digito * peso for digito, peso in zip(d[:n_digitos], pesos, strict=True))
        dv = (soma * 10) % 11
        if dv == 10:
            dv = 0
        if dv != d[n_digitos]:
            return False
    return True


def validar_cnpj(cnpj: str) -> bool:
    if not re.fullmatch(r"[0-9]{2}\.[0-9]{3}\.[0-9]{3}/[0-9]{4}-[0-9]{2}|[0-9]{14}", cnpj):
        return False
    d = _digitos(cnpj)
    if len(set(d)) == 1:
        return False

    pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos_2 = [6, *pesos_1]  # 6,5,4,3,2,9,8,7,6,5,4,3,2
    for n_digitos, pesos in ((12, pesos_1), (13, pesos_2)):
        soma = sum(digito * peso for digito, peso in zip(d[:n_digitos], pesos, strict=True))
        resto = soma % 11
        dv = 0 if resto < 2 else 11 - resto
        if dv != d[n_digitos]:
            return False
    return True


def validar_ean13(ean: str) -> bool:
    if not re.fullmatch(r"[0-9]{13}", ean):
        return False
    d = _digitos(ean)
    # índice 0 é a 1ª posição (ímpar, peso 1); índice 1 é a 2ª (par, peso 3)...
    soma = sum(digito * (1 if i % 2 == 0 else 3) for i, digito in enumerate(d[:12]))
    return (10 - soma % 10) % 10 == d[12]


def validar_cep(cep: str) -> bool:
    return re.fullmatch(r"[0-9]{5}-?[0-9]{3}", cep) is not None
