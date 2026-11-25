
# VAMOS REFATIRAR USANDO Clean Architecture dividindo o problema em três camadas lógicas:


# Modelos de Domínio e Casos de Uso: Nossas dataclasses puras 
# e a função matemática (o que já temos).

# Camada de Acesso a Dados (Repository Pattern): O contrato de como salvar as coisas.

# Camada de Serviço (Service/Usecase): O maestro que orquestra a regra matemática e a persistência, garantindo a integridade transacional.


# =========================
# O CONTRATO DE REPOSITÓRIO (Repository Pattern)- INTERFACE
# =========================

from typing import Protocol
from dataclasses import dataclass
from decimal import Decimal

# importe os enums e dataclasses do caixa.py
# ---------------------------------------------------------
# DOMÍNIO: Entidades e Objetos de Valor
# ---------------------------------------------------------

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

class FechamentoRepository(Protocol):
    """Contrato (Interface) para o repositório de fechamento de caixa.
    
    Qualquer classe que implemente a persistência de dados (seja SQLAlchemy, 
    Motor assíncrono, ou um FakeRepository em memória para testes) deve 
    obrigatoriamente seguir esta exata assinatura.
    """
    
    def salvar(self, fechamento: Fechamento, operador_id: int) -> int:
        """
        Persiste o resultado de um fechamento de caixa.
        
        Args:
            fechamento (Fechamento): O objeto processado contendo os totais e status.
            operador_id (int): O identificador do operador responsável pelo turno.
            
        Returns:
            int: O ID (chave primária) gerado pelo banco de dados após a inserção.
        """
        ...
