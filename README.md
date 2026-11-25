# Nível 1 — Aquecimento: lógica com regras de negócio

Python puro, sem API e sem banco. Os testes já estão prontos em `tests/`.
Seu trabalho é completar as funções em `pdv/` até todos os testes passarem.

## Como trabalhar

```bash
cd nivel1
pytest tests/test_troco.py -v     # um exercício por vez
pytest                            # tudo
ruff check . && ruff format .     # lint e formatação
```

Ciclo sugerido para cada exercício:

1. Leia a explicação no topo do arquivo em `pdv/`.
2. Leia os testes: eles são a especificação.
3. Rode os testes e veja falhar.
4. Implemente até passar.
5. Refatore com os testes verdes.
6. Faça um commit.

## Exercícios

| # | Arquivo | Testes | O que treina |
| --- | --- | --- | --- |
| 1.1 | `pdv/troco.py` | 8 | Decimal, algoritmo guloso, exceções próprias |
| 1.2 | `pdv/carrinho.py` | 11 | dataclasses, agrupamento, ordem de regras, arredondamento |
| 1.3 | `pdv/frete.py` | 21 | regex, tabelas de regra, limites de faixa |
| 1.4 | `pdv/validadores.py` | 33 | algoritmos de dígito verificador, testes parametrizados |
| 1.5 | `pdv/caixa.py` | 6 | Enum, acumuladores, regras de conciliação |

## Regra de ouro

Dinheiro sempre em `Decimal`, criado a partir de **string**:

```python
Decimal("0.10")  # certo
Decimal(0.10)  # errado: vira 0.1000000000000000055511151231257827...
```

## Desafio extra

Depois de terminar, escreva você mesmo 2 testes novos para cada exercício,
pensando em casos de borda que eu não cobri.
# backend-treinning
