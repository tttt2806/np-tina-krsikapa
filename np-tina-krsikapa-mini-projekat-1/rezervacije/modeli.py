"""Domenski model: jedna rezervacija."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Rezervacija:
    gost: str
    noci: int
    cijena_noci: float

    def __post_init__(self) -> None:
        if self.noci <= 0:
            raise ValueError("Broj noćenja mora biti pozitivan")
        if self.cijena_noci < 0:
            raise ValueError("Cijena noćenja ne može biti negativna")

    @property
    def iznos(self) -> float:
        return self.noci * self.cijena_noci
