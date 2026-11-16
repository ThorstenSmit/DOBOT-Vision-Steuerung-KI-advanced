# Starter-Paket „Vision-Steuerung“

Gerüst für das Projekt [../PROJEKT.md](../PROJEKT.md). Dieses Projekt **baut auf zwei anderen auf**:

1. [DobotBasicMovement](https://github.com/ThorstenSmit/DobotBasicMovement): Verbindung zum Dobot (`dobot_helper.py`)
2. [DOBOT-Sprach-Steuerung-KI-basic](https://github.com/ThorstenSmit/DOBOT-Sprach-Steuerung-KI-basic): `grenzen.py`, `ki_client.py`, `validierung.py` (**deine fertige** `validiere()`), `ki_steuerung.py`

## 1. Einrichten (einmalig)
1. Du arbeitest in **demselben Clone** wie im Sprachprojekt (Ordner mit `dobot_helper.py`, `grenzen.py`, `validierung.py` ...). Fehlen diese Dateien, hole zuerst das Sprachprojekt nach.
2. **Alle Dateien aus diesem `starter`-Ordner** (außer dieser README) in diesen Hauptordner kopieren. Sie überschreiben nichts aus dem Sprachprojekt.
3. Pakete installieren (Umgebung aktiv: `.venv\Scripts\Activate.ps1`):
   ```powershell
   pip install -r requirements-vision.txt
   ```
4. Schlüssel und **Modell mit Bildverständnis** setzen (von der Lehrkraft; Key-Anleitung siehe [API-KEY-ANLEITUNG.md](https://github.com/ThorstenSmit/DOBOT-Sprach-Steuerung-KI-basic/blob/main/API-KEY-ANLEITUNG.md)):
   ```powershell
   $env:GROQ_API_KEY      = "dein-schluessel"
   $env:GROQ_VISION_MODEL = "bildmodell-von-der-lehrkraft"
   ```
   (`GROQ_MODEL` aus dem Sprachprojekt ist ein reines Textmodell und hier **nicht** geeignet.)

## 2. Ohne Kamera, Internet und Dobot arbeiten
Alles lässt sich mit **Tests**, einem **Testbild/Video** und der Mock-Bild-KI entwickeln:
```powershell
python -m pytest -v                       # Tests (zu Beginn rot, das ist gewollt)
python ueberwachung.py --szenario tasten --quelle testvideo.avi --mock --ohne-roboter
```
`--quelle` akzeptiert eine Kameranummer, ein Bild oder ein Video.

## 3. Die Dateien

| Datei | Inhalt | Wann bearbeiten |
|---|---|---|
| `konfig.py` | zentrale Einstellungen (ROI, Schwellen, Höhen, Fächer, Tasten) | laufend, **messen**! |
| `kamera.py` | Kamera/Bild/Video lesen, Bild als JPEG-Text | fertig, lesen |
| `trigger.py` | Objekt erkennen und einmal auslösen | **Stunde 1** |
| `ueberwachung.py` | Hauptprogramm (Schleife) | Stunde 2 und 6 |
| `prompts.py` | System-Prompts für die Bild-KI | Stunde 3 |
| `vision_client.py` | Bild an die KI senden, JSON auswerten | fertig, lesen |
| `mock_vision.py` | Mock-Bild-KI (Farbregel / Zahlenfolge) | zum Testen |
| `entscheidung.py` | Prüfung der KI-Entscheidung | **Stunde 3** |
| `kalibrierung.py` | Pixel zu mm umrechnen | **Stunde 4** |
| `kalibrieren.py` | Werkzeug zum Kalibrieren (Klicken, Eingeben) | Stunde 4 ausführen |
| `objekt.py` | Schwerpunkt eines Objekts finden | **Stunde 4** |
| `jobs.py` | Befehle planen, validieren, ausführen | **Stunde 5** |
| `rueckkopplung.py` | Ergebnis prüfen und begrenzt wiederholen (Regelkreis) | **Zusatzaufgabe** |
| `check_kamera.py` | Kameratest mit Livebild | Stunde 1 |
| `test_*.py` | Tests (je 1 bis 2 vorgegeben) | immer **zuerst** ergänzen |

## 4. Wichtig
- **Z_TISCH in `konfig.py` messen**, sonst weigert sich das Programm zu sortieren.
- Dobot in der **Home-Position darf nicht im Kamerabild (ROI) liegen**, sonst hält der Trigger den Arm für ein Objekt.
- **Keine Gesichter im Bild.** Aufnahmen gehen an einen Cloud-Dienst. Die Bilder im Ordner `aufnahmen/` und `kalibrierung.json` gehören **nicht** in Git: Prüfe vor jedem Commit mit `git status` und füge sie nicht hinzu (oder trage `aufnahmen/` in deine `.gitignore` ein).
- Nur ein Zugriff auf den Dobot gleichzeitig: Weboberfläche des Grundprojekts, DobotLink und DobotLab beenden.
- Schlüssel nie in Code oder Git.
