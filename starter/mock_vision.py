"""Mock-Bild-KI: liefert Antworten ohne Internet und ohne API-Schlüssel.

- sortieren: bestimmt die Farbe klassisch per Farbwert (HSV). Gleichzeitig eine Vergleichsbasis:
  Wann ist die echte KI besser oder schlechter als diese einfache Regel?
- tasten:    liefert reihum 1, 2, 3 und danach absichtlich eine ungültige Antwort (7),
             damit eure Validierung getestet wird.
"""
import cv2
import numpy as np

_zaehler = {"tasten": 0}
_TASTEN_FOLGE = [1, 2, 3, 7]


def _farbe_hsv(bild):
    hsv = cv2.cvtColor(bild, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    kraeftig = (s > 90) & (v > 60)
    if np.count_nonzero(kraeftig) < 500:
        return None
    farbton = h[kraeftig]
    rot = np.count_nonzero((farbton < 10) | (farbton > 170))
    gruen = np.count_nonzero((farbton > 35) & (farbton < 85))
    blau = np.count_nonzero((farbton > 95) & (farbton < 135))
    zaehlung = {"rot": rot, "gruen": gruen, "blau": blau}
    farbe = max(zaehlung, key=zaehlung.get)
    return farbe if zaehlung[farbe] > 300 else "unbekannt"


def frage_mock_vision(bild, szenario: str) -> dict:
    """Wie vision_client.frage_vision(), aber ohne Cloud."""
    if szenario == "sortieren":
        farbe = _farbe_hsv(bild)
        if farbe is None:
            return {"objekt_vorhanden": False, "farbe": "unbekannt", "konfidenz": 0.9}
        return {"objekt_vorhanden": True, "farbe": farbe, "konfidenz": 0.9}
    if szenario == "tasten":
        zahl = _TASTEN_FOLGE[_zaehler["tasten"] % len(_TASTEN_FOLGE)]
        _zaehler["tasten"] += 1
        return {"zahl": zahl, "konfidenz": 0.95}
    raise ValueError(f"Unbekanntes Szenario: {szenario}")
