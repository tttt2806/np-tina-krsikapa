# Napredno programiranje: priprema okruženja (Nedjelja 1)

Autor: Tina Kršikapa

Funkcija `prosjecna_cijena` računa prosječnu cijenu noćenja ponderisanu brojem
noćenja iz CSV datoteke (kolone: `gost`, `noci`, `cijena_noci`).

## Pokretanje

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
ruff check . && ruff format .
```

## Upotrijebljeni upit

Za izradu je korišćen AI asistent Claude (Anthropic). Generisani kod je pokrenut, provjeren testovima i ručno pregledan.

```
Kontekst: Python 3.12; podaci o rezervacijama u CSV datoteci (kolone: gost, noci, cijena_noci).
Zadatak: napisati funkciju koja vraća prosječnu cijenu noćenja ponderisanu brojem noćenja.
Ograničenja: samo standardna biblioteka, type hints, obrada grešaka (prazna datoteka, neispravni podaci).
Format odgovora: kod, tri pytest testa i kratko obrazloženje rješenja.
```

## Uočeni nedostaci generisanog koda i ispravke

1. Nije provjeravano postojanje kolona: nedostajuća kolona bacala je `KeyError`
   bez jasne poruke. **Ispravka:** provjera zaglavlja i `ValueError`.
2. Neispravan tip (`"dva"` umjesto broja) bacao je izuzetak bez konteksta.
   **Ispravka:** `ValueError` sa prikazom spornog reda.
3. Negativni brojevi noćenja ili cijene nisu odbijani. **Ispravka:** provjera i izuzetak.
4. Testom nisu bili pokriveni prazna datoteka, neispravan tip, nedostajuća kolona i
   kodiranje. **Ispravka:** dodati testovi za svaki od tih slučajeva.
