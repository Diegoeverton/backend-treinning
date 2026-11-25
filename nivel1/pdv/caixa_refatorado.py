"""Fechamento de caixa refatorado em camadas (Clean Architecture simplificada).

Três camadas lógicas, de dentro para fora:

1. DOMÍNIO / CASO DE USO  -> pdv/caixa.py
   Dataclasses puras e a função `fechar_caixa` (só matemática, sem I/O).
   Não conhece banco de dados nem este módulo.

2. REPOSITÓRIO (contrato)  -> `FechamentoRepository` abaixo
   Uma interface (Protocol) que diz COMO salvar, sem dizer ONDE.
   Em produção seria SQLAlchemy; nos testes, o `RepositorioEmMemoria`.

3. SERVIÇO                 -> `FechamentoService` abaixo
   O maestro: chama a regra de negócio e depois manda persistir.
   Depende do contrato, nunca de um banco concreto (inversão de dependência).

A seta de dependência sempre aponta para dentro:
    serviço -> contrato -> domínio
"""

from typing import Protocol

from pdv.caixa import (
    Fechamento,
    FormaPagamento,
    Movimento,
    Venda,
    fechar_caixa,
)
from decimal import Decimal

# ---------------------------------------------------------
# CAMADA DE ACESSO A DADOS: contrato (Repository Pattern)
# ---------------------------------------------------------


class FechamentoRepository(Protocol):
    """Contrato (interface) para o repositório de fechamento de caixa.

    Qualquer classe que tenha um método `salvar` com esta assinatura serve
    (SQLAlchemy, Motor assíncrono, ou um repositório em memória para testes).
    O Protocol usa "tipagem estrutural": não é preciso herdar dele.
    """

    def salvar(self, fechamento: Fechamento, operador_id: int) -> int:
        """Persiste o resultado de um fechamento de caixa.

        Args:
            fechamento: o objeto processado contendo os totais e o status.
            operador_id: identificador do operador responsável pelo turno.

        Returns:
            O ID (chave primária) gerado após a inserção.
        """
        ...


class RepositorioEmMemoria:
    """Implementação falsa (fake) do contrato, para testes e para o treino.

    Guarda os fechamentos numa lista em vez de um banco de dados.
    """

    def __init__(self) -> None:
        self.registros: dict[int, tuple[Fechamento, int]] = {}
        self._proximo_id = 1

    def salvar(self, fechamento: Fechamento, operador_id: int) -> int:
        novo_id = self._proximo_id
        self.registros[novo_id] = (fechamento, operador_id)
        self._proximo_id += 1
        return novo_id


# ---------------------------------------------------------
# CAMADA DE SERVIÇO: orquestra regra de negócio + persistência
# ---------------------------------------------------------


class FechamentoService:
    """Caso de uso "fechar o caixa do turno".

    Recebe o repositório pelo construtor (injeção de dependência). Assim o
    serviço não sabe se está gravando em Postgres ou em memória.
    """

    def __init__(self, repositorio: FechamentoRepository) -> None:
        self._repositorio = repositorio

    def fechar_e_salvar(
        self,
        operador_id: int,
        fundo_troco: Decimal,
        vendas: list[Venda],
        movimentos: list[Movimento],
        contado: dict[FormaPagamento, Decimal],
    ) -> tuple[int, Fechamento]:
        """Calcula o fechamento e o persiste. Devolve (id_gerado, fechamento).

        Primeiro calcula; só persiste se o cálculo deu certo. Assim, se a regra
        de negócio lançar erro, nada é gravado pela metade.
        """
        fechamento = fechar_caixa(fundo_troco, vendas, movimentos, contado)
        fechamento_id = self._repositorio.salvar(fechamento, operador_id)
        return fechamento_id, fechamento
