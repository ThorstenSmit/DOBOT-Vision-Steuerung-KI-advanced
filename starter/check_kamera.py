"""Kamera testen: Livebild anzeigen. LEERTASTE speichert ein Foto, q beendet.

Aufruf:  python check_kamera.py [--quelle 0]
Stelle die Kamera so ein, dass sie senkrecht von oben auf das Arbeitsfeld schaut und
KEINE Gesichter im Bild sind (Datenschutz: Bilder gehen an einen Cloud-Dienst!).
"""
import argparse
import os
import time

import cv2

import konfig
from kamera import Kamera

p = argparse.ArgumentParser()
p.add_argument("--quelle", default=str(konfig.KAMERA))
args = p.parse_args()

kamera = Kamera(args.quelle)
os.makedirs("aufnahmen", exist_ok=True)
print("LEERTASTE = Foto speichern, q = Ende")
while True:
    bild = kamera.bild()
    if bild is None:
        print("Kein Bild.")
        break
    h, b = bild.shape[:2]
    anzeige = bild.copy()
    x, y, rb, rh = konfig.ROI
    cv2.rectangle(anzeige, (x, y), (x + rb, y + rh), (0, 255, 0), 2)
    cv2.putText(anzeige, f"{b}x{h}  (gruen = ROI)", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 255, 0), 2)
    cv2.imshow("Kamera-Test", anzeige)
    taste = cv2.waitKey(30) & 0xFF
    if taste == ord("q"):
        break
    if taste == ord(" "):
        pfad = f"aufnahmen/test-{time.strftime('%H%M%S')}.jpg"
        cv2.imwrite(pfad, bild)
        print("Gespeichert:", pfad)
kamera.schliessen()
cv2.destroyAllWindows()
