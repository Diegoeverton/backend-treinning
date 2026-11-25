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


def validar_cpf(cpf: str) -> bool:
    raise NotImplementedError


def validar_cnpj(cnpj: str) -> bool:
    raise NotImplementedError


def validar_ean13(ean: str) -> bool:
    raise NotImplementedError


def validar_cep(cep: str) -> bool:
    raise NotImplementedError
