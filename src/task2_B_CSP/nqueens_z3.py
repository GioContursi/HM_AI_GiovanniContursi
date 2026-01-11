from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

import z3

from utils.metrics import Cronometro

SoluzioneCSP = Tuple[int, ...]


@dataclass(frozen=True)
class StatisticheCSP:
    tempo_sec: float
    sat: bool


def risolvi_nqueens_z3(n: int) -> Tuple[Optional[SoluzioneCSP], StatisticheCSP]:
    timer = Cronometro()

    if n < 1:
        raise ValueError("n deve essere >= 1")

    q = [z3.Int(f"q{i}") for i in range(1, n + 1)]

    vincoli: List[z3.BoolRef] = []

    for i in range(n):
        vincoli.append(z3.And(q[i] >= 1, q[i] <= n))

    vincoli.append(z3.Distinct(q))

    for i in range(n):
        for j in range(i + 1, n):
            vincoli.append(z3.Abs(q[i] - q[j]) != (j - i))

    s = z3.Solver()
    s.add(vincoli)

    esito = s.check()
    tempo = timer.ferma()

    if esito != z3.sat:
        return None, StatisticheCSP(tempo_sec=tempo, sat=False)

    m = s.model()
    soluzione = tuple(int(m.evaluate(q[i]).as_long()) for i in range(n))
    return soluzione, StatisticheCSP(tempo_sec=tempo, sat=True)
