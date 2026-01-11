from __future__ import annotations

from typing import Callable, Tuple

Stato = Tuple[int, ...]


def h0(_: Stato) -> float:
    return 0.0


def h_rimanenti(n: int) -> Callable[[Stato], float]:
    def h(stato: Stato) -> float:
        return float(n - len(stato))
    return h
