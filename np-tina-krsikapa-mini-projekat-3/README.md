# Mini projekat 3: testiran i obezbijeđen API

FastAPI servis sa dva endpointa, pytest testovima i GitHub Actions CI-em
(ruff, mypy, pytest, bandit, pip-audit).

## Endpointi

| Metoda | Putanja            | Opis                                   |
|--------|--------------------|----------------------------------------|
| POST   | `/tasks`           | Kreira zadatak (201), validira unos    |
| GET    | `/tasks/{task_id}` | Vraća zadatak (200) ili 404 / 422      |

Polja zadatka: `title` (1–100 znakova, ne smije biti prazan), `description`
(do 500 znakova), `priority` (1–5).

## Pokretanje

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

## Provjere (iste kao u CI-u)

```bash
ruff check . && ruff format --check .
mypy app tests
pytest -v
bandit -r app
pip-audit -r requirements.txt
```

## Testovi

Testovi pokrivaju uspješan unos, nepostojeći resurs (404), neispravan ID (0, negativan,
tekst), neispravne unose (prazan/razmaci/pogrešan tip naslova, prekratak/predug opis) i
granične slučajeve (naslov 1/100/101 znakova, prioritet 0/1/5/6) te popunjenost skladišta.

## Bezbjednosni pregled

**Bandit** (`bandit -r app`) i **pip-audit** (`pip-audit -r requirements.txt`) se
pokreću u CI-u i build pada ako prijave nalaz. Nalazi i odluke:

- Bandit: nema nalaza u `app/`. Test fajlovi koriste `assert` (B101), zato se bandit
  pokreće samo nad `app/`, a ruff pravilo S101 je isključeno samo za `tests/`.
- pip-audit: nema poznatih ranjivosti u trenutnim zavisnostima. Ako se pojavi nalaz,
  zavisnost se ažurira, a ako ispravka ne postoji, nalaz se obrazlaže ovdje.

## Rizici i mjere smanjenja

1. **Iscrpljivanje resursa (DoS).** Skladište je u memoriji, pa bi neograničen broj ili
   veličina zahtjeva mogli srušiti servis. *Mjere:* ograničenja dužine polja
   (title 100, description 500), gornja granica broja zadataka (`MAX_TASKS`, odgovor 507),
   a u produkciji rate limiting na reverse proxy-ju.
2. **Neispravan ili zlonamjeran unos.** Prazni, predugi ili pogrešno tipizirani podaci
   mogu izazvati greške ili dovesti do injekcija u sistemima koji kasnije koriste podatke.
   *Mjere:* stroga Pydantic validacija (tipovi, granice, trim naslova), `Path(ge=1)` za ID,
   automatski 422 odgovori, nema SQL-a ni izvršavanja unosa.
3. **Ranjive zavisnosti (supply chain).** Biblioteke mogu imati poznate CVE ranjivosti.
   *Mjere:* `pip-audit` u svakom CI pokretanju, ažuriranje zavisnosti (npr. Dependabot),
   korišćenje samo nužnih paketa.
4. **Nedostatak autentifikacije.** Svako može kreirati i čitati zadatke. *Mjere:* za
   produkciju dodati autentifikaciju (npr. OAuth2/JWT preko FastAPI security alata) i
   HTTPS; servis ne treba izlagati javno bez toga.
5. **Curenje informacija kroz greške.** Detaljne poruke grešaka mogu otkriti internu
   strukturu. *Mjere:* kontrolisane poruke grešaka (`HTTPException` sa kratkim `detail`),
   bez debug moda u produkciji.
