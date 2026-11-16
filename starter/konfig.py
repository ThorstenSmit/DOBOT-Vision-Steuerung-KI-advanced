"""Zentrale Einstellungen für das Vision-Projekt.

Alle Werte mit "MESSEN" oder "ANPASSEN" müssen an EUREN Aufbau angepasst werden.
Positionen in Millimetern (Roboterkoordinaten), Bildpositionen in Pixeln.
"""

# ---------------- Kamera ----------------
KAMERA = 0                    # 0 = erste Webcam, oder Pfad zu einem Bild/Video zum Testen
ROI = (100, 80, 440, 320)     # ANPASSEN: Überwachungsbereich im Bild (x, y, Breite, Höhe)

# ---------------- Trigger ----------------
TRIGGER_SCHWELLE = 30         # Helligkeitsunterschied (0-255), ab dem ein Pixel als "anders" zählt
TRIGGER_MIN_FLAECHE = 1500    # so viele Pixel müssen "anders" sein, damit ein Objekt gezählt wird
TRIGGER_STABIL_FRAMES = 10    # so viele Bilder in Folge muss das Objekt ruhig liegen
COOLDOWN_S = 5.0              # Pause nach einem Job, bevor der nächste Trigger zählt

# ---------------- Höhen (z, mm) ----------------
Z_TISCH = None                # MESSEN: z-Wert, bei dem der Saugnapf die Tischplatte berührt!
Z_SICHER = 60.0               # Fahrhöhe über allem (Steine, Taster)
STEIN_HOEHE = 10.0            # ANPASSEN: Höhe eines Steins in mm
SAUG_WARTEZEIT_S = 1.0        # so lange Pumpe laufen lassen, bevor angehoben wird

# ---------------- Szenario A: Sortieren ----------------
# Ablagepositionen (x, y) in mm. ANPASSEN: mit der Weboberfläche des Grundprojekts anfahren
# und die Position ablesen.
FAECHER = {
    "rot": (180.0, -100.0),
    "gruen": (230.0, -100.0),
    "blau": (280.0, -100.0),
}

# ---------------- Szenario B: Taster drücken ----------------
# Position (x, y) und z der Tasteroberfläche. ANPASSEN: einmal anfahren und ablesen.
TASTEN = {
    1: (200.0, 60.0, 20.0),
    2: (200.0, 90.0, 20.0),
    3: (200.0, 120.0, 20.0),
}
TASTEN_HUB_MM = 6.0           # so viel fährt der Arm beim Drücken unter die Tasteroberfläche
