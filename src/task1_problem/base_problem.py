from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Hashable, Iterable, Optional, Protocol, Tuple, TypeVar


StatoT = TypeVar("StatoT", bound=Hashable)
AzioneT = TypeVar("AzioneT")
Successore = Tuple[AzioneT, StatoT, float]

class Problema(Protocol, Generic[StatoT, AzioneT]):

    @property
    def stato_iniziale(self) -> StatoT:
        ...

    def e_obiettivo(self, stato: StatoT) -> bool:
        ...

    def successori(self, stato: StatoT) -> Iterable[Successore[AzioneT, StatoT]]:
        ...

    def stampa_stato(self, stato: StatoT) -> str:
        return str(stato)

    def stampa_azione(self, azione: AzioneT) -> str:
        return str(azione)


@dataclass(frozen=True)
class Soluzione(Generic[StatoT, AzioneT]):
    azioni: Tuple[AzioneT, ...]
    stati: Tuple[StatoT, ...]
    costo_totale: float

    def __len__(self) -> int:
        return len(self.azioni)

    @property
    def ultimo_stato(self) -> Optional[StatoT]:
        return self.stati[-1] if self.stati else None