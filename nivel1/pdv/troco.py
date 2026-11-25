"""Exercício 1.1 — Troco do caixa.

Regras:
- Recebe o total da venda e o valor pago, ambos em Decimal.
- Devolve um dicionário {denominação: quantidade} usando a MENOR quantidade
  possível de notas e moedas. Só entram as denominações usadas.
- Sem troco (pagamento exato) -> dicionário vazio.
- O troco é arredondado PARA BAIXO até o múltiplo de R$ 0,05 mais próximo
  (não existem moedas de 1 centavo circulando no caixa).
- Valor pago menor que o total -> ValorInsuficienteError.
- Valores negativos -> ValueError.
- Se receber float em vez de Decimal -> TypeError.

Rodar os testes:  pytest tests/test_troco.py -v
"""

from decimal import Decimal

DENOMINACOES = [
    Decimal(valor)
    for valor in ("200", "100", "50", "20", "10", "5", "2", "1", "0.50", "0.25", "0.10", "0.05")
]


class ValorInsuficienteError(ValueError):
    """O cliente pagou menos do que o total da venda."""


def calcular_troco(total: Decimal, pago: Decimal) -> dict[Decimal, int]:
    # Dica: pense em "quantas vezes cabe a maior nota?" e vá descendo a lista.
    raise NotImplementedError
