"""
This module takes as input a topological code and a set of constraints and outputs a compiled
representation of the code, constraints, and problem.
"""
from typing import Callable, Iterable, Union
from collections import defaultdict
from dataclasses import dataclass

from .stabilizer import Stabilizer, TopologicalCode
from .expressions import Expression, ConstantExpression, ABeforeBCount, BBeforeACount, And, Equal

@dataclass(frozen=True, slots=True)
class StabilizerPairContext():
    """
    A context for a pair of stabilizers, which can be used to define constraints on their scheduling.
    """
    shared_slots: Iterable[int]
    bits_per_layer: int

class CompiledTopologicalCode:
    def __init__(self, topological_code: TopologicalCode):
        self.topological_code = topological_code
        self.index_fn = topological_code.index_fn

# TODO: Need a user-facing Problem class
class CompiledProblem:
    def __init__(self, 
                 topological_code: TopologicalCode, 
                 constraints: Iterable[Expression],
                 stabilizer_order: Iterable[Stabilizer] = None):
        """
        A compiled representation of the schedule search problem. 

        Arguments
        ---------
        - topological_code: A TopologicalCode object representing the code to be scheduled.
        - constraints: A list of Expression objects representing the constraints on the schedule.
        - stabilizer_order: An optional list of Stabilizer objects representing the order in which to schedule the stabilizers. 
        If not provided, the order will be determined heuristcally based on constraints.
        """

        # take in constraints and separate by type
        self._code = topological_code
        self._constraints = constraints # compile?
        self._stabilizer_order = stabilizer_order if stabilizer_order is not None else self._determine_stabilizer_order()

    def _determine_stabilizer_order(self) -> Iterable[Stabilizer]:
        return self._code.stabilizers # TODO: implement heuristic

def evaluate_expression(expr: Expression, values: dict):
    """
    Evaluate an Expression object and return a boolean value.
    """
    if isinstance(expr, ConstantExpression):
        return expr.value
    elif isinstance(expr, ABeforeBCount) or isinstance(expr, BBeforeACount):
        return values[expr.name]
    elif isinstance(expr, And):
        return evaluate_expression(expr.left, values) and evaluate_expression(expr.right, values)
    elif isinstance(expr, Equal):
        return evaluate_expression(expr.left, values) == evaluate_expression(expr.right, values)
    else:
        raise NotImplementedError(f"The expression {expr.__class__.__name__} has not yet been implemented")

def collect_loop_values(expr: Expression):
    values = set()

    if isinstance(expr, ABeforeBCount) or isinstance(expr, BBeforeACount):
        values.add(expr.name)
    elif isinstance(expr, And) or isinstance(expr, Equal):
        values = values.union(collect_loop_values(expr.left)).union(collect_loop_values(expr.right))
    # ignore all other cases

    return values
