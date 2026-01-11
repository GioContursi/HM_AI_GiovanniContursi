from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple

from .base_problem import Problema, Successore

Stato = Tuple[int, ...]


@dataclass(frozen=True)
class Azione:
    colonna: int
    riga: int


class NQueens(Problema[Stato, Azione]):
    def __init__(self, n: int):
        if n < 1:
            raise ValueError("n deve essere >= 1")
        self.n = n

    @property
    def stato_iniziale(self) -> Stato:
        return tuple()

    def e_obiettivo(self, stato: Stato) -> bool:
        return len(stato) == self.n

    def successori(self, stato: Stato) -> Iterable[Successore[Azione, Stato]]:
        k = len(stato)
        prossima_colonna = k + 1
        if prossima_colonna > self.n:
            return []

        succ: List[Successore[Azione, Stato]] = []
        for riga in range(1, self.n + 1):
            if self._posizione_valida(stato, prossima_colonna, riga):
                nuova = stato + (riga,)
                az = Azione(colonna=prossima_colonna, riga=riga)
                succ.append((az, nuova, 1.0))
        return succ

    def _posizione_valida(self, stato: Stato, colonna: int, riga: int) -> bool:
        for i, riga_i in enumerate(stato, start=1):
            if riga == riga_i:
                return False
            if abs(riga - riga_i) == abs(colonna - i):
                return False
        return True

    def stampa_stato(self, stato: Stato) -> str:
        return f"Stato(colonne={len(stato)}/{self.n}, righe={stato})"

    def stampa_azione(self, azione: Azione) -> str:
        return f"Metti regina in colonna {azione.colonna}, riga {azione.riga}"
