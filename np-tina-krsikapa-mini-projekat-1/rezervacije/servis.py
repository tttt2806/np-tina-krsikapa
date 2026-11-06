"""Servis koji povezuje izvor podataka i izvještavače (injekcija zavisnosti)."""
from typing import Sequence

from .protokoli import Izvjestilac, IzvorPodataka


class ObradaRezervacija:
    def __init__(self, izvor: IzvorPodataka, izvjestioci: Sequence[Izvjestilac]) -> None:
        self.izvor = izvor
        self.izvjestioci = izvjestioci

    def obradi(self) -> list[float]:
        iznosi = [r.iznos for r in self.izvor.ucitaj()]
        for izvjestilac in self.izvjestioci:
            izvjestilac.izvjesti(iznosi)
        return iznosi
