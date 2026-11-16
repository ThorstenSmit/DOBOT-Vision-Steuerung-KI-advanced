"""Kalibrierwerkzeug: verknüpft Kamerabild und Roboterkoordinaten.

Vorbereitung:
  - Lege 5 gut sichtbare Markierungen (z. B. Klebepunkte) auf den Tisch, verteilt über das
    Arbeitsfeld. Vier davon dienen der Berechnung, der fünfte als unabhängiger Kontrollpunkt.
  - Fahre mit der Weboberfläche des Grundprojekts (python app.py) die Spitze des Dobot
    nacheinander über jede Markierung und lies x und y im Feld "Position" ab. Notiere sie.
  - Beende danach die Weboberfläche (Strg+C), denn der Dobot hat nur einen Zugriff.

Ablauf des Programms:
    python kalibrieren.py [--quelle 0]
  1. Livebild: Taste LEERTASTE nimmt ein Foto auf (Markierungen sichtbar, Arm aus dem Bild!).
  2. Klicke nacheinander die 5 Markierungen im Foto an (Reihenfolge wie deine Notizen).
  3. Gib zu jedem Klick die notierten Roboterkoordinaten ein (x y in mm).
  4. Die Matrix wird aus den ersten 4 Punkten berechnet, der Fehler am 5. Punkt angezeigt
     und in kalibrierung.json gespeichert.
"""
import argparse

import cv2

import kalibrierung
import konfig
from kamera import Kamera


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--quelle", default=str(konfig.KAMERA))
    args = p.parse_args()

    kamera = Kamera(args.quelle)
    foto = None
    print("Livebild. LEERTASTE = Foto aufnehmen, q = Abbrechen.")
    while foto is None:
        bild = kamera.bild()
        if bild is None:
            raise SystemExit("Kein Kamerabild.")
        cv2.imshow("Kalibrierung - LEERTASTE", bild)
        taste = cv2.waitKey(30) & 0xFF
        if taste == ord("q"):
            raise SystemExit("Abgebrochen.")
        if taste == ord(" "):
            foto = bild
    kamera.schliessen()
    cv2.destroyAllWindows()

    klicks = []

    def maus(ereignis, x, y, *_):
        if ereignis == cv2.EVENT_LBUTTONDOWN and len(klicks) < 5:
            klicks.append((x, y))
            cv2.circle(anzeige, (x, y), 6, (0, 0, 255), 2)
            cv2.putText(anzeige, str(len(klicks)), (x + 8, y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    anzeige = foto.copy()
    cv2.namedWindow("Markierungen anklicken")
    cv2.setMouseCallback("Markierungen anklicken", maus)
    print("Klicke die 5 Markierungen an (in der Reihenfolge deiner Notizen).")
    while len(klicks) < 5:
        cv2.imshow("Markierungen anklicken", anzeige)
        if cv2.waitKey(30) & 0xFF == ord("q"):
            raise SystemExit("Abgebrochen.")
    cv2.destroyAllWindows()

    roboter = []
    for nr in range(1, 6):
        while True:
            eingabe = input(f"Punkt {nr}: Roboterposition 'x y' in mm: ").replace(",", ".").split()
            try:
                x, y = float(eingabe[0]), float(eingabe[1])
                break
            except (ValueError, IndexError):
                print("Bitte zwei Zahlen eingeben, z. B.  200 -45.5")
        roboter.append((x, y))

    matrix = kalibrierung.berechne_matrix(klicks[:4], roboter[:4])
    fehler = kalibrierung.mittlerer_fehler_mm(matrix, klicks[4:], roboter[4:])
    print(f"Fehler am Kontrollpunkt: {fehler:.1f} mm")
    if fehler > 5:
        print("WARNUNG: mehr als 5 mm Abweichung. Der Saugnapf würde den Stein verfehlen. "
              "Punkte genauer anklicken/messen und wiederholen.")
    kalibrierung.speichere(matrix)
    print("Gespeichert in kalibrierung.json")


if __name__ == "__main__":
    main()
