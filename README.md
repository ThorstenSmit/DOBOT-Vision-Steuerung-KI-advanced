# DOBOT-Vision-Steuerung-KI-advanced

**Aufbauprojekt für Fachinformatiker/-innen Anwendungsentwicklung (3. Lehrjahr):** Eine Webcam überwacht den Arbeitstisch. Bei einem **Trigger** entscheidet eine **Bild-KI**, was zu tun ist, und ein **Dobot Magician** führt den Job aus. Zum Beispiel Steine nach Farbe sortieren oder einen von drei Tastern drücken.

> **Projektfrage:** Wie kann ein Roboter selbstständig auf Ereignisse in der realen Welt reagieren, wenn eine KI die Entscheidung trifft, und dabei trotzdem sicher bleiben?

```
Kamera ──► TRIGGER ──► Bild-KI ──► Entscheidung prüfen ──► Job planen ──► validieren ──► Dobot
```

## Einordnung: Vorstufe zu Physical AI
Dieses Projekt ist **keine vollständige Physical AI**, sondern eine **Vorstufe** (KI-gestützte Robotik): ein Einstieg, der die nötige Ingenieursarbeit rund um die KI übt.

*Physical AI* meint Systeme, die die physische Welt **wahrnehmen**, selbst **entscheiden** und **handeln**, im Idealfall in einem **geschlossenen Regelkreis** (der Roboter prüft sein Ergebnis und korrigiert) und oft mit einer KI, die das Handeln selbst lernt oder steuert. Der Begriff ist unscharf. Im weiteren Sinn passt dieses Projekt teilweise.

| | Dieses Projekt |
|---|---|
| Wahrnehmung | Kamera (echte Welt) |
| Rolle der KI | **erkennt** (Farbe oder Zahl) und liefert die Entscheidung |
| Handeln | klassisch skriptiert, Bewegung steuert nicht die KI |
| Rückkopplung | keine (offene Kette: Trigger → Entscheidung → Job) |
| Lernen | nein |

Es ist eine **Sense-Think-Act-Pipeline mit KI als Entscheider**. Was ihr dabei lernt, braucht jedes Physical-AI-System: Sensoren anbinden, KI-Antworten prüfen, Kalibrierung, Sicherheit, Fehlerbehandlung.

**Was zu echter Physical AI noch fehlt** (mögliche Erweiterungen):
1. **Rückkopplung:** Nach dem Ablegen prüft die Kamera, ob der Stein im Fach liegt, und wiederholt den Job bei Misserfolg.
2. **Mehrschrittige Planung:** Die KI entscheidet nach jedem Schritt neu („Sortiere alle Steine“).
3. **Eigenes Lernen:** Der Roboter lernt aus eigener Erfahrung, besser zu greifen (umgesetzt im Folgeprojekt unten). Oder: Mit selbst gesammelten Bildern ein kleines Modell trainieren und mit der Cloud-KI vergleichen.
4. **Sichtgeführte Bewegung:** Die Kamera korrigiert die Position während der Fahrt.

## Dieses Projekt baut auf zwei anderen auf
1. **[DobotBasicMovement](https://github.com/ThorstenSmit/DobotBasicMovement)**: Dobot anschließen und steuern.
2. **[DOBOT-Sprach-Steuerung-KI-basic](https://github.com/ThorstenSmit/DOBOT-Sprach-Steuerung-KI-basic)**: KI-Anbindung und die Sicherheitsvalidierung `validiere()`, die hier wiederverwendet wird.

Beide müssen erledigt sein und im **selben Clone-Ordner** liegen.

## Wie es weitergeht
Nach diesem Projekt folgt [DOBOT-Lernender-Greifer-KI-expert](https://github.com/ThorstenSmit/DOBOT-Lernender-Greifer-KI-expert): Der Roboter lernt durch eigene Versuche, besser zu greifen, und bewertet seine Fortschritte mit Statistik. Es nutzt die **Rückkopplung** aus diesem Projekt (Zusatzaufgabe) als Erfolgsmessung. Wer es später bearbeiten will, sollte sie hier umsetzen.

## Los geht's
1. **[PROJEKT.md](PROJEKT.md)** lesen: Szenarien, Zeitplan (6 Stunden in 3 Wochen), Aufgaben, Abnahme, Bewertung.
2. **[starter/README.md](starter/README.md)** folgen: Starter-Dateien in den Clone kopieren, Pakete installieren, Schlüssel und Bildmodell setzen.
3. Tests schreiben, Modul für Modul füllen, erst ohne Roboter, dann am Dobot.

## Inhalt

| Pfad | Zweck |
|---|---|
| [PROJEKT.md](PROJEKT.md) | Projektbeschreibung und Aufgaben für Teams |
| [starter/](starter/) | Gerüst: Kamera, Trigger, Bild-KI-Client, Mock, Kalibrierung, Jobs, Tests |

## Sicherheit und Datenschutz
- Der Dobot bewegt sich **ohne Tastendruck**: Arbeitsbereich frei, nur eine Person bedient, Dobot-Schalter in Reichweite.
- Kamerabilder gehen an einen Cloud-Dienst: **keine Gesichter im Bild.**
- API-Schlüssel gehören **nie** in Code, Git oder Chats.

## Lizenz
MIT, siehe [LICENSE](LICENSE).
