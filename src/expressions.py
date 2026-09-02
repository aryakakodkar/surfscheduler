"""
This is a helper module for users to define custom schedule constraints
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Union
from enum import Enum

# Enums for Relation.count_where() method
class Commutation(Enum):
    COMMUTING = 0
    ANTI_COMMUTING = 1

class Expression(ABC):
    """
    The base class representing any symbolic scheduling-constraint expression
    """
    def __eq__(self, other):
        return Equal(left=self, right=to_expr(other))

    def __and__(self, other):
        return And(left=self, right=to_expr(other))

    def __bool__(self):
        raise TypeError("Cannot evaluate an Expression as a boolean. Use '&' to compose relations.")

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"

@dataclass(frozen=True, slots=True, eq=False)
class ConstantExpression(Expression):
    """
    A constant value that can be used in constraints.
    """
    value: int

@dataclass(frozen=True, slots=True, eq=False)
class LocalLoopExpression(Expression):
    """
    Some local property which can be determined by looping through the shared supports of a set of stabilizers.
    For example, a_before_b_count()
    """
    pass

@dataclass(frozen=True, slots=True, eq=False)
class PredicateExpression(Expression):
    """
    A boolean expression which compares several sub-expressions
    """
    left: Expression
    right: Expression

# Return an expression or constant
def to_expr(value) -> Expression:
    if isinstance(value, Expression):
        return value

    return ConstantExpression(value)

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

# PREDICATES

@dataclass(frozen=True, slots=True, eq=False)
class Equal(PredicateExpression):
    """
    An equality constraint between two expressions.
    """
    pass

@dataclass(frozen=True, slots=True, eq=False)
class And(PredicateExpression):
    """
    A logical AND of multiple expressions.
    """
    pass

# LOCAL LOOP EXPRESSIONS

@dataclass(frozen=True, slots=True, eq=False)
class ABeforeBCount(LocalLoopExpression):
    """
    A count of the number of shared data qubits between two stabilizers A and B,
    where the ancilla or A is entangled with the shared data qubit before the ancilla of B.
    """
    name = "a_before_b_count"


@dataclass(frozen=True, slots=True, eq=False)
class BBeforeACount(LocalLoopExpression):
    """
    A count of the number of shared data qubits between two stabilizers A and B,
    where the ancilla of B is entangled before the ancilla of A.
    """
    name = "b_before_a_count"

# TODO: Deal with this
@dataclass(frozen=True, slots=True, eq=False)
class CountWhere(LocalLoopExpression):
    """
    A count expression conditioned on a commutation relation.
    """
    commutation: Commutation
