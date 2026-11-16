"""Hauptprogramm: Kamera überwachen -> Trigger -> KI-Entscheidung -> prüfen -> Job am Dobot.

Start (Beispiele):
    python ueberwachung.py --szenario sortieren --mock --ohne-roboter --zeige
    python ueberwachung.py --szenario tasten --quelle testbild.jpg --mock --ohne-roboter
    python ueberwachung.py --szenario sortieren                 # echte KI, echter Dobot

Beenden: Taste q im Bildfenster oder Strg+C. Standardmäßig fragt das Programm vor JEDEM
Job nach einer Bestätigung (j/N). Nur mit --auto läuft es ohne Rückfrage.

STUNDE 2 (LF 10a): Bedienoberfläche verbessern (Statusanzeige im Bild, verständliche Meldungen).
STUNDE 6 (LF 10a): Integration, Bestätigung und Notaus-Bedienung.
"""
import argparse
import os
import sys
import time

import cv2

import kalibrierung
import konfig
from entscheidung import UngueltigeEntscheidung, pruefe_entscheidung
from jobs import JobFehler, fuehre_job, job_druecke_taste, job_sortieren, passe_grenzen_an
from kamera import Kamera
from ki_client import KIFehler
from mock_vision import frage_mock_vision
from objekt import finde_schwerpunkt
from prompts import PROMPTS
from trigger import Trigger
from vision_client import frage_vision


def baue_job(szenario, entscheidung, bild, hintergrund, matrix):
    if szenario == "tasten":
        return job_druecke_taste(entscheidung["zahl"])
    schwerpunkt = finde_schwerpunkt(bild, hintergrund, konfig.ROI, konfig.TRIGGER_SCHWELLE)
    if schwerpunkt is None:
        raise JobFehler("Objektposition im Bild nicht gefunden")
    x, y = kalibrierung.pixel_zu_mm(matrix, *schwerpunkt)
    print(f"Objekt bei Pixel {schwerpunkt[0]:.0f},{schwerpunkt[1]:.0f}  ->  x={x:.0f} y={y:.0f} mm")
    return job_sortieren(entscheidung["farbe"], (x, y))


def zeichne_status(bild, text):
    """STUNDE 2: Überwachungsbereich und Status ins Livebild einblenden."""
    x, y, b, h = konfig.ROI
    cv2.rectangle(bild, (x, y), (x + b, y + h), (0, 255, 0), 2)
    cv2.putText(bild, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--szenario", choices=["sortieren", "tasten"], default="sortieren")
    p.add_argument("--quelle", default=str(konfig.KAMERA), help="Kameranummer oder Bild/Video")
    p.add_argument("--mock", action="store_true", help="Mock-Bild-KI statt Cloud")
    p.add_argument("--ohne-roboter", action="store_true", help="Jobs nur simulieren")
    p.add_argument("--auto", action="store_true", help="ohne Rückfrage ausführen (Vorsicht!)")
    p.add_argument("--zeige", action="store_true", help="Livebild in einem Fenster zeigen")
    args = p.parse_args()

    matrix = None
    if args.szenario == "sortieren":
        if konfig.Z_TISCH is None:
            sys.exit("konfig.Z_TISCH ist nicht gemessen. Erst messen (siehe PROJEKT.md, Stunde 5).")
        passe_grenzen_an(konfig.Z_TISCH - 2)
        if not os.path.exists("kalibrierung.json"):
            sys.exit("kalibrierung.json fehlt. Erst 'python kalibrieren.py' ausführen (Stunde 4).")
        matrix = kalibrierung.lade()

    device = None
    if not args.ohne_roboter:
        from dobot_helper import verbinde
        device = verbinde()

    kamera = Kamera(args.quelle)
    trigger = Trigger(konfig.ROI, konfig.TRIGGER_SCHWELLE, konfig.TRIGGER_MIN_FLAECHE,
                      konfig.TRIGGER_STABIL_FRAMES)
    os.makedirs("aufnahmen", exist_ok=True)
    try:
        print("Tisch bitte leer lassen, Hintergrund wird aufgenommen ...")
        time.sleep(2)
        hintergrund = kamera.bild()
        trigger.setze_hintergrund(hintergrund)
        print(f"Überwachung läuft (Szenario: {args.szenario}). Beenden mit q oder Strg+C.")
        pause_bis = 0.0
        while True:
            bild = kamera.bild()
            if bild is None:
                print("Kein Kamerabild mehr. Ende.")
                break
            if args.zeige:
                anzeige = bild.copy()
                zeichne_status(anzeige, "Pause" if time.time() < pause_bis else "Ueberwache")
                cv2.imshow("Dobot Vision", anzeige)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            if time.time() < pause_bis or not trigger.pruefe(bild):
                continue

            print("\n*** Trigger ausgelöst ***")
            cv2.imwrite(f"aufnahmen/{time.strftime('%Y%m%d-%H%M%S')}.jpg", bild)
            try:
                antwort = (frage_mock_vision(bild, args.szenario) if args.mock
                           else frage_vision(bild, PROMPTS[args.szenario]))
                print("KI-Antwort:", antwort)
                entscheidung = pruefe_entscheidung(args.szenario, antwort)
                print("Entscheidung:", entscheidung)
                job = baue_job(args.szenario, entscheidung, bild, hintergrund, matrix)
                print("Geplanter Ablauf:")
                fuehre_job(None, job, vorschau=True)
                if not args.auto and input("Ausführen? [j/N] ").strip().lower() != "j":
                    print("Abgebrochen.")
                else:
                    fuehre_job(device, job)
                    print("Job fertig.")
            except (KIFehler, UngueltigeEntscheidung, JobFehler) as e:
                print("KEIN JOB:", e)
                if device is not None:
                    device.stopp()
            pause_bis = time.time() + konfig.COOLDOWN_S
    except KeyboardInterrupt:
        print("\nAbbruch durch Nutzer.")
    finally:
        if device is not None:
            device.stopp()
            device.close()
        kamera.schliessen()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
