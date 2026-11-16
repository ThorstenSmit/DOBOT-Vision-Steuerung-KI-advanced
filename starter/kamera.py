"""Zugriff auf die Webcam (oder auf ein Bild/Video zum Testen ohne Kamera)."""
import base64
import os
import sys

import cv2

BILD_ENDUNGEN = (".jpg", ".jpeg", ".png", ".bmp")


class Kamera:
    """Liefert Bilder (BGR-Arrays) von einer Webcam, einer Bilddatei oder einem Video.

    quelle: 0, 1, ... = Webcam-Nummer  |  "pfad/bild.jpg" = Standbild  |  "video.mp4" = Video
    """

    def __init__(self, quelle=0):
        self._standbild = None
        self._cap = None
        if isinstance(quelle, str) and quelle.isdigit():
            quelle = int(quelle)
        if isinstance(quelle, str) and quelle.lower().endswith(BILD_ENDUNGEN):
            if not os.path.exists(quelle):
                raise FileNotFoundError(f"Bilddatei nicht gefunden: {quelle}")
            self._standbild = cv2.imread(quelle)
            if self._standbild is None:
                raise OSError(f"Bild konnte nicht gelesen werden: {quelle}")
            return
        # unter Windows ist das DirectShow-Backend für Webcams meist zuverlässiger
        backend = cv2.CAP_DSHOW if isinstance(quelle, int) and sys.platform == "win32" else cv2.CAP_ANY
        self._cap = cv2.VideoCapture(quelle, backend)
        if not self._cap.isOpened():
            raise OSError(f"Kamera/Video '{quelle}' lässt sich nicht öffnen "
                          "(andere Nummer probieren, anderes Programm schließen?)")

    def bild(self):
        """Gibt das aktuelle Bild zurück oder None, wenn keins verfügbar ist."""
        if self._standbild is not None:
            return self._standbild.copy()
        ok, bild = self._cap.read()
        return bild if ok else None

    def schliessen(self):
        if self._cap is not None:
            self._cap.release()


def als_jpeg_base64(bild, max_breite=640, qualitaet=80) -> str:
    """Verkleinert das Bild und gibt es als base64-JPEG-Text zurück (für die KI-API)."""
    hoehe, breite = bild.shape[:2]
    if breite > max_breite:
        bild = cv2.resize(bild, (max_breite, int(hoehe * max_breite / breite)))
    ok, daten = cv2.imencode(".jpg", bild, [cv2.IMWRITE_JPEG_QUALITY, qualitaet])
    if not ok:
        raise ValueError("Bild konnte nicht als JPEG kodiert werden")
    return base64.b64encode(daten.tobytes()).decode("ascii")
