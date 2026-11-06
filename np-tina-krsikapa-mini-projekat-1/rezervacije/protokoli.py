"""Ugovori (Protocol) za izvor podataka i za izvještavanje (princip D, I)."""
from typing import Protocol, Sequence

from .modeli import Rezervacija


class IzvorPodataka(Protocol):
    def ucitaj(self) -> list[Rezervacija]: ...


class Izvjestilac(Protocol):
    def izvjesti(self, iznosi: Sequence[float]) -> None: ...
