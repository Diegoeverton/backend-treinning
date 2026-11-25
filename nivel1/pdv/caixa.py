"""Exercício 1.5 — Fechamento de caixa.

No fim do turno o operador conta o que tem em cada forma de pagamento e o
sistema compara com o que deveria ter.

Regras:
- esperado[DINHEIRO] = fundo de troco + vendas em dinheiro
                       + suprimentos - sangrias
- esperado das outras formas = soma das vendas naquela forma.
- Vendas canceladas não entram em nada.
- Uma venda pode ter vários pagamentos (ex.: parte no débito, parte em dinheiro).
- `esperado` e `diferenca` têm TODAS as formas de pagamento, mesmo as sem venda
  (valor 0.00).
- diferenca = contado - esperado (negativo = falta, positivo = sobra).
- Forma que não aparece em `contado` conta como 0.00.
- total_vendas = soma dos pagamentos das vendas não canceladas.
- status = "CONFERE" se todas as diferenças forem zero, senão "DIVERGENTE".

Rodar os testes:  pytest tests/test_caixa.py -v
"""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class FormaPagamento(Enum):
    DINHEIRO = "DINHEIRO"
    DEBITO = "DEBITO"
    CREDITO = "CREDITO"
    PIX = "PIX"


class TipoMovimento(Enum):
    SANGRIA = "SANGRIA"  # dinheiro retirado do caixa (ex.: levado ao cofre)
    SUPRIMENTO = "SUPRIMENTO"  # dinheiro colocado no caixa (ex.: reforço de troco)


@dataclass
class Pagamento:
    forma: FormaPagamento
    valor: Decimal


@dataclass
class Venda:
    id: int
    pagamentos: list[Pagamento]
    cancelada: bool = False


@dataclass
class Movimento:
    tipo: TipoMovimento
    valor: Decimal


@dataclass
class Fechamento:
    esperado: dict[FormaPagamento, Decimal]
    diferenca: dict[FormaPagamento, Decimal]
    total_vendas: Decimal
    status: str


def fechar_caixa(
    fundo_troco: Decimal,
    vendas: list[Venda],
    movimentos: list[Movimento],
    contado: dict[FormaPagamento, Decimal],
) -> Fechamento:
    zero = Decimal("0.00")

    # Passo 1: começamos com TODAS as formas de pagamento valendo 0.00.
    # Assim, formas sem nenhuma venda também aparecem no resultado.
    vendido = {forma: zero for forma in FormaPagamento}

    # Passo 2: somamos os pagamentos das vendas, pulando as canceladas.
    for venda in vendas:
        if venda.cancelada:
            continue
        for pagamento in venda.pagamentos:
            vendido[pagamento.forma] += pagamento.valor

    # Passo 3: o total de vendas é a soma de tudo que foi vendido.
    total_vendas = sum(vendido.values(), zero)

    # Passo 4: o esperado começa igual ao vendido...
    esperado = dict(vendido)

    # ...mas o DINHEIRO ainda recebe o fundo de troco e os movimentos do caixa.
    esperado[FormaPagamento.DINHEIRO] += fundo_troco
    for mov in movimentos:
        if mov.tipo == TipoMovimento.SUPRIMENTO:
            esperado[FormaPagamento.DINHEIRO] += mov.valor
        else:  # SANGRIA
            esperado[FormaPagamento.DINHEIRO] -= mov.valor

    # Passo 5: diferença = contado - esperado.
    # `contado.get(forma, zero)` devolve 0.00 quando a forma não foi informada.
    diferenca = {
        forma: contado.get(forma, zero) - esperado[forma] for forma in FormaPagamento
    }

    # Passo 6: só "CONFERE" se TODAS as diferenças forem zero.
    status = "CONFERE" if all(d == zero for d in diferenca.values()) else "DIVERGENTE"

    return Fechamento(
        esperado=esperado,
        diferenca=diferenca,
        total_vendas=total_vendas,
        status=status,
    )
