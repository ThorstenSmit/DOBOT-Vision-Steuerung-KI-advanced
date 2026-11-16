"""Tests für die Kalibrierung. Ausführen:  python -m pytest -v"""
import pytest

from kalibrierung import berechne_matrix, pixel_zu_mm

PIXEL = [(0, 0), (640, 0), (640, 480), (0, 480)]


def test_skalierung_und_verschiebung():
    # 640 px entsprechen 320 mm, 480 px entsprechen 240 mm, Ursprung liegt bei x=150, y=-120
    roboter = [(150, -120), (470, -120), (470, 120), (150, 120)]
    m = berechne_matrix(PIXEL, roboter)
    assert pixel_zu_mm(m, 0, 0) == pytest.approx((150, -120), abs=0.01)
    assert pixel_zu_mm(m, 320, 240) == pytest.approx((310, 0), abs=0.01)   # Bildmitte
    assert pixel_zu_mm(m, 640, 480) == pytest.approx((470, 120), abs=0.01)

# TODO: weitere Tests
#   - falsche Punktanzahl (3 statt 4)  -> ValueError
#   - speichere() und lade() liefern dieselbe Matrix
#   - mittlerer_fehler_mm() ist bei den Kalibrierpunkten selbst (fast) 0
