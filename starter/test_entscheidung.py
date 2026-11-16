"""Tests für die Prüfung der KI-Entscheidung. Ausführen:  python -m pytest -v

Zwei Tests sind vorgegeben. Mit dem Platzhalter sind sie ROT (red -> green). Ergänze die
übrigen Fälle (siehe Liste unten).
"""
import pytest

from entscheidung import UngueltigeEntscheidung, pruefe_entscheidung


def test_gueltige_farbe_wird_akzeptiert():
    antwort = {"objekt_vorhanden": True, "farbe": "rot", "konfidenz": 0.9}
    assert pruefe_entscheidung("sortieren", antwort) == {"farbe": "rot"}


def test_zahl_ausserhalb_1_bis_3_wird_abgelehnt():
    with pytest.raises(UngueltigeEntscheidung):
        pruefe_entscheidung("tasten", {"zahl": 7, "konfidenz": 0.95})

# TODO: weitere Tests
#   - farbe "unbekannt" oder "gelb"         -> abgelehnt
#   - objekt_vorhanden False / fehlt        -> abgelehnt
#   - konfidenz zu klein / fehlt / "hoch"   -> abgelehnt
#   - zahl "2" (Text), 2.5, True, None      -> abgelehnt
#   - antwort kein dict, unbekanntes Szenario -> abgelehnt
