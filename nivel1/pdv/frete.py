"""Exercício 1.3 — Cálculo de frete.

Regras:
- Peso cubado = comprimento x largura x altura (cm) / 6000, em kg,
  arredondado em 3 casas com ROUND_HALF_UP.
- Peso taxado = o MAIOR entre o peso real e o peso cubado.
- A região sai do primeiro dígito do CEP (tabela REGIOES abaixo).
  CEP aceito: "50030-230" ou "50030230". Qualquer outro formato -> ValueError.
- O preço e o prazo saem da TABELA_FRETE pela primeira faixa em que
  peso_taxado <= limite (o limite é inclusivo: 1,000 kg ainda é "até 1 kg").
- Acima de 30 kg não é atendido -> ValueError.
- Peso ou qualquer medida menor ou igual a zero -> ValueError.

Obs.: a divisão por região é simplificada para o treino.

Rodar os testes:  pytest tests/test_frete.py -v
"""

import re
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

D = Decimal

# primeiro dígito do CEP -> região
REGIOES = {
    "0": "SUDESTE", "1": "SUDESTE", "2": "SUDESTE", "3": "SUDESTE",
    "4": "NORDESTE", "5": "NORDESTE",
    "6": "NORTE",
    "7": "CENTRO_OESTE",
    "8": "SUL", "9": "SUL",
}  # fmt: skip

# região -> lista de (limite da faixa em kg, valor em R$, prazo em dias)
TABELA_FRETE = {
    "NORDESTE":     [(D("1"), D("15.00"), 3), (D("5"), D("22.00"), 4), (D("10"), D("35.00"), 5), (D("30"), D("60.00"), 6)],
    "SUDESTE":      [(D("1"), D("20.00"), 5), (D("5"), D("30.00"), 6), (D("10"), D("45.00"), 7), (D("30"), D("80.00"), 8)],
    "CENTRO_OESTE": [(D("1"), D("22.00"), 6), (D("5"), D("33.00"), 7), (D("10"), D("50.00"), 8), (D("30"), D("90.00"), 9)],
    "SUL":          [(D("1"), D("25.00"), 7), (D("5"), D("36.00"), 8), (D("10"), D("55.00"), 9), (D("30"), D("95.00"), 10)],
    "NORTE":        [(D("1"), D("28.00"), 8), (D("5"), D("40.00"), 9), (D("10"), D("62.00"), 10), (D("30"), D("110.00"), 12)],
}  # fmt: skip


@dataclass
class Pacote:
    peso_kg: Decimal
    comprimento_cm: Decimal
    largura_cm: Decimal
    altura_cm: Decimal


@dataclass
class Cotacao:
    regiao: str
    peso_taxado: Decimal
    valor: Decimal
    prazo_dias: int


def _validar(pacote: Pacote) -> None:
    """Peso e medidas precisam ser maiores que zero."""
    medidas = (pacote.peso_kg, pacote.comprimento_cm, pacote.largura_cm, pacote.altura_cm)
    if any(m <= 0 for m in medidas):
        raise ValueError("Peso e medidas devem ser maiores que zero")


def peso_cubado(pacote: Pacote) -> Decimal:
    _validar(pacote)
    volume = pacote.comprimento_cm * pacote.largura_cm * pacote.altura_cm
    return (volume / D("6000")).quantize(D("0.001"), rounding=ROUND_HALF_UP)


def peso_taxado(pacote: Pacote) -> Decimal:
    # max() devolve o maior dos dois valores
    return max(pacote.peso_kg, peso_cubado(pacote))


def regiao_por_cep(cep: str) -> str:
    # fullmatch exige que o texto INTEIRO siga o padrão: 5 dígitos, hífen opcional, 3 dígitos.
    # Usamos [0-9] em vez de \d porque \d também aceitaria dígitos de outros alfabetos.
    if not re.fullmatch(r"[0-9]{5}-?[0-9]{3}", cep):
        raise ValueError(f"CEP inválido: {cep!r}")
    return REGIOES[cep[0]]


def calcular_frete(pacote: Pacote, cep_destino: str) -> Cotacao:
    regiao = regiao_por_cep(cep_destino)
    taxado = peso_taxado(pacote)  # também valida peso e medidas

    # Percorre as faixas em ordem e fica com a primeira em que o peso cabe.
    for limite, valor, prazo in TABELA_FRETE[regiao]:
        if taxado <= limite:  # <= torna o limite inclusivo
            return Cotacao(regiao=regiao, peso_taxado=taxado, valor=valor, prazo_dias=prazo)

    raise ValueError("Peso acima de 30 kg: não atendido")
