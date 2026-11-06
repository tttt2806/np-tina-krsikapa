# Mini projekat 1: refaktoring obrade rezervacija

Autor: Tina Kršikapa  
Napredno programiranje (FIST4NP), Nedjelja 2 – OOP i SOLID.

Monolitna klasa `UpravljanjeRezervacijama` (učitavanje, obračun, čuvanje izvještaja
i slanje maila u jednoj klasi) refaktorisana je u male klase sa jednom odgovornošću.

## Pokretanje

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python main.py podaci/rezervacije.csv     # ili podaci/rezervacije.json
```

## Struktura

| Datoteka | Odgovornost |
| --- | --- |
| `rezervacije/modeli.py` | `Rezervacija` (frozen dataclass) sa validacijom i svojstvom `iznos` |
| `rezervacije/protokoli.py` | `IzvorPodataka` i `Izvjestilac` (`typing.Protocol`) |
| `rezervacije/izvori.py` | `CsvIzvor`, `JsonIzvor` – učitavanje podataka |
| `rezervacije/izvjestaji.py` | `TekstualniIzvjestaj`, `MailObavjestenje` – izvještavanje |
| `rezervacije/servis.py` | `ObradaRezervacija` – povezuje izvor i izvještavače |
| `main.py` | sastavljanje zavisnosti (composition root) |
| `tests/test_servis.py` | pytest testovi sa zamjenskim izvorom podataka |

## Primijenjeni principi

- **S (Single Responsibility):** učitavanje, obračun iznosa, čuvanje izvještaja i
  obavještavanje su četiri razloga za promjenu, pa su u četiri odvojena mjesta.
- **D (Dependency Inversion):** `ObradaRezervacija` prima `IzvorPodataka` i
  `Izvjestilac` kroz konstruktor i zavisi samo od `Protocol`-a, ne od konkretnih klasa.
- **O (Open/Closed):** `JsonIzvor` je dodat bez izmjene servisa.
- **I (Interface Segregation):** dva mala ugovora umjesto jednog velikog.

## Testovi

Šest pytest testova. Servis se testira sa `LazniIzvor` i `LazniIzvjestilac`
(bez datoteka), plus testovi izvora, izvještaja i validacije.

## Rad sa AI asistentom

Za izradu je korišćen AI asistent Claude (Anthropic). Generisani kod je pokrenut, provjeren testovima i ručno pregledan.

### Upit (struktura: kontekst, zadatak, ograničenja, format)

```
Kontekst: Python 3.12; klasa UpravljanjeRezervacijama (kod ispod) radi učitavanje CSV-a,
obračun iznosa, upis izvještaja i slanje maila.
Zadatak: refaktorisati u klase primjenom principa S i D; uvesti Protocol za izvor
podataka i za izvještavanje.
Ograničenja: samo standardna biblioteka, type hints, ne uvoditi apstrakcije koje
problem ne zahtijeva.
Format odgovora: kod po datotekama, tri pytest testa sa zamjenskim izvorom
podataka i kratko obrazloženje.

[kod monolitnog skripta]
```

### Uočeni nedostaci originalnog/generisanog koda i ispravke

1. `open(...)` bez `with` u `ucitaj` i `sacuvaj_izvjestaj` – datoteka se ne zatvara
   garantovano. **Ispravka:** `with path.open(...)` u `CsvIzvor` i `TekstualniIzvjestaj`.
2. Bez kodiranja (`encoding`) – ponašanje zavisi od sistema. **Ispravka:** `encoding="utf-8"`.
3. Ručno `split(",")` i pristup po indeksu (`r[1]`, `r[2]`) – krhko i nečitljivo.
   **Ispravka:** `csv.DictReader` sa imenovanim kolonama i `Rezervacija` dataclass.
4. Bez validacije ulaza (negativne noći, loš format). **Ispravka:** `__post_init__` u
   `Rezervacija` baca `ValueError`; test `test_neispravna_rezervacija_baca_izuzetak`.
5. Naziv izvještaja zapisan u kodu (`"izvjestaj.txt"`) i izvještaj je `str(lista)`.
   **Ispravka:** putanja se prosljeđuje kroz konstruktor, jedan iznos po redu.
6. Klasa je čvrsto vezana za datoteku i `print` – nemoguće testirati bez diska.
   **Ispravka:** `Protocol` + injekcija zavisnosti.
7. AI je sklon predlaganju previše apstrakcija (npr. fabrike, tarife, bazna klasa).
   **Odluka:** zadržana samo dva `Protocol`-a koja zadatak traži.
