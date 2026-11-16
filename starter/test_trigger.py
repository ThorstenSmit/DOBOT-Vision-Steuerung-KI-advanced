"""Tests für den Trigger. Ausführen:  python -m pytest -v

Zwei Tests sind vorgegeben (mit synthetischen Bildern, ganz ohne Kamera). Ergänze eigene:
 - Eine vorbeiziehende Hand (Objekt ändert sich von Bild zu Bild) darf NICHT auslösen.
 - Nach dem Wegnehmen des Objekts und erneutem Auflegen löst der Trigger wieder aus.
 - ist_frei() ist True auf leerem Tisch und False mit Objekt.
"""
import cv2
import numpy as np

from trigger import Trigger


def leer():
    return np.full((240, 320, 3), 120, np.uint8)


def mit_stein(x=100):
    bild = leer()
    cv2.rectangle(bild, (x, 80), (x + 60, 140), (20, 20, 20), -1)
    return bild


def test_leerer_tisch_loest_nicht_aus():
    t = Trigger(None, schwelle=30, min_flaeche=500, stabil_frames=3)
    t.setze_hintergrund(leer())
    assert not any(t.pruefe(leer()) for _ in range(10))


def test_stein_loest_genau_einmal_aus():
    t = Trigger(None, schwelle=30, min_flaeche=500, stabil_frames=3)
    t.setze_hintergrund(leer())
    ergebnisse = [t.pruefe(mit_stein()) for _ in range(6)]
    assert ergebnisse == [False, False, True, False, False, False]
