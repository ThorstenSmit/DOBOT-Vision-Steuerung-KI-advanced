# Projekt: „Der Roboter, der selbst entscheidet“ – Kamera + KI + Dobot Magician

## Die Projektfrage

> **Wie kann ein Roboter selbstständig auf Ereignisse in der realen Welt reagieren, wenn eine KI die Entscheidung trifft, und dabei trotzdem sicher bleiben?**

Beim Sprachprojekt hat ein Mensch jeden Befehl eingetippt. Jetzt **beobachtet** ein System seine Umgebung selbst: Eine Webcam überwacht den Arbeitstisch. Passiert etwas (der **Trigger**), fragt das Programm eine Cloud-KI, **was zu tun ist**, prüft die Antwort und führt am Dobot einen **Job** aus. Niemand tippt etwas ein. Genau deshalb ist die Sicherheit wichtiger als je zuvor.

## Wähle ein Szenario (pro Team eins, das zweite als Erweiterung)

**Szenario A – Sortierstation:** Ein farbiger Spielstein wird auf den Tisch gelegt. Die KI erkennt die **Farbe**. Der Dobot nimmt den Stein mit dem **Saugnapf** auf und legt ihn im Fach der passenden Farbe (rot, grün, blau) ab.

**Szenario B – Fahrstuhl-Tasten:** Jemand hält eine **Karte mit einer Zahl** (1, 2 oder 3) in die Kamera. Die KI **liest die Zahl**. Der Dobot **drückt den passenden von drei Tastern**.

Beide Szenarien haben denselben Aufbau:
```
Kamera ──► TRIGGER ──► Bild an KI ──► ENTSCHEIDUNG prüfen ──► JOB planen ──► validieren ──► Bestätigung ──► Dobot
(Dauerbild) (Objekt     (nur dann!)    (Farbe / Zahl gültig?)   (Befehlsliste) (Sprachprojekt) (j/N)         (STOPP)
            liegt ruhig)                                         ▲
                                         Objektposition: klassische Bildverarbeitung + Kalibrierung
```

### Drei Entwurfsgrundsätze
1. **Die KI entscheidet, WAS. Klassische Bildverarbeitung misst, WO.** Sprachmodelle sind schlecht bei exakten Pixelkoordinaten. Die Position des Steins bestimmt deshalb OpenCV, die Farbe die KI.
2. **Die KI wird nur bei einem Trigger gefragt**, nicht 30-mal pro Sekunde. Das spart Kontingent, Zeit und Geld.
3. **Mehrere Sicherheitsschichten:** Trigger → Prüfung der KI-Entscheidung → Validierung jedes Roboterbefehls (aus dem Sprachprojekt) → Bestätigung → Stopp.

