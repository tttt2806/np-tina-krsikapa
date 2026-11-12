"""Strategy pattern: zamjenjive metrike."""
from abc import ABC, abstractmethod
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


class Metrika(ABC):
    naziv = "metrika"

    @abstractmethod
    def izracunaj(self, y_true, y_pred) -> float:
        ...


class Tacnost(Metrika):
    naziv = "tacnost"

    def izracunaj(self, y_true, y_pred):
        return accuracy_score(y_true, y_pred)


class F1(Metrika):
    naziv = "f1"

    def izracunaj(self, y_true, y_pred):
        return f1_score(y_true, y_pred, average="macro")


class Preciznost(Metrika):
    naziv = "preciznost"

    def izracunaj(self, y_true, y_pred):
        return precision_score(y_true, y_pred, average="macro", zero_division=0)


class Odziv(Metrika):
    naziv = "odziv"

    def izracunaj(self, y_true, y_pred):
        return recall_score(y_true, y_pred, average="macro")
