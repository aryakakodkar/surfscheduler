"""
This module outlines the user-facing classes for representing stabilizers and 2D topological quantum codes.
"""
from collections import defaultdict
from enum import Enum
from typing import Callable, Iterable

# Pauli operators are represented as an enum for clarity and type safety.
class Pauli(Enum):
    X = 0
    Z = 1
    Y = 2

class Stabilizer:
    def __init__(self, operator_dict: dict):
        # TODO: Validate
        self._operator_dict = operator_dict
        self.weight = sum(len(qubits) for qubits in operator_dict.values())

    @classmethod
    def from_string(cls, operator_str: str):
        self = cls.__new__(cls)
        self._operator_dict = {"X": [], "Y": [], "Z": []}

        for op in operator_str.split():
            if not op:
                continue
            if op[0] not in {"X", "Y", "Z"}:
                raise ValueError(f"Invalid Pauli operator: {op[0]}")
            
            try:
                self._operator_dict[op[0]].append(int(op[1:]))
                self.weight += 1
            except ValueError:
                raise ValueError(f"Invalid qubit index: {op[1:]}")
            
        return self

    @property
    def operator_signature(self):
        return (len(self._operator_dict["X"]),
                len(self._operator_dict["Y"]),
                len(self._operator_dict["Z"])) # return the number of X, Y, Z operators in the stabilizer

    def __eq__(self, otherStabilizer):
        if not isinstance(otherStabilizer, Stabilizer):
            return False

        return self._operator_dict == otherStabilizer._operator_dict
    
    def __repr__(self):
        return f"Stabilizer({self._operator_dict})"

# TODO: limited to surface codes for now
# TODO: need to add an internal geometric structure here, so that we can tell which stabilizers are s
#       similar to which other stabilizers in the schedule-finding compilation step.
class TopologicalCode:
    def __init__(self, stabilizers: Iterable[Stabilizer], index_fn: Callable[[Stabilizer], int]):
        if not stabilizers:
            raise ValueError("Stabilizers cannot be empty.")

        self.index_fn = index_fn
        # see if this should be private or public
        self.stabilizers = set(stabilizers)

    def validate_stabilisers(self):
        # placeholder for validation logic, just throw warnings for anti-commuting stabilizers
        pass

    def __repr__(self):
        return f"TopologicalCode({self.stabilizers})"

