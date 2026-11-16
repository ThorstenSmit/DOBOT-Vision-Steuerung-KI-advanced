"""Trigger: erkennt, wann ein Objekt im Überwachungsbereich liegt UND ruhig liegen bleibt.

STUNDE 1 (LF 11a): Implementiere _belegte_flaeche() und pruefe().

Idee: Vergleiche jedes Bild mit einem Hintergrundbild (leerer Tisch). Je mehr Pixel
abweichen, desto mehr liegt dort. Erst wenn das Objekt mehrere Bilder in Folge liegt
(und sich nicht bewegt), löst der Trigger EINMAL aus. So reagiert er weder auf eine
vorbeiziehende Hand noch löst er 30-mal pro Sekunde aus.
"""
import cv2
import numpy as np


def vorbereiten(bild, roi=None):
    """Zuschneiden auf die ROI, in Graustufen umwandeln, leicht weichzeichnen (Rauschen)."""
    if roi is not None:
        x, y, b, h = roi
        bild = bild[y:y + h, x:x + b]
    grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(grau, (7, 7), 0)


class Trigger:
    def __init__(self, roi=None, schwelle=30, min_flaeche=1500, stabil_frames=10):
        self.roi = roi
        self.schwelle = schwelle
        self.min_flaeche = min_flaeche
        self.stabil_frames = stabil_frames
        self.hintergrund = None
        self._stabil = 0          # wie viele Bilder in Folge ruhig belegt
        self._letztes = None      # vorheriges (vorbereitetes) Bild

    def setze_hintergrund(self, bild):
        """Merkt sich das Bild des leeren Tisches als Vergleich."""
        self.hintergrund = vorbereiten(bild, self.roi)
        self._stabil = 0
        self._letztes = None

    def _belegte_flaeche(self, bild) -> int:
        """Anzahl der Pixel, die sich vom Hintergrund unterscheiden.

        TODO: vorbereiten(bild, self.roi) -> cv2.absdiff mit self.hintergrund ->
              cv2.threshold mit self.schwelle -> cv2.countNonZero
        """
        raise NotImplementedError("TODO Stunde 1")

    def pruefe(self, bild) -> bool:
        """True genau EINMAL, wenn ein Objekt seit stabil_frames Bildern ruhig liegt.

        TODO:
          1. fläche = self._belegte_flaeche(bild)
          2. belegt = fläche >= self.min_flaeche
          3. ruhig = Unterschied zum vorherigen Bild (self._letztes) ist klein
             (z. B. weniger als min_flaeche / 4 Pixel weichen ab)
          4. Zähler self._stabil erhöhen, wenn belegt und ruhig, sonst auf 0
          5. True nur, wenn der Zähler GENAU stabil_frames erreicht
             (dann bleibt es für dasselbe Objekt False, bis der Tisch wieder frei war)
        """
        raise NotImplementedError("TODO Stunde 1")

    def ist_frei(self, bild) -> bool:
        """True, wenn der Tisch (fast) leer ist. Gibt es nach einem Job zurück, ob alles weg ist."""
        return self._belegte_flaeche(bild) < self.min_flaeche / 3
