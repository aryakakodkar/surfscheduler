"""
This module defines the abstract Constraint class, which is used to define arbitrary constraints on the scheduling
of stabilisers in a topological code.
"""
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Union

from .stabilizer import Stabilizer


class Constraint(ABC):
    @abstractmethod
    def is_satisfied(self, value: Union[Stabilizer, Iterable[Stabilizer]]) -> bool:
        pass

    @abstractmethod
    def applies_to(self, stabilizer: Stabilizer) -> bool:
        pass
