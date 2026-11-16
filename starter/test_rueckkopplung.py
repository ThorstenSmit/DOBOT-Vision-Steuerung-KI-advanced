"""Tests für die Rückkopplung (Zusatzaufgabe). Ausführen:  python -m pytest -v test_rueckkopplung.py

Synthetische Bilder, ganz ohne Kamera und Roboter. Die Kalibriermatrix ist hier die Einheitsmatrix,
also gilt: 1 Pixel = 1 mm. Zwei Tests sind vorgegeben, ergänzt die übrigen.
"""
import cv2
import numpy as np

from rueckkopplung import fuehre_mit_rueckkopplung, pruefe_ergebnis

EINS = np.eye(3)
FACH = (200.0, 100.0)          # Fach bei Pixel (200, 100)


def leer():
    return np.full((240, 320, 3), 120, np.uint8)


def stein_bei(x, y):
    bild = leer()
    cv2.rectangle(bild, (x - 15, y - 15), (x + 15, y + 15), (20, 20, 20), -1)
    return bild


def test_stein_im_fach_ist_erfolg():
    assert pruefe_ergebnis(stein_bei(200, 100), leer(), FACH, EINS)


def test_wiederholungen_sind_begrenzt():
    aufrufe = []
    ergebnis = fuehre_mit_rueckkopplung(lambda: aufrufe.append(1), lambda: False,
                                        max_wiederholungen=2)
    assert ergebnis is False
    assert len(aufrufe) == 3      # 1 Versuch + 2 Wiederholungen

# TODO: weitere Tests
#   - Fach leer                                   -> False
#   - Stein liegt noch am alten Ort (alt_px)      -> False
#   - Stein liegt im falschen Fach                -> False
#   - Erfolg im 2. Versuch                        -> True, versuch_fn genau 2x aufgerufen
#   - Fehler in versuch_fn (z. B. Exception)      -> wird NICHT abgefangen, pruefe_fn nie aufgerufen
