"""Observer pattern: praćenje toka treninga."""
from abc import ABC, abstractmethod


class Posmatrac(ABC):
    @abstractmethod
    def azuriraj(self, dogadjaj: str, podaci: dict) -> None:
        ...


class Subjekt:
    def __init__(self):
        self._posmatraci = []

    def pretplati(self, posmatrac: Posmatrac):
        self._posmatraci.append(posmatrac)

    def odjavi(self, posmatrac: Posmatrac):
        self._posmatraci.remove(posmatrac)

    def obavijesti(self, dogadjaj, **podaci):
        for p in self._posmatraci:
            p.azuriraj(dogadjaj, podaci)


class KonzolniLogger(Posmatrac):
    def azuriraj(self, dogadjaj, podaci):
        print(f"[{dogadjaj}] {podaci}")


class Istorija(Posmatrac):
    """Pamti sve događaje (korisno i za testove)."""

    def __init__(self):
        self.dogadjaji = []

    def azuriraj(self, dogadjaj, podaci):
        self.dogadjaji.append((dogadjaj, podaci))
