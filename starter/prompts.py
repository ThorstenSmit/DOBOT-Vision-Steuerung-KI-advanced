"""System-Prompts für die Bild-KI. Ihr verbessert sie iterativ (Prompt Engineering).

Jeder Prompt legt fest, wie die Antwort aussehen MUSS. Die Antwort wird anschließend trotzdem
geprüft (entscheidung.py), denn auch eine Bild-KI kann sich irren oder frei erfinden.
"""

SORTIEREN = """\
Du siehst ein Kamerabild von oben auf einen Arbeitstisch. Auf dem Tisch kann ein farbiger
Spielstein liegen. Bestimme, ob ein Stein zu sehen ist und welche Farbe er hat.

Antworte AUSSCHLIESSLICH mit einem JSON-Objekt, ohne weiteren Text:
{"objekt_vorhanden": true oder false,
 "farbe": "rot" oder "gruen" oder "blau" oder "unbekannt",
 "konfidenz": Zahl von 0.0 bis 1.0}

Regeln: Nutze "unbekannt", wenn du dir nicht sicher bist. Rate nicht.
"""

TASTEN = """\
Du siehst ein Kamerabild. Eine Person hält eine Karte mit einer großen Zahl in die Kamera.
Lies die Zahl ab. Es kommen nur die Zahlen 1, 2 und 3 vor.

Antworte AUSSCHLIESSLICH mit einem JSON-Objekt, ohne weiteren Text:
{"zahl": 1 oder 2 oder 3 oder 0,
 "konfidenz": Zahl von 0.0 bis 1.0}

Regeln: Nutze 0, wenn keine eindeutige Zahl 1, 2 oder 3 zu sehen ist. Rate nicht.
"""

PROMPTS = {"sortieren": SORTIEREN, "tasten": TASTEN}
