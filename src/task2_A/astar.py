from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Callable, Dict, Hashable, List, Optional, Tuple, TypeVar

from task1_problem.base_problem import Problema, Soluzione
from utils.metrics import Cronometro

StatoT = TypeVar("StatoT", bound=Hashable)
AzioneT = TypeVar("AzioneT")


@dataclass(frozen=True)
class StatisticheAStar:
    tempo_sec: float
    nodi_estratti: int
    nodi_espansi: int
    nodi_generati: int
    max_frontiera: int


def a_star(
    problema: Problema[StatoT, AzioneT],
    euristica: Callable[[StatoT], float],
    tie_break: str = "g_alto",
) -> Tuple[Optional[Soluzione[StatoT, AzioneT]], StatisticheAStar]:
    timer = Cronometro()

    if tie_break not in {"g_alto", "g_basso"}:
        raise ValueError("tie_break deve essere 'g_alto' oppure 'g_basso'")

    stato0 = problema.stato_iniziale

    frontiera: List[Tuple[float, float, int, StatoT]] = []
    contatore = 0

    g_score: Dict[StatoT, float] = {stato0: 0.0}
    padre: Dict[StatoT, Tuple[Optional[StatoT], Optional[AzioneT]]] = {stato0: (None, None)}

    chiusi: set[StatoT] = set()

    f0 = float(euristica(stato0))
    heapq.heappush(frontiera, (f0, 0.0, contatore, stato0))

    nodi_estratti = 0
    nodi_espansi = 0
    nodi_generati = 1
    max_frontiera = 1

    while frontiera:
        if len(frontiera) > max_frontiera:
            max_frontiera = len(frontiera)

        f_corr, tie_corr, _, stato = heapq.heappop(frontiera)
        nodi_estratti += 1

        if stato in chiusi:
            continue

        if problema.e_obiettivo(stato):
            sol = _ricostruisci_soluzione(stato, padre, g_score[stato])
            tempo = timer.ferma()
            stats = StatisticheAStar(tempo, nodi_estratti, nodi_espansi, nodi_generati, max_frontiera)
            return sol, stats

        chiusi.add(stato)
        nodi_espansi += 1

        g_stato = g_score[stato]

        for azione, prossimo, costo_passo in problema.successori(stato):
            nodi_generati += 1

            if prossimo in chiusi:
                continue

            g_nuovo = g_stato + float(costo_passo)

            g_vecchio = g_score.get(prossimo)
            if g_vecchio is None or g_nuovo < g_vecchio:
                g_score[prossimo] = g_nuovo
                padre[prossimo] = (stato, azione)

                h = float(euristica(prossimo))
                f = g_nuovo + h

                tie = -g_nuovo if tie_break == "g_alto" else g_nuovo

                contatore += 1
                heapq.heappush(frontiera, (f, tie, contatore, prossimo))

    tempo = timer.ferma()
    stats = StatisticheAStar(tempo, nodi_estratti, nodi_espansi, nodi_generati, max_frontiera)
    return None, stats


def _ricostruisci_soluzione(
    stato_goal: StatoT,
    padre: Dict[StatoT, Tuple[Optional[StatoT], Optional[AzioneT]]],
    costo_totale: float,
) -> Soluzione[StatoT, AzioneT]:
    stati: List[StatoT] = []
    azioni: List[AzioneT] = []

    cur: Optional[StatoT] = stato_goal
    while cur is not None:
        stati.append(cur)
        prev, az = padre[cur]
        if az is not None:
            azioni.append(az)
        cur = prev

    stati.reverse()
    azioni.reverse()
    return Soluzione(azioni=tuple(azioni), stati=tuple(stati), costo_totale=costo_totale)
