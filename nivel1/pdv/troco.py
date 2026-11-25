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
    # Passo 1: só aceitamos Decimal (float tem erro de precisão: 0.1 + 0.2 != 0.3).
    if not isinstance(total, Decimal) or not isinstance(pago, Decimal):
        raise TypeError("total e pago devem ser Decimal")

    # Passo 2: valores negativos não fazem sentido.
    if total < 0 or pago < 0:
        raise ValueError("Valores não podem ser negativos")

    # Passo 3: o cliente precisa ter pago pelo menos o total.
    if pago < total:
        raise ValorInsuficienteError("Valor pago é menor que o total")

    # Passo 4: arredonda o troco PARA BAIXO em múltiplos de 0,05.
    # `//` é a divisão inteira: 9.98 // 0.05 = 199, e 199 * 0.05 = 9.95.
    passo = Decimal("0.05")
    restante = ((pago - total) // passo) * passo

    # Passo 5: algoritmo guloso. Da maior para a menor denominação, vemos
    # quantas vezes ela cabe no que sobrou e descontamos.
    troco: dict[Decimal, int] = {}
    for denominacao in DENOMINACOES:
        quantidade, restante = divmod(restante, denominacao)
        if quantidade > 0:  # só entram as denominações usadas
            troco[denominacao] = int(quantidade)

    return troco
