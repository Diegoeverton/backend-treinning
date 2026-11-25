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

from dataclasses import dataclass
from decimal import Decimal

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


def peso_cubado(pacote: Pacote) -> Decimal:
    raise NotImplementedError


def peso_taxado(pacote: Pacote) -> Decimal:
    raise NotImplementedError


def regiao_por_cep(cep: str) -> str:
    # Dica: o módulo `re` (expressões regulares) resolve a validação em uma linha.
    raise NotImplementedError


def calcular_frete(pacote: Pacote, cep_destino: str) -> Cotacao:
    raise NotImplementedError
