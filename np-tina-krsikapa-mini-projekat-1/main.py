"""Ulazna tačka: sastavlja zavisnosti i pokreće obradu."""
import sys
from pathlib import Path

from rezervacije.izvjestaji import MailObavjestenje, TekstualniIzvjestaj
from rezervacije.izvori import CsvIzvor, JsonIzvor
from rezervacije.servis import ObradaRezervacija


def main(putanja: str) -> None:
    p = Path(putanja)
    izvor = JsonIzvor(p) if p.suffix == ".json" else CsvIzvor(p)
    servis = ObradaRezervacija(
        izvor, [TekstualniIzvjestaj(Path("izvjestaj.txt")), MailObavjestenje()]
    )
    servis.obradi()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "podaci/rezervacije.csv")
