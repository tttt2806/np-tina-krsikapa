"""Decorator pattern: mjerenje vremena izvršavanja."""
import functools
import time


def izmjeri_vrijeme(fn):
    @functools.wraps(fn)
    def omotac(*args, **kwargs):
        start = time.perf_counter()
        rezultat = fn(*args, **kwargs)
        omotac.zadnje_trajanje = time.perf_counter() - start
        return rezultat

    omotac.zadnje_trajanje = None
    return omotac
