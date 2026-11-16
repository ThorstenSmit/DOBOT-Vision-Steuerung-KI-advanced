"""Tests für die Jobplanung. Ausführen:  python -m pytest -v"""
import math

from grenzen import MAX_SCHRITT
from jobs import plane_fahrt


def test_lange_fahrt_wird_in_kurze_schritte_zerlegt():
    start, ziel = (200.0, 0.0, 50.0, 0.0), (200.0, 0.0, 50.0 + 400.0, 0.0)  # absichtlich weit
    schritte = plane_fahrt(start, ziel)
    punkte = [start[:3]] + [(s["x"], s["y"], s["z"]) for s in schritte]
    assert all(math.dist(a, b) <= MAX_SCHRITT for a, b in zip(punkte, punkte[1:]))
    assert punkte[-1] == ziel[:3]

# TODO: weitere Tests
#   - start == ziel                      -> leere Liste
#   - job_sortieren ohne konfig.Z_TISCH   -> JobFehler
#   - kompletter Job besteht fuehre_job(None, job, vorschau=True) (alle Schritte valide)
#   - Job mit Fach/Objekt außerhalb des Bereichs wird von fuehre_job abgelehnt (JobFehler)
