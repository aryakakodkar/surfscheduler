"""
This module defines the abstract Constraint class, which is used to define arbitrary constraints on the scheduling
of stabilisers in a topological code.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Union

from .stabilizer import Stabilizer

@dataclass(frozen=True, slots=True)
class StabilizerPairContext():
    """
    A context for a pair of stabilizers, which can be used to define constraints on their scheduling.
    """
    shared_slots: Iterable[int]
    bits_per_layer: int
