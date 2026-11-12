from mlokvir.eksperiment import IrisEksperiment
from mlokvir.metrike import Tacnost, F1
from mlokvir.posmatraci import KonzolniLogger

for naziv in ["linearni", "stablo", "knn"]:
    params = {"max_iter": 500} if naziv == "linearni" else {}
    e = IrisEksperiment(naziv, [Tacnost(), F1()], **params)
    e.pretplati(KonzolniLogger())
    e.pokreni()
