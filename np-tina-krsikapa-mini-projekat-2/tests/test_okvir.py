import pytest
from sklearn.neighbors import KNeighborsClassifier
from mlokvir.factory import ModelFactory
from mlokvir.metrike import Tacnost, F1
from mlokvir.posmatraci import Istorija
from mlokvir.dekoratori import izmjeri_vrijeme
from mlokvir.eksperiment import IrisEksperiment


def test_factory_pravi_knn_sa_parametrom():
    m = ModelFactory.napravi("knn", n_neighbors=3)
    assert isinstance(m, KNeighborsClassifier) and m.n_neighbors == 3


def test_factory_nepoznat_model():
    with pytest.raises(ValueError):
        ModelFactory.napravi("nepostoji")


def test_metrike_strategy():
    y = [0, 1, 1, 0]
    assert Tacnost().izracunaj(y, y) == 1.0
    assert F1().izracunaj(y, [1, 0, 0, 1]) == 0.0


def test_observer_prima_dogadjaje():
    e = IrisEksperiment("stablo", [Tacnost()])
    h = Istorija()
    e.pretplati(h)
    e.pokreni()
    imena = [d[0] for d in h.dogadjaji]
    assert imena == ["start", "trening_gotov", "kraj"]


def test_decorator_mjeri_vrijeme():
    @izmjeri_vrijeme
    def f():
        return 5
    assert f() == 5 and f.zadnje_trajanje >= 0


@pytest.mark.parametrize("naziv", ["linearni", "stablo", "knn"])
def test_iris_tacnost_visoka(naziv):
    params = {"max_iter": 500} if naziv == "linearni" else {}
    r = IrisEksperiment(naziv, [Tacnost()], **params).pokreni()
    assert r["tacnost"] > 0.85
