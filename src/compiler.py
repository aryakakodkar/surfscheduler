"""
This module takes as input a topological code and a set of constraints and outputs a compiled
representation of the code that can be used by the schedule searcher.
"""
from typing import Callable, Iterable, Union
from collections import defaultdict

from .constraint import StabilizerPairContext
from .stabilizer import Stabilizer, TopologicalCode
from .expressions import Expression

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
        return self._topological_code.stabilizers # TODO: implement heuristic

class CompiledLocalConstraint:
    def __init__(self, constraint: Expression):
        pass
        
    def _check(stabilizers: Union[Stabilizer, Iterable[Stabilizer]]) -> Callable[[Iterable[int]]]:
        """
        Check if the given schedules satisfy the constraint.

        Returns
        -------
        A function that takes in a list of schedules and returns True if the constraint is satisfied.
        """
        pass

