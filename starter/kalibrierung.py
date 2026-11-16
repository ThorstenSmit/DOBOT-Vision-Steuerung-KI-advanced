"""Kalibrierung: Bildpixel (px, py)  ->  Roboterkoordinaten (x, y in mm).

Die Kamera schaut von oben auf den Tisch. Mit vier bekannten Punktpaaren (Pixel im Bild und die
zugehörige Roboterposition) lässt sich eine Transformationsmatrix berechnen, die jeden Bildpunkt
in Roboterkoordinaten umrechnet (Perspektivtransformation / Homographie).

STUNDE 4 (LF 10a): Implementiere berechne_matrix() und pixel_zu_mm().
"""
import json

import cv2
import numpy as np


def berechne_matrix(pixel_punkte, roboter_punkte):
    """Berechnet die 3x3-Matrix aus genau 4 Punktpaaren.

    pixel_punkte:   [(px, py), ...]  vier Punkte im Kamerabild
    roboter_punkte: [(x, y), ...]    dieselben vier Punkte in mm (gleiche Reihenfolge!)

    TODO: cv2.getPerspectiveTransform(np.float32(...), np.float32(...))
    """
    raise NotImplementedError("TODO Stunde 4")


def pixel_zu_mm(matrix, px, py):
    """Rechnet einen Bildpunkt in Roboterkoordinaten (x, y) um.

    TODO: cv2.perspectiveTransform(np.float32([[[px, py]]]), matrix)  ->  Ergebnis [0][0]
    """
    raise NotImplementedError("TODO Stunde 4")


def mittlerer_fehler_mm(matrix, pixel_punkte, roboter_punkte) -> float:
    """Wie genau passt die Matrix? Mittlerer Abstand (mm) zwischen berechnet und gemessen."""
    abstaende = []
    for (px, py), (rx, ry) in zip(pixel_punkte, roboter_punkte):
        x, y = pixel_zu_mm(matrix, px, py)
        abstaende.append(((x - rx) ** 2 + (y - ry) ** 2) ** 0.5)
    return float(np.mean(abstaende))


def speichere(matrix, pfad="kalibrierung.json"):
    with open(pfad, "w", encoding="utf-8") as f:
        json.dump(np.asarray(matrix).tolist(), f)


def lade(pfad="kalibrierung.json"):
    with open(pfad, encoding="utf-8") as f:
        return np.array(json.load(f), dtype=np.float64)
