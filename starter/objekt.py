"""Wo liegt das Objekt? (klassische Bildverarbeitung)

Die KI entscheidet, WAS auf dem Bild zu sehen ist (z. B. die Farbe). Aber Sprachmodelle sind
schlecht darin, Pixelkoordinaten exakt anzugeben. Deshalb misst klassische Bildverarbeitung
(OpenCV), WO das Objekt liegt. Das ist ein typischer Entwurfsgrundsatz: jedes Werkzeug für
das, was es gut kann.

STUNDE 4 (LF 10a): Implementiere finde_schwerpunkt().
"""
import cv2

from trigger import vorbereiten


def finde_schwerpunkt(bild, hintergrund_bild, roi=None, schwelle=30, min_flaeche=500):
    """Gibt den Schwerpunkt (px, py) des größten abweichenden Bereichs in BILDKOORDINATEN zurück.

    Rückgabe: (px, py) als Pixel im GANZEN Bild (nicht nur in der ROI) oder None, wenn nichts
    gefunden wurde.

    TODO:
      1. vorbereiten(bild, roi) und vorbereiten(hintergrund_bild, roi)
      2. cv2.absdiff -> cv2.threshold (schwelle) -> Maske
      3. cv2.findContours auf der Maske, größte Kontur nach cv2.contourArea wählen
      4. kleiner als min_flaeche -> None
      5. cv2.moments(kontur): px = m10/m00, py = m01/m00
      6. ROI-Versatz addieren, damit die Koordinate im ganzen Bild gilt!
    """
    raise NotImplementedError("TODO Stunde 4")
