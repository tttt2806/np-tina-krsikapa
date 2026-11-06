"""Konkretni izvještavači."""
from pathlib import Path
from typing import Sequence


class TekstualniIzvjestaj:
    """Upisuje iznose u tekstualnu datoteku, jedan iznos po redu."""

    def __init__(self, putanja: Path) -> None:
        self.putanja = putanja

    def izvjesti(self, iznosi: Sequence[float]) -> None:
        with self.putanja.open("w", encoding="utf-8") as f:
            for iznos in iznosi:
                f.write(f"{iznos}\n")


class MailObavjestenje:
    """Simulira slanje maila (ispis na konzolu)."""

    def izvjesti(self, iznosi: Sequence[float]) -> None:
        print("Poslato:", sum(iznosi))
