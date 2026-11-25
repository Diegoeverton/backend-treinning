"""Exercício 1.2 — Carrinho com promoções.

Regras, aplicadas NESTA ordem:
1. Leve 3, pague 2: vale para os SKUs em `skus_leve3pague2`. A cada 3 unidades
   do mesmo SKU, 1 sai de graça. Linhas repetidas do mesmo SKU somam as
   quantidades antes da conta (2 + 1 = 3 unidades -> 1 grátis).
2. Desconto progressivo: 10% sobre o valor que sobrou depois do passo 1,
   somente se esse valor for MAIOR que R$ 200,00 (exatamente 200 não ganha).
3. Cupom: desconto de valor fixo sobre o que sobrou. O total nunca fica
   negativo, então o desconto do cupom fica limitado ao valor restante.

Outras regras:
- Cada desconto é arredondado em 2 casas com ROUND_HALF_UP.
- Carrinho vazio ou item com quantidade <= 0 -> ValueError.

Rodar os testes:  pytest tests/test_carrinho.py -v
"""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


@dataclass
class Item:
    sku: str
    descricao: str
    quantidade: int
    preco_unitario: Decimal


@dataclass
class Cupom:
    codigo: str
    valor: Decimal


@dataclass
class ResumoCarrinho:
    subtotal: Decimal
    desconto_leve3pague2: Decimal
    desconto_progressivo: Decimal
    desconto_cupom: Decimal
    total: Decimal


def calcular_carrinho(
    itens: list[Item],
    skus_leve3pague2: set[str] = frozenset(),
    cupom: Cupom | None = None,
) -> ResumoCarrinho:
    centavo = Decimal("0.01")
    zero = Decimal("0.00")

    def arredondar(valor: Decimal) -> Decimal:
        return valor.quantize(centavo, rounding=ROUND_HALF_UP)

    # Passo 0: validações.
    if not itens:
        raise ValueError("Carrinho vazio")
    if any(item.quantidade <= 0 for item in itens):
        raise ValueError("Quantidade deve ser maior que zero")

    # Passo 1: subtotal = soma de quantidade * preço de cada linha.
    subtotal = arredondar(sum((i.quantidade * i.preco_unitario for i in itens), zero))

    # Passo 2: leve 3, pague 2.
    # Primeiro agrupamos por SKU (linhas repetidas somam as quantidades).
    quantidades: dict[str, int] = {}
    precos: dict[str, Decimal] = {}
    for item in itens:
        quantidades[item.sku] = quantidades.get(item.sku, 0) + item.quantidade
        precos.setdefault(item.sku, item.preco_unitario)  # preço da 1ª linha do SKU

    desconto_leve3 = zero
    for sku, qtd in quantidades.items():
        if sku in skus_leve3pague2:
            gratis = qtd // 3  # divisão inteira: a cada 3, 1 sai de graça
            desconto_leve3 += gratis * precos[sku]
    desconto_leve3 = arredondar(desconto_leve3)
    restante = subtotal - desconto_leve3

    # Passo 3: 10% se o que sobrou for MAIOR que 200 (200 exato não ganha).
    desconto_progressivo = zero
    if restante > Decimal("200.00"):
        desconto_progressivo = arredondar(restante * Decimal("0.10"))
    restante -= desconto_progressivo

    # Passo 4: cupom, limitado ao que sobrou (total nunca fica negativo).
    desconto_cupom = zero
    if cupom is not None:
        desconto_cupom = arredondar(min(cupom.valor, restante))
    restante -= desconto_cupom

    return ResumoCarrinho(
        subtotal=subtotal,
        desconto_leve3pague2=desconto_leve3,
        desconto_progressivo=desconto_progressivo,
        desconto_cupom=desconto_cupom,
        total=restante,
    )
