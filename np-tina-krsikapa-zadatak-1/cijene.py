"""Prosječna cijena noćenja ponderisana brojem noćenja."""
import csv
from pathlib import Path

OBAVEZNE_KOLONE = {"gost", "noci", "cijena_noci"}


def prosjecna_cijena(putanja: Path) -> float:
    """Vraća prosječnu cijenu noćenja ponderisanu brojem noćenja.

    Raises:
        ValueError: nedostaju kolone, neispravni podaci ili nema noćenja.
    """
    ukupno, noci = 0.0, 0
    with putanja.open(newline="", encoding="utf-8") as f:
        citac = csv.DictReader(f)
        if not OBAVEZNE_KOLONE.issubset(citac.fieldnames or []):
            raise ValueError(f"Nedostaju kolone: {sorted(OBAVEZNE_KOLONE)}")
        for red in citac:
            try:
                n = int(red["noci"])
                cijena = float(red["cijena_noci"])
            except (TypeError, ValueError) as e:
                raise ValueError(f"Neispravan red: {red}") from e
            if n < 0 or cijena < 0:
                raise ValueError(f"Negativna vrijednost u redu: {red}")
            ukupno += n * cijena
            noci += n
    if noci == 0:
        raise ValueError("Nema ostvarenih noćenja")
    return ukupno / noci