## Voraussetzungen
- Grundprojekt [DobotBasicMovement](https://github.com/ThorstenSmit/DobotBasicMovement) in deinem Clone, der Dobot fährt.
- **Das Sprachprojekt ist erledigt**: Im selben Ordner liegen `grenzen.py`, `ki_client.py`, `validierung.py` (mit **deiner** fertigen `validiere()`) und `ki_steuerung.py` aus dem Projekt [DOBOT-Sprach-Steuerung-KI-basic](https://github.com/ThorstenSmit/DOBOT-Sprach-Steuerung-KI-basic). Dieses Projekt **baut darauf auf** und nutzt es.
- Das **Starter-Paket** dieses Projekts (Ordner `starter/`, Anleitung in [starter/README.md](starter/README.md)) ist in denselben Ordner kopiert, `pip install -r requirements-vision.txt` ausgeführt.
- API-Schlüssel und der Name eines **bildfähigen Modells** (von der Lehrkraft oder mit eigenem Key nach [der API-Key-Anleitung](https://github.com/ThorstenSmit/DOBOT-Sprach-Steuerung-KI-basic/blob/main/API-KEY-ANLEITUNG.md)).
- Hardware am Platz: Webcam mit Halterung (schaut senkrecht von oben auf das Arbeitsfeld), Saugnapf-Aufsatz, Spielsteine und drei Ablagefächer (A) bzw. drei Taster und Zahlenkarten (B).

## Zeitplan: 6 Stunden in 3 Wochen

| | LF 11a – Funktionalität | LF 10a – Benutzerschnittstelle |
|---|---|---|
| **Woche 1** | **Stunde 1:** Kamera und Trigger | **Stunde 2:** Überwachungsoberfläche |
| **Woche 2** | **Stunde 3:** Bild-KI und Prüfung der Entscheidung | **Stunde 4:** Kalibrierung und Objektposition |
| **Woche 3** | **Stunde 5:** Jobplanung und Sicherheit | **Stunde 6:** Integration, Bedienung, Abnahme |

Arbeitet in **Zweierteams**. Fast alles lässt sich **ohne Dobot und ohne Internet** entwickeln und testen: mit synthetischen Testbildern, einem Video und der **Mock-Bild-KI** (`mock_vision.py`). Den Dobot braucht ihr nur zum Messen (Stunde 4, 5) und für die Abnahme (Stunde 6).

---

## Stunde 1 (LF 11a): Kamera und Trigger

**Ziel:** Das Programm erkennt, dass ein Objekt auf dem Tisch liegt, und löst **genau einmal** aus.

1. Webcam anschließen, `python check_kamera.py` starten. Richtet die Kamera **senkrecht von oben** auf das Arbeitsfeld aus. **Keine Gesichter im Bild!** (Das Bild geht später an einen Cloud-Dienst.) Passt `ROI` und `KAMERA` in `konfig.py` an.
2. Implementiert in `trigger.py` die Methoden `_belegte_flaeche()` und `pruefe()`. Idee: Bild mit einem Hintergrundbild vergleichen (`cv2.absdiff`), Pixel über einer Schwelle zählen und erst auslösen, wenn das Objekt **mehrere Bilder in Folge ruhig** liegt.
3. **Tests zuerst:** `python -m pytest -v test_trigger.py`. Zwei Tests sind vorgegeben, ergänzt eigene (vorbeiziehende Hand, erneutes Auflegen).

**Fragen:** Warum soll der Trigger nur **einmal** auslösen? Was passiert bei einer Hand, die den Stein platziert? Was bei einer Lichtänderung?

**Ergebnis:** Trigger besteht die Tests und reagiert auf der echten Kamera auf einen Stein.

## Stunde 2 (LF 10a): Überwachungsoberfläche

**Ziel:** Das Programm ist **bedienbar und nachvollziehbar**: Man sieht, was es gerade tut.

1. Startet `python ueberwachung.py --szenario sortieren --mock --ohne-roboter --zeige` (nutzt noch Platzhalter, erst Stunde 3 bis 6 füllen die Lücken).
2. Verbessert `zeichne_status()` und die Konsolenmeldungen: Bereich (ROI) und **Status** (`Überwache`, `Pause`, `KI fragt`, `Job läuft`) im Livebild einblenden, verständliche Meldungen statt Fachbegriffen.
3. Gestaltet die **Konfiguration**: Welche Werte (ROI, Schwelle, Cooldown) lassen sich ohne Code-Änderung anpassen? (z. B. Kommandozeilenparameter oder Datei)
4. Legt fest, **wie der Nutzer eingreifen kann**: Bestätigung j/N, Beenden mit `q` oder Strg+C. Wie erfährt er, warum ein Job **nicht** gestartet wurde?

**Ergebnis:** Livebild mit Statusanzeige, klare Meldungen, dokumentierte Bedienung.

## Stunde 3 (LF 11a): Bild-KI und Prüfung der Entscheidung

**Ziel:** Das Kamerabild an eine KI schicken und die Antwort **sicher** auswerten.

1. Setzt `GROQ_API_KEY` und `GROQ_VISION_MODEL`, prüft mit einem Testbild (`vision_client.py` ist fertig, ihr lest es und versteht, wie das Bild als Text kodiert wird).
2. Verbessert den Prompt in `prompts.py` (Szenario A oder B). Protokolliert: Was war falsch, was habt ihr geändert, was hat es gebracht?
3. Implementiert `pruefe_entscheidung()` in `entscheidung.py`: Farbe nur aus der Whitelist, Zahl nur 1 bis 3 als **echte** ganze Zahl, **Konfidenz** über der Schwelle, „kein Objekt“ gibt keinen Job.
4. **Tests zuerst:** `python -m pytest -v test_entscheidung.py` (zwei vorgegeben, ergänzt die Liste im Testfile).
5. **Vergleich:** Lasst dasselbe Bild von der echten KI und von der Mock-KI (`mock_vision.py`, einfache Farbregel) bewerten. Wann ist die KI besser, wann schlechter? Lohnt sie sich für diese Aufgabe?

**Ergebnis:** Entscheidung kommt als geprüftes Ergebnis zurück oder als verständlicher Fehler. Alle Tests grün.

## Stunde 4 (LF 10a): Kalibrierung und Objektposition

**Ziel:** Aus dem Bildpunkt (Pixel) die Position am Roboter (mm) berechnen. Gilt für Szenario A. Für Szenario B legt ihr stattdessen die Tasterpositionen in `konfig.TASTEN` fest.

1. Legt 5 Markierungen (Klebepunkte) auf den Tisch. Fahrt mit der Weboberfläche des Grundprojekts die Dobot-Spitze nacheinander über jede Markierung und **notiert x und y**.
2. Implementiert `berechne_matrix()` und `pixel_zu_mm()` in `kalibrierung.py` (Perspektivtransformation mit OpenCV). Tests: `python -m pytest -v test_kalibrierung.py`.
3. Führt `python kalibrieren.py` aus: Foto aufnehmen, Markierungen anklicken, Koordinaten eingeben. Das Programm zeigt den **Fehler an einem unabhängigen Kontrollpunkt**. Ziel: **unter 5 mm** (sonst verfehlt der Saugnapf den Stein). Wiederholt bei zu großem Fehler.
4. Implementiert `finde_schwerpunkt()` in `objekt.py` (Kontur finden, Momente berechnen, **ROI-Versatz** addieren).

**Fragen:** Warum genügen 4 Punkte? Warum ein fünfter zur Kontrolle? Was passiert, wenn die Kamera nach der Kalibrierung verrutscht?

**Ergebnis:** Der Schwerpunkt eines Steins wird in mm umgerechnet, Fehler unter 5 mm.

## Stunde 5 (LF 11a): Jobplanung und Sicherheit

**Ziel:** Aus der Entscheidung eine **sichere Folge von Roboterbefehlen** machen.

1. **Messt `Z_TISCH`:** Fahrt mit der Weboberfläche **sehr langsam von oben**, bis der Saugnapf die Tischplatte berührt, und lest z ab. Tragt den Wert in `konfig.py` ein. Die Standard-Grenze (z ≥ 0) schützt den Tisch. Mit `passe_grenzen_an()` senkt ihr sie **bewusst** (z. B. `Z_TISCH − 2`). Dokumentiert diese Entscheidung und begründet sie.
2. Implementiert `plane_fahrt()`: Lange Bewegungen werden in Teilstücke zerlegt, weil `validiere()` aus dem Sprachprojekt Schritte über `MAX_SCHRITT` ablehnt. (Hier greifen **zwei Sicherheitskonzepte** ineinander.)
3. Szenario A: Implementiert `job_sortieren()` (über den Stein, absenken, ansaugen, anheben, zum Fach, absenken, loslassen, anheben, Home). Szenario B nutzt das fertige `job_druecke_taste()` als Vorbild.
4. **Tests zuerst:** `python -m pytest -v test_jobs.py`. Testet auch, dass ein Job mit Ziel außerhalb des Bereichs **abgelehnt** wird.

**Ergebnis:** Jobs bestehen `fuehre_job(None, job, vorschau=True)` (Simulation), Tests grün.

## Stunde 6 (LF 10a): Integration, Bedienung, Abnahme

1. Setzt alles zusammen: `python ueberwachung.py --szenario sortieren` (bzw. `tasten`). Erst `--mock --ohne-roboter`, dann mit echter KI, zuletzt mit Dobot.
2. **Bedienung:** Der Nutzer sieht den **geplanten Ablauf** vor jedem Job und bestätigt mit `j`. Der Notaus muss **jederzeit** funktionieren: `Strg+C` bzw. `q` stoppt den Arm. Der Dobot-Schalter bleibt der echte Not-Aus.
3. **Abnahme-Challenge:** Löst die Fälle **gezielt aus** und zeigt, dass kein Job startet (oder sicher abgebrochen wird):

| Fall | Wie auslösen? | Erwartetes Verhalten |
|---|---|---|
| Hand fährt durch das Bild | Hand über den Tisch bewegen | Kein Trigger |
| Tisch leer / unbekannte Farbe | leeres Bild bzw. gelber Stein | Entscheidung abgelehnt, kein Job |
| KI antwortet unsicher oder Unsinn | Mock-Szenario `tasten` (liefert 7) | `pruefe_entscheidung` lehnt ab |
| Internet weg | WLAN trennen | KI-Fehler gemeldet, kein Job |
| Objekt außerhalb des Arbeitsbereichs | Stein weit am Rand | Validierung lehnt Job ab |
| Stopp während des Jobs | Strg+C mitten im Job | Arm hält an, Programm beendet sauber |

4. **Kurzpräsentation** (je Team ca. 4 min): Live-Demo eines erfolgreichen und eines abgelehnten Falls, dazu eine Antwort auf eine Reflexionsfrage.

**Ergebnis:** Lauffähiges System, abgenommene Challenge, Präsentation.

---

## Zusatzaufgabe: Rückkopplung (Schritt zu echter Physical AI)

Bisher ist die Kette **offen**: Trigger → Entscheidung → Job, und danach nimmt das Programm einfach an, dass alles geklappt hat. Ein Roboter in der echten Welt darf das nicht. Der Saugnapf kann den Stein verfehlen, ihn unterwegs verlieren oder er rutscht. Ein **geschlossener Regelkreis** prüft das Ergebnis und reagiert. Das ist der wichtigste Schritt von „KI-gestützter Robotik“ zu **Physical AI** (siehe [README](README.md), Abschnitt „Einordnung“).

**Aufgabe (Szenario A):** Nach dem Job prüft die Kamera, ob der Stein **wirklich im richtigen Fach liegt**. Wenn nicht, wird der Job wiederholt, aber höchstens **zweimal**, danach bricht das Programm mit einer klaren Meldung ab.

1. **Soll-Zustand festlegen:** Wo (in Pixeln) liegt das Fach? Die Fachposition steht in Millimetern in `konfig.FAECHER`. Mit der **inversen Kalibriermatrix** (`np.linalg.inv(matrix)`, dann `cv2.perspectiveTransform`) rechnet ihr sie in Bildpixel um.
2. **Ergebnis prüfen:** Im Starter liegt das Gerüst `rueckkopplung.py`. Implementiert `fach_pixel()` (Millimeter in Pixel, mit der inversen Matrix) und `pruefe_ergebnis(bild, hintergrund, fach_xy, matrix, alt_px)`. Vor dem Prüfen muss der **Arm aus dem Bild** sein (Home-Position). Vergleicht den Fach-Ausschnitt mit dem Hintergrund (wie im Trigger) und prüft zusätzlich, dass **am alten Ort kein Stein mehr liegt** (`alt_px`).
3. **Regelkreis bauen:** Implementiert `fuehre_mit_rueckkopplung()` (Schleife mit Zähler, höchstens 2 Wiederholungen) und bindet sie in `ueberwachung.py` ein: Job ausführen → **frisches** Bild (Webcams liefern anfangs veraltete Bilder, also einige Bilder verwerfen) → `pruefe_ergebnis()` → bei Misserfolg neu planen und wiederholen, danach Abbruch mit Meldung. **Jeder Wiederholungsjob läuft wieder durch die vollständige Validierung. Ein Fehler der Validierung wird nie „einfach nochmal versucht“.**
4. **Tests zuerst** (`python -m pytest -v test_rueckkopplung.py`, ohne Roboter, mit synthetischen Bildern; zwei sind vorgegeben): Stein im Fach → `True`. Fach leer → `False`. Stein noch am alten Ort → `False`. Stein im falschen Fach → `False`. Erfolg im 2. Versuch. Sicherheitsfehler werden nicht wiederholt.
5. **Fehlerfälle zeigen:** Nehmt dem Saugnapf die Wirkung (Schlauch kurz abziehen) oder legt den Stein von Hand zurück, und zeigt, dass das Programm es merkt, wiederholt und nach dem zweiten Misserfolg sauber abbricht.

**Fragen:** Was ist der Unterschied zwischen *Steuerung* und *Regelung*? Warum braucht man ein Wiederholungslimit? Welche Fehler erkennt die Kamera nicht (z. B. Stein liegt schief im Fach)? Wie viel Vertrauen verdient die Prüfung selbst?

**Hinweis für Szenario B:** Prüft statt des Fachs, ob der Taster gedrückt wurde. Das geht nur mit einer Rückmeldung (z. B. eine LED am Taster, die die Kamera sieht).

## Erweiterungen (für Schnelle)
- **Beide Szenarien** in einem Programm, je nach Bild.
- **Weitere Schritte zu Physical AI:** mehrschrittige Planung („Sortiere alle Steine“), eigenes kleines Modell mit selbst gesammelten Bildern trainieren und mit der Cloud-KI vergleichen, Sichtführung während der Fahrt.
- **Qualitätskontrolle:** KI unterscheidet „gut“ und „schlecht“ (z. B. heile und defekte Teile) und sortiert in zwei Fächer.
- **Mehrere Steine nacheinander** abarbeiten.
- **Protokoll** aller Entscheidungen (Zeit, Bild, KI-Antwort, Job, Ergebnis) als Datei mit Bildern.
- **Hand-Schutz:** Wird eine Hand im Arbeitsbereich erkannt, startet oder stoppt kein Job.
- **Hintergrund nachführen**, damit langsame Lichtänderungen keinen Trigger auslösen.

## Bewertungskriterien
| Kriterium | Beschreibung |
|---|---|
| Funktion | Trigger, Entscheidung und Job funktionieren am echten Aufbau |
| Sicherheit | Entscheidung und alle Befehle werden geprüft, Tests vorhanden, Stopp funktioniert |
| Robustheit | Alle Fälle der Abnahme-Challenge sind abgefangen |
| Bedienbarkeit | Status sichtbar, verständliche Meldungen, Bestätigung, Abbruch (LF 10a) |
| Genauigkeit | Kalibrierfehler unter 5 mm, dokumentiert |
| Zusatz: Rückkopplung | Ergebnis wird geprüft, Wiederholungslimit, Tests vorhanden |
| Code-Qualität | Aufgeteilt in Module, lesbar, kommentiert, Wiederverwendung des Sprachprojekts |
| Geheimnisse und Daten | Kein API-Key im Repository, Kamera ohne Gesichter |
| Dokumentation | Prompt-Entwicklung, Entscheidungen (Grenzen, Schwellen) und Messwerte dokumentiert |

## Reflexionsfragen
1. Warum fragt das Programm die KI nur nach einem Trigger und nicht dauernd?
2. Wann ist die einfache Farbregel (Mock) besser als die KI, wann nicht? Was sind Kosten, Tempo, Genauigkeit?
3. Welche Daten verlassen beim Aufruf euren Rechner (Bilder!)? Was folgt daraus für den Kameraaufbau?
4. Wer trägt die Verantwortung, wenn ein autonomes System einen Fehler macht: Entwickler, Betreiber, KI-Anbieter?
5. Was ändert sich, wenn nicht ein Dobot, sondern ein Industrieroboter in der Nähe von Menschen arbeitet?

## Sicherheit am Roboter
- Der Dobot bewegt sich hier **ohne Tastendruck**. Niemand greift in den Arbeitsbereich, solange die Überwachung läuft.
- Nur eine Person bedient den Rechner, alle anderen halten Abstand. Dobot-Schalter in Reichweite.
- Vor dem ersten Lauf mit Roboter immer **Vorschau und Bestätigung** (kein `--auto`).
- Die untere z-Grenze nur nach dem **Messen** und mit Reserve senken.
