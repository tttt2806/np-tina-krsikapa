from pathlib import Path

import pytest

from cijene import prosjecna_cijena


def napisi(tmp_path: Path, tekst: str) -> Path:
    p = tmp_path / "r.csv"
    p.write_text(tekst, encoding="utf-8")
    return p


def test_prosjek(tmp_path):
    p = napisi(tmp_path, "gost,noci,cijena_noci\nAna,2,100\nMarko,2,50\n")
    assert prosjecna_cijena(p) == 75.0


def test_ponderisan_brojem_nocenja(tmp_path):
    p = napisi(tmp_path, "gost,noci,cijena_noci\nAna,1,100\nMarko,3,60\n")
    assert prosjecna_cijena(p) == 70.0


def test_prazna_datoteka(tmp_path):
    p = napisi(tmp_path, "gost,noci,cijena_noci\n")
    with pytest.raises(ValueError):
        prosjecna_cijena(p)


def test_neispravan_tip(tmp_path):
    p = napisi(tmp_path, "gost,noci,cijena_noci\nAna,dva,100\n")
    with pytest.raises(ValueError):
        prosjecna_cijena(p)


def test_nedostajuca_kolona(tmp_path):
    p = napisi(tmp_path, "gost,noci\nAna,2\n")
    with pytest.raises(ValueError):
        prosjecna_cijena(p)


def test_kodiranje_utf8(tmp_path):
    p = napisi(tmp_path, "gost,noci,cijena_noci\nŽeljko,2,100\n")
    assert prosjecna_cijena(p) == 100.0
