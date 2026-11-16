"""Jobs: aus einer Entscheidung eine sichere Folge von Roboterbefehlen machen.

Ein Job ist eine LISTE von Befehlen im Format des Sprachprojekts (fahre_zu, saugnapf_an, ...),
plus {"aktion": "pause", "sekunden": 1}. JEDER Bewegungsbefehl läuft durch validiere()
aus dem Sprachprojekt (validierung.py) und wird erst dann mit fuehre_aus() (ki_steuerung.py)
ausgeführt. So gelten dieselben Sicherheitsgrenzen wie bei der Sprachsteuerung.

STUNDE 5 (LF 11a): Implementiere plane_fahrt() und job_sortieren().
"""
import math
import time

import konfig
from grenzen import GRENZEN, HOME, MAX_SCHRITT
from ki_steuerung import fuehre_aus
from validierung import UngueltigerBefehl, validiere


class JobFehler(Exception):
    """Der Job kann nicht geplant oder nicht sicher ausgeführt werden."""


def passe_grenzen_an(z_min: float) -> None:
    """Senkt die untere z-Grenze, damit der Saugnapf den Tisch erreichen darf.

    Die Standardgrenze aus grenzen.py (z >= 0) schützt den Tisch. Für Aufnehmen und Ablegen
    muss sie bewusst gesenkt werden. Nur nach dem MESSEN von konfig.Z_TISCH und mit etwas
    Reserve (z. B. z_min = Z_TISCH - 2). Entscheidung dokumentieren!
    """
    unten, oben = GRENZEN["z"]
    GRENZEN["z"] = (min(unten, z_min), oben)
    print(f"ACHTUNG: z-Grenze gesenkt auf {GRENZEN['z']}")


def plane_fahrt(start, ziel, max_schritt=MAX_SCHRITT * 0.9) -> list:
    """Zerlegt eine lange Bewegung in Teilstücke von höchstens max_schritt mm.

    validiere() lehnt Bewegungen über MAX_SCHRITT ab. Deshalb wird die Strecke von start nach ziel
    in gleich lange Zwischenschritte geteilt. start/ziel: (x, y, z, r).
    Rückgabe: Liste von {"aktion": "fahre_zu", "x":..., "y":..., "z":..., "r":...}; der letzte
    Eintrag ist genau das Ziel. Sind start und ziel (fast) gleich: leere Liste.

    TODO: Abstand mit math.dist (x, y, z), Anzahl Schritte = ceil(abstand / max_schritt),
          dann linear interpolieren.
    """
    raise NotImplementedError("TODO Stunde 5")


def job_druecke_taste(nr: int, start=HOME) -> list:
    """Beispiel-Job (fertig): über der Taste hinfahren, drücken, wieder hoch."""
    if nr not in konfig.TASTEN:
        raise JobFehler(f"Unbekannte Taste: {nr}")
    x, y, z = konfig.TASTEN[nr]
    ueber = (x, y, konfig.Z_SICHER, 0.0)
    unten = (x, y, z - konfig.TASTEN_HUB_MM, 0.0)
    befehle, pos = [], tuple(start)
    for ziel in (ueber, unten, ueber):
        befehle += plane_fahrt(pos, ziel)
        pos = ziel
    befehle += plane_fahrt(pos, HOME)
    return befehle + [{"aktion": "home"}]


def job_sortieren(farbe: str, objekt_xy, start=HOME) -> list:
    """Stein aufnehmen und im Fach der Farbe ablegen.

    objekt_xy: (x, y) in mm, aus Bildposition + Kalibrierung.

    TODO: Ablauf (jeweils mit plane_fahrt zwischen den Punkten):
      1. über den Stein fahren (z = konfig.Z_SICHER)
      2. absenken auf Aufnahmehöhe (konfig.Z_TISCH + konfig.STEIN_HOEHE)
      3. {"aktion": "saugnapf_an"}, {"aktion": "pause", "sekunden": konfig.SAUG_WARTEZEIT_S}
      4. wieder auf Z_SICHER heben
      5. über das Fach konfig.FAECHER[farbe] fahren, absenken, {"aktion": "saugnapf_aus"},
         kurz pausieren, wieder heben
      6. zurück nach HOME
    Bricht mit JobFehler ab, wenn konfig.Z_TISCH None ist (nicht gemessen!) oder die Farbe unbekannt.
    """
    raise NotImplementedError("TODO Stunde 5")


def fuehre_job(device, befehle: list, start=HOME, vorschau=False) -> None:
    """Führt einen Job aus. JEDER Befehl wird vorher validiert.

    device=None: nur simulieren (kein Roboter angeschlossen).
    vorschau=True: Befehle nur ausgeben, nichts ausführen (aber trotzdem validieren).
    Bei UngueltigerBefehl wird SOFORT abgebrochen. Der Roboter bleibt dann in seiner letzten
    sicheren Position stehen.
    """
    pos = tuple(start)
    for nr, befehl in enumerate(befehle, start=1):
        if befehl.get("aktion") == "pause":
            print(f"  {nr:2d}/{len(befehle)}: Pause {befehl['sekunden']} s")
            if not vorschau:
                time.sleep(float(befehl["sekunden"]))
            continue
        if device is not None and not vorschau:
            pos = tuple(device.pose()[:4])
        try:
            sauber = validiere(befehl, pos)
        except UngueltigerBefehl as e:
            raise JobFehler(f"Schritt {nr} abgelehnt: {e}") from e
        print(f"  {nr:2d}/{len(befehle)}: {sauber}")
        if not vorschau:
            fuehre_aus(device, sauber)
        # Position für die nächste Prüfung fortschreiben (auch bei Simulation)
        if sauber["aktion"] == "fahre_zu":
            pos = (sauber["x"], sauber["y"], sauber["z"], sauber["r"])
        elif sauber["aktion"] == "home":
            pos = tuple(HOME)
