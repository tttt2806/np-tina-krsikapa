"""Konkretni izvori podataka. Novi izvor = nova klasa, servis se ne mijenja (princip O)."""
import csv
import json
from pathlib import Path

from .modeli import Rezervacija


class CsvIzvor:
    """CSV sa zaglavljem: gost,noci,cijena_noci."""

    def __init__(self, putanja: Path) -> None:
        self.putanja = putanja

    def ucitaj(self) -> list[Rezervacija]:
        with self.putanja.open(newline="", encoding="utf-8") as f:
            return [
                Rezervacija(red["gost"], int(red["noci"]), float(red["cijena_noci"]))
                for red in csv.DictReader(f)
            ]


class JsonIzvor:
    """JSON lista objekata sa poljima gost, noci, cijena_noci."""

    def __init__(self, putanja: Path) -> None:
        self.putanja = putanja

    def ucitaj(self) -> list[Rezervacija]:
        with self.putanja.open(encoding="utf-8") as f:
            return [
                Rezervacija(s["gost"], int(s["noci"]), float(s["cijena_noci"]))
                for s in json.load(f)
            ]
