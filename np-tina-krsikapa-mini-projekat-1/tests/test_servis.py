from pathlib import Path

import pytest

from rezervacije.izvjestaji import TekstualniIzvjestaj
from rezervacije.izvori import CsvIzvor, JsonIzvor
from rezervacije.modeli import Rezervacija
from rezervacije.servis import ObradaRezervacija


class LazniIzvor:
    """Zamjenski izvor podataka: ne dira datoteke."""

    def __init__(self, rezervacije: list[Rezervacija]) -> None:
        self.rezervacije = rezervacije

    def ucitaj(self) -> list[Rezervacija]:
        return self.rezervacije


class LazniIzvjestilac:
    def __init__(self) -> None:
        self.primljeno: list[list[float]] = []

    def izvjesti(self, iznosi) -> None:
        self.primljeno.append(list(iznosi))


def test_servis_racuna_iznose_sa_zamjenskim_izvorom():
    izvor = LazniIzvor([Rezervacija("Ana", 3, 80), Rezervacija("Marko", 5, 65)])
    assert ObradaRezervacija(izvor, []).obradi() == [240, 325]


def test_servis_salje_iznose_svim_izvjestiocima():
    izvor = LazniIzvor([Rezervacija("Ana", 2, 100)])
    a, b = LazniIzvjestilac(), LazniIzvjestilac()
    ObradaRezervacija(izvor, [a, b]).obradi()
    assert a.primljeno == [[200]] and b.primljeno == [[200]]


def test_prazan_izvor_daje_prazan_izvjestaj():
    iz = LazniIzvjestilac()
    assert ObradaRezervacija(LazniIzvor([]), [iz]).obradi() == []
    assert iz.primljeno == [[]]


def test_neispravna_rezervacija_baca_izuzetak():
    with pytest.raises(ValueError):
        Rezervacija("Ana", 0, 80)


def test_csv_i_json_izvor_daju_isti_rezultat(tmp_path: Path):
    csv_p = tmp_path / "r.csv"
    csv_p.write_text("gost,noci,cijena_noci\nAna,2,100\n", encoding="utf-8")
    json_p = tmp_path / "r.json"
    json_p.write_text('[{"gost":"Ana","noci":2,"cijena_noci":100}]', encoding="utf-8")
    assert CsvIzvor(csv_p).ucitaj() == JsonIzvor(json_p).ucitaj()


def test_tekstualni_izvjestaj_upisuje_datoteku(tmp_path: Path):
    p = tmp_path / "izvjestaj.txt"
    TekstualniIzvjestaj(p).izvjesti([240.0, 325.0])
    assert p.read_text(encoding="utf-8") == "240.0\n325.0\n"
