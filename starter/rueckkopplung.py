"""Rückkopplung: Das Ergebnis eines Jobs prüfen und bei Misserfolg gezielt wiederholen.

ZUSATZAUFGABE (siehe PROJEKT.md): Aus der offenen Kette wird ein Regelkreis.

    Job ausführen -> Kamera prüft das Ergebnis -> Misserfolg? -> Wiederholen (begrenzt!)
"""
import cv2
import numpy as np

from trigger import vorbereiten


def fach_pixel(matrix, fach_xy):
    """Rechnet eine Roboterposition (x, y in mm) in einen Bildpunkt (px, py) um.

    kalibrierung.pixel_zu_mm() rechnet Pixel -> mm. Hier brauchst du die UMKEHRUNG.

    TODO: Inverse Matrix mit np.linalg.inv(matrix), dann cv2.perspectiveTransform wie in
          kalibrierung.pixel_zu_mm(). Rückgabe: (px, py) als float.
    """
    raise NotImplementedError("Zusatzaufgabe")


def pruefe_ergebnis(bild, hintergrund, fach_xy, matrix, alt_px=None,
                    radius=40, schwelle=30, min_flaeche=300) -> bool:
    """True, wenn der Stein im Fach liegt (und nicht mehr am alten Ort).

    bild:        aktuelles Kamerabild (der Arm muss aus dem Bild sein, also in Home-Position)
    hintergrund: Bild des leeren Tisches (wie beim Trigger)
    fach_xy:     (x, y) des Fachs in mm (konfig.FAECHER[farbe])
    matrix:      Kalibriermatrix Pixel -> mm
    alt_px:      (px, py), wo der Stein vorher lag; dort darf nichts mehr liegen (optional)
    radius:      halbe Kantenlänge des geprüften Quadrats um das Fach in Pixeln

    TODO:
      1. px, py = fach_pixel(matrix, fach_xy)
      2. vorbereiten() für bild und hintergrund (Graubild), cv2.absdiff, cv2.threshold(schwelle)
      3. Anzahl abweichender Pixel im Quadrat um (px, py) zählen (Ränder des Bildes beachten!)
      4. Fach belegt = Anzahl >= min_flaeche
      5. Wenn alt_px angegeben: am alten Ort muss die Anzahl < min_flaeche sein
    """
    raise NotImplementedError("Zusatzaufgabe")


def fuehre_mit_rueckkopplung(versuch_fn, pruefe_fn, max_wiederholungen=2) -> bool:
    """Führt versuch_fn() aus, prüft mit pruefe_fn() und wiederholt bei Misserfolg.

    versuch_fn: führt den Job einmal aus (plant ihn, validiert und fährt)
    pruefe_fn:  gibt True zurück, wenn das Ergebnis stimmt
    Insgesamt höchstens 1 + max_wiederholungen Versuche. Rückgabe: True bei Erfolg, sonst False.

    WICHTIG: Fehler aus versuch_fn (z. B. JobFehler, weil die Validierung einen Schritt ablehnt)
    werden NICHT abgefangen. Ein Sicherheitsfehler wird nie "einfach nochmal versucht".

    TODO: Schleife mit Zähler, Meldungen ausgeben ("Versuch 2 von 3 ...").
    """
    raise NotImplementedError("Zusatzaufgabe")
