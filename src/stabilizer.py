"""
This module outlines the user-facing classes for representing stabilizers and 2D topological quantum codes.
"""
from enum import Enum
from typing import Iterable

# Pauli operators are represented as an enum for clarity and type safety.
class Pauli(Enum):
    X = 0
    Z = 1
    Y = 2

class Stabilizer:
    def __init__(self, operator_dict: dict):
        self._paulis = [op for op in operator_dict.keys() if op in {"X", "Y", "Z"}]
        try:
            self._qubits = [int(q) for q in operator_dict.values()]
        except ValueError:
            raise ValueError("Qubit indices must be integers.")

    @classmethod
    def from_string(cls, operator_str: str):
        self = cls.__new__(cls)
        self._paulis = []
        self._qubits = []

        for op in operator_str.split():
            if not op:
                continue
            if op[0] not in {"X", "Y", "Z"}:
                raise ValueError(f"Invalid Pauli operator: {op[0]}")
            self._paulis.append(Pauli[op[0]])
            self._qubits.append(int(op[1:]))

        return self
    
    def __repr__(self):
        return f"Stabilizer({' '.join(str(p) + str(q) for p, q in zip(self._paulis, self._qubits))})"

# TODO: limited to surface codes for now
class TopologicalCode:
    def __init__(self, stabilizers: Iterable[Stabilizer]):
        if not stabilizers:
            raise ValueError("Stabilizers cannot be empty.")

        self._stabilizers = list(stabilizers)

    def validate_stabilisers(self):
        # placeholder for validation logic, just throw warnings for anti-commuting stabilizers
        pass

    def __repr__(self):
        return f"TopologicalCode({self._stabilizers})"
