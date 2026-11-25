# Treino Backend — Logística e Frente de Loja

Projeto de estudo para retomar o desenvolvimento backend com **Python**, voltado a dois domínios do varejo:

- **Frente de loja (PDV):** caixa, vendas, estoque, trocas, condicional e fechamento de caixa em lojas de roupas e acessórios.
- **Logística:** pedidos, centros de distribuição, frete, rastreio e integração com transportadoras.

O treino é dividido em 4 níveis, do Python puro até a integração entre sistemas. Cada nível é uma pasta independente com seus próprios testes.

## Estrutura

```
treino-backend/
├── .venv/              # ambiente virtual compartilhado (não vai para o Git)
├── requirements.txt    # dependências de todos os níveis
├── README.md
├── nivel1/             # lógica com regras de negócio (Python puro)
├── nivel2/             # API REST de frente de loja
├── nivel3/             # API de logística
└── nivel4/             # integração entre sistemas
```

## Níveis

| Nível | Tema | Exercícios | Stack principal | Status |
| --- | --- | --- | --- | --- |
| 1 | Aquecimento: regras de PDV e logística | 1.1 a 1.5 | Python, Decimal, pytest | Em andamento |
| 2 | API REST de frente de loja + varejo de moda | 2.1 a 2.11 | FastAPI, SQLAlchemy, PostgreSQL, JWT | A fazer |
| 3 | API de logística | 3.1 a 3.5 | FastAPI, PostgreSQL | A fazer |
| 4 | Integração entre sistemas | 4.1 a 4.6 | Redis, httpx, SQLite, webhooks | A fazer |

### Nível 1 — Aquecimento

| # | Exercício | Arquivo |
| --- | --- | --- |
| 1.1 | Troco do caixa | `pdv/troco.py` |
| 1.2 | Carrinho com promoções | `pdv/carrinho.py` |
| 1.3 | Cálculo de frete | `pdv/frete.py` |
| 1.4 | Validadores (CPF, CNPJ, EAN-13, CEP) | `pdv/validadores.py` |
| 1.5 | Fechamento de caixa | `pdv/caixa.py` |

### Nível 2 — API de frente de loja

Cadastro de produtos, estoque por movimentações, venda no PDV com transação, cancelamento, login com perfis, relatórios em SQL, e o extra de varejo de moda: grade de cor e tamanho, troca e vale-troca, condicional, sincronização entre lojas e retaguarda, e uma tela de caixa desktop.

### Nível 3 — API de logística

Pedidos com máquina de estados, estoque por centro de distribuição, cotação de frete, rastreio público e ondas de separação.

### Nível 4 — Integração entre sistemas

Concorrência no estoque, idempotência, webhook de transportadora, fila de eventos com retry, PDV offline com sincronização e integração com sistema legado (arquivos e API externa de CEP).

## Como rodar

Requisitos: **Python 3.12+**. A partir do Nível 2: **Docker** e **Docker Compose** (PostgreSQL e Redis).

### 1. Criar a venv e instalar as dependências

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Rodar os testes de um nível

```bash
cd nivel1
pytest                          # todos os testes do nível
pytest tests/test_troco.py -v   # um exercício
pytest --cov=pdv                # com cobertura
```

### 3. Lint e formatação

```bash
ruff check .
ruff format .
```

## Como trabalhar em cada exercício

1. Leia a explicação no topo do arquivo do exercício.
2. Leia os testes: eles são a especificação.
3. Rode os testes e veja falhar.
4. Implemente até passar.
5. Refatore com os testes verdes.
6. Faça um commit por exercício, por exemplo `feat(nivel1): troco do caixa`.

## Convenções

- **Dinheiro sempre em `Decimal`, criado a partir de string:** `Decimal("0.10")`, nunca `Decimal(0.10)` nem `float`.
- **Arredondamento** com `ROUND_HALF_UP`, em 2 casas para valores e 3 casas para peso.
- **Toda regra de negócio tem teste.** Nenhum exercício está pronto sem os testes verdes.
- **Nomes de domínio em português** (venda, pedido, troco), para ficar próximo da linguagem do negócio.
- **Configurações e segredos** ficam em um arquivo `.env`, que não vai para o Git.

## .gitignore sugerido

```
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
.coverage
.env
*.db
```

## Tecnologias

Python · FastAPI · Pydantic · SQLAlchemy · Alembic · PostgreSQL · SQLite · Redis · Docker · pytest · ruff · JWT

## Autor

**Diego Silva**: [LinkedIn](https://www.linkedin.com/in/diego-evangelista-824436272/) · [GitHub](https://github.com/Diegoeverton)