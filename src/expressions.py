"""
This is a helper module for users to define custom schedule constraints
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Union
from enum import Enum

class Commutation(Enum):
    COMMUTING = 0
    ANTI_COMMUTING = 1

class Expression(ABC):
    def __eq__(self, other):
        return Equal(left=self, right=to_expr(other))

    def __and__(self, other):
        return And(left=self, right=to_expr(other))

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"

@dataclass(frozen=True, slots=True, eq=False)
class Constant(Expression):
    """
    A constant value that can be used in constraints.
    """
    value: int

# Return an expression or constant
def to_expr(value) -> Union[Expression, Constant]:
    if isinstance(value, Expression):
        return value

    return Constant(value)

class Relation():
    """
    A user-definable relation between stabilizer schedules. The user may build a relation
    using a number of pre-defined building blocks.
    """
    @property
    def a_before_b_count(self) -> Expression:
        return ABeforeBCount()

    @property
    def b_before_a_count(self) -> Expression:
        return BBeforeACount()

    def count_where(self, commutation: Commutation) -> Expression:
        return CountWhere(commutation)

@dataclass(frozen=True, slots=True, eq=False)
class Equal(Expression):
    """
    An equality constraint between two expressions.
    """
    left: Expression
    right: Union[Expression, Constant]

@dataclass(frozen=True, slots=True, eq=False)
class And(Expression):
    """
    A logical AND of multiple expressions.
    """
    left: Expression
    right: Union[Expression, Constant]

@dataclass(frozen=True, slots=True, eq=False)
class ABeforeBCount(Expression):
    """
    A count of the number of shared data qubits between two stabilizers A and B,
    where the ancilla or A is entangled with the shared data qubit before the ancilla of B.
    """
    pass


@dataclass(frozen=True, slots=True, eq=False)
class BBeforeACount(Expression):
    """
    A count of the number of shared data qubits between two stabilizers A and B,
    where the ancilla of B is entangled before the ancilla of A.
    """
    pass

# TODO: Deal with this
@dataclass(frozen=True, slots=True, eq=False)
class CountWhere(Expression):
    """
    A count expression conditioned on a commutation relation.
    """
    commutation: Commutation
