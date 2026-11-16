"""Prüfung der KI-Entscheidung (das Sicherheitsnetz für die Bild-KI).

Wie im Sprachprojekt gilt: Nichts, was die KI liefert, wird ungeprüft zur Aktion.
Auch eine Bild-KI kann halluzinieren: Farbe erfinden, eine Zahl 5 lesen, obwohl nur 1 bis 3
erlaubt sind, oder bei einem leeren Tisch trotzdem "rot" melden.

STUNDE 3 (LF 11a): Implementiere pruefe_entscheidung().
"""

FARBEN = {"rot", "gruen", "blau"}
ZAHLEN = {1, 2, 3}
MIN_KONFIDENZ = 0.7


class UngueltigeEntscheidung(ValueError):
    """Die KI-Antwort ist unbrauchbar oder unsicher: es darf KEIN Job gestartet werden."""


def pruefe_entscheidung(szenario: str, antwort) -> dict:
    """Prüft die KI-Antwort und gibt eine bereinigte Entscheidung zurück.

    Rückgabe sortieren: {"farbe": "rot"|"gruen"|"blau"}
    Rückgabe tasten:    {"zahl": 1|2|3}
    Sonst: UngueltigeEntscheidung mit verständlicher Meldung.

    TODO (Placeholder akzeptiert alles, UNSICHER!). Prüfe:
      - ist antwort ein dict, szenario bekannt?
      - sortieren: objekt_vorhanden muss True sein; farbe in FARBEN ("unbekannt" ablehnen)
      - tasten:    zahl muss eine ECHTE ganze Zahl in ZAHLEN sein (kein "2", kein 2.5, kein True)
      - konfidenz: Zahl zwischen 0 und 1 (kein bool, kein NaN) und >= MIN_KONFIDENZ
    """
    if szenario == "sortieren":
        return {"farbe": antwort.get("farbe")}
    return {"zahl": antwort.get("zahl")}
