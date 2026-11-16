"""Bild an die Cloud-KI schicken und eine JSON-Entscheidung zurückbekommen.

Nutzt die Einstellungen und die Fehlerklasse aus dem Sprachsteuerungs-Projekt (ki_client.py).

Umgebungsvariablen:
    GROQ_API_KEY        dein API-Schlüssel (wie im Sprachprojekt)
    GROQ_VISION_MODEL   Name eines Modells, das BILDER versteht (von der Lehrkraft)
    KI_JSON_MODUS       optional "1": JSON-Modus anfordern (nicht jedes Bildmodell kann das)
"""
import json
import os
import re

import requests

from kamera import als_jpeg_base64
from ki_client import KI_URL, KIFehler


def _json_aus_text(text: str) -> dict:
    """Holt das erste JSON-Objekt aus der Antwort (Modelle packen es manchmal in ```json ... ```)."""
    treffer = re.search(r"\{.*\}", text, re.DOTALL)
    if not treffer:
        raise KIFehler(f"Antwort enthält kein JSON: {text[:120]!r}")
    try:
        daten = json.loads(treffer.group(0))
    except json.JSONDecodeError as e:
        raise KIFehler(f"Antwort ist kein gültiges JSON: {e}") from e
    if not isinstance(daten, dict):
        raise KIFehler("Antwort ist kein JSON-Objekt")
    return daten


def frage_vision(bild, system_prompt: str, nutzertext: str = "Analysiere das Bild.") -> dict:
    """Schickt ein Kamerabild (BGR-Array) mit Prompt an die KI. Gibt die Antwort als dict zurück.

    Wirft KIFehler bei Netzwerk-, Zugriffs- und Formatfehlern (der Roboter bekommt dann nichts).
    """
    schluessel = os.environ.get("GROQ_API_KEY")
    modell = os.environ.get("GROQ_VISION_MODEL")
    if not schluessel or not modell:
        raise KIFehler("GROQ_API_KEY oder GROQ_VISION_MODEL ist nicht gesetzt (siehe starter/README.md).")

    body = {
        "model": modell,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": nutzertext},
                {"type": "image_url",
                 "image_url": {"url": "data:image/jpeg;base64," + als_jpeg_base64(bild)}},
            ]},
        ],
    }
    if os.environ.get("KI_JSON_MODUS") == "1":
        body["response_format"] = {"type": "json_object"}

    try:
        antwort = requests.post(KI_URL, headers={"Authorization": f"Bearer {schluessel}"},
                                json=body, timeout=20)
        antwort.raise_for_status()
        inhalt = antwort.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code
        hinweise = {401: "Key falsch", 404: "Modellname falsch", 429: "Limit erreicht, kurz warten",
                    400: "Anfrage abgelehnt (unterstützt das Modell Bilder? JSON-Modus aus?)"}
        raise KIFehler(f"HTTP {code}: {hinweise.get(code, e.response.text[:150])}") from e
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        raise KIFehler("Keine Verbindung zur KI (Internet/Firewall?)") from e
    except (KeyError, IndexError, ValueError) as e:
        raise KIFehler(f"Unerwartetes Antwortformat: {e}") from e
    return _json_aus_text(inhalt)
