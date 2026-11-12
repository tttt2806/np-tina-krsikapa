"""Template Method: fiksni tok eksperimenta, koraci se mogu nadjačati."""
from abc import ABC, abstractmethod
from sklearn.model_selection import train_test_split

from .dekoratori import izmjeri_vrijeme
from .factory import ModelFactory
from .posmatraci import Subjekt


class Eksperiment(Subjekt, ABC):
    def __init__(self, model_naziv, metrike, test_udio=0.3, seed=42, **model_param):
        super().__init__()
        self.model_naziv = model_naziv
        self.metrike = metrike
        self.test_udio = test_udio
        self.seed = seed
        self.model_param = model_param

    # --- template method ---
    def pokreni(self):
        self.obavijesti("start", model=self.model_naziv)
        X, y = self.ucitaj_podatke()
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y, test_size=self.test_udio, random_state=self.seed, stratify=y
        )
        model = ModelFactory.napravi(self.model_naziv, **self.model_param)
        self.treniraj(model, X_tr, y_tr)
        self.obavijesti("trening_gotov", trajanje=self.treniraj.zadnje_trajanje)
        rezultati = self.evaluiraj(model, X_te, y_te)
        self.obavijesti("kraj", rezultati=rezultati)
        return rezultati

    @abstractmethod
    def ucitaj_podatke(self):
        ...

    @izmjeri_vrijeme
    def treniraj(self, model, X, y):
        model.fit(X, y)

    def evaluiraj(self, model, X, y):
        pred = model.predict(X)
        return {m.naziv: float(m.izracunaj(y, pred)) for m in self.metrike}


class IrisEksperiment(Eksperiment):
    def ucitaj_podatke(self):
        from sklearn.datasets import load_iris
        return load_iris(return_X_y=True)
