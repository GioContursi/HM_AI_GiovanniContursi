from __future__ import annotations

from time import perf_counter


class Cronometro:
    def __init__(self) -> None:
        self._t0 = perf_counter()

    def ferma(self) -> float:
        return perf_counter() - self._t0
