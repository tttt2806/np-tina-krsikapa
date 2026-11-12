"""Factory pattern: kreiranje modela po imenu."""
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier


class ModelFactory:
    _registar = {
        "linearni": LogisticRegression,
        "stablo": DecisionTreeClassifier,
        "knn": KNeighborsClassifier,
    }

    @classmethod
    def napravi(cls, naziv, **parametri):
        try:
            return cls._registar[naziv](**parametri)
        except KeyError:
            raise ValueError(
                f"Nepoznat model '{naziv}'. Dostupni: {cls.dostupni()}"
            ) from None

    @classmethod
    def dostupni(cls):
        return sorted(cls._registar)
