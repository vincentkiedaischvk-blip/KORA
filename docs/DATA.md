# Daten

Woher die Zahlen kommen, was veröffentlicht ist und was bewusst nicht.

## Die Rohliste liegt nicht im Repository

Grundlage der Marktzahlen ist eine Erhebung von **155 Betrieben** über Google
Places, Abruf 13.08.2026, 13 Städte. Die Liste enthält Firmennamen, Anschriften,
Direktnummern, dazu eine selbst gesetzte Vertriebspriorität von A bis C.

Sie ist **nicht Teil dieses Repositories**, aus drei Gründen:

1. **Datenschutz.** Direktnummern und Anschriften realer Unternehmen sind
   personenbezogene Daten, sobald sich eine natürliche Person dahinter zuordnen
   lässt — bei Einzelunternehmen und kleinen GmbHs ist das der Normalfall. Für
   eine Veröffentlichung im Netz gibt es keine Rechtsgrundlage nach Art. 6 DSGVO.
2. **Nutzungsbedingungen.** Die Google Maps Platform Terms untersagen es,
   Inhalte dauerhaft zu speichern oder weiterzugeben, außer in engen Grenzen.
   Ein öffentliches Repository ist keine davon.
3. **Die Prioritätsspalte.** Sie stuft reale Betriebe nach Vertriebsattraktivität
   ein, „C" bedeutet unter 4,5 Sternen. Das ist eine interne Arbeitshypothese für
   die Anrufreihenfolge. Öffentlich neben einem Firmennamen ist es eine
   Bewertung, die dem Betrieb schadet und die niemand von uns hören wollte.

Wer die Datei hat, kann das Aggregat jederzeit neu ziehen:

```bash
python3 scripts/build-data.py --leads /pfad/zu/KORA-Leads.xlsx
```

`.gitignore` hält `*.xlsx` mit `Leads` im Namen aus dem Repository heraus, damit
das nicht versehentlich passiert.

## Was veröffentlicht ist

### `data/market.json` — echt, aggregiert

Kennzahlen ohne Rückschluss auf einzelne Betriebe:

- Betriebe pro Stadt, nur die Anbieterseite (121 von 155)
- Bewertungslage: Mittel 4,65, Median 4,9, Spanne 2,7 bis 5,0, Anteil ab 4,5 bei 79 %
- Bewertungsanzahl: Median 37, Mittel 48, Maximum 159, Anteil unter 60 bei 68 %
- Verteilung über Kategorien und Marktseiten
- die belegten Marktzahlen aus [MARKET.md](MARKET.md)

Die Aussage steckt in der Höhe der Zahlen, nicht in ihrer Spreizung: Median 37,
Mittel 48, Maximum 159 — **auf der Anbieterseite gibt es keine Ausreisser nach
oben.** 68 % der Betriebe liegen unter 60 Bewertungen. Das ist ein Markt aus
kleinen Betrieben ohne Vertrieb, und genau das ist die Zielgruppe.

Der oft zitierte Ausreisser mit 6.323 Bewertungen steht in der Erhebung, gehört
aber zur **Auftraggeberseite** — eine Eventlocation, kein Sicherheitsdienst.
Über beide Seiten gerechnet ergibt das ein Mittel von 194 und ein irreführendes
Bild. Deshalb sind alle Kennzahlen hier auf die 121 Anbieter beschränkt.

### `data/providers.json` und `providers.js` — synthetisch

121 Anbieter für die Demo. **Firmennamen sind Platzhalter und bezeichnen keinen
realen Betrieb.**

Echt übernommen ist die Form des Marktes:

- Anzahl der Betriebe pro Stadt, exakt wie erhoben
- Bewertungen gezogen aus der Häufigkeitstabelle der Erhebung
  (`anbieter_bewertung.histogramm`, auf 0,1 gerundet) statt aus einer
  unterstellten Verteilung. Die echte Lage ist linksschief — Median 4,9 liegt
  über dem Mittel 4,65 —, und das bekommt eine Glockenkurve nicht hin: ein
  erster Versuch mit Normalverteilung landete bei Median 4,60 und 66 % ab 4,5
  statt 4,90 und 79 %
- Bewertungsanzahl über die Umkehrung der empirischen Verteilungsfunktion,
  linear zwischen den Dezilen interpoliert. Eine Lognormalverteilung lag beim
  Median richtig und beim Maximum um den Faktor neun daneben (1.422 statt 159)
- Betriebsgrößen lognormal, Median rund 12 Kräfte

Erzeugt statt übernommen ist alles, was einen Betrieb identifizieren würde. Das
ist keine Kosmetik: hätte ich echte Bewertungen und echte Bewertungsanzahlen mit
echter Stadt kombiniert, wäre ein Betrieb mit 4,9 Sternen und 28 Bewertungen in
Bremen in einer Minute gefunden. Die Kombination ist der Identifikator, nicht der
Name.

Der Seed ist fest (`20260813`). Dieselbe Demo zeigt bei jedem Aufruf dieselben
Anbieter — sonst ist ein Vorführtermin nicht wiederholbar.

Frei erfunden, weil in der Erhebung nicht enthalten: Stundensätze (26–44 €,
marktüblich), Leistungsportfolios, Sachkunde-Bestand (62 %), eigene
Einsatzleitung (55 %), Reaktionszeiten. Wer echte Werte hat, ersetzt sie in
`build_providers()`.

### `data/unit-economics.csv` und `.js`

36-Monats-Projektion des Abo-Modells, in Python nachgerechnet. Ergibt dieselben
Werte wie die Arbeitsmappe: Monat 12 → 125 Abos, Monat 24 → 572, Monat 36 → 933.
Der Sinn der Doppelung ist Prüfbarkeit — eine CSV liest sich ohne Excel und ein
Diff zeigt, wenn sich eine Annahme geändert hat. Herleitung in
[BUSINESS.md](BUSINESS.md).

## Erzeugungskette

```
KORA-Leads.xlsx  (lokal, nicht im Repo)
        │
        │  scripts/build-data.py --leads …
        ▼
data/market.json ──────────────┬──► data/market.js        (Übersichtsseite)
   (echt, aggregiert)          │
                               └──► data/providers.json   (synthetisch, Seed)
                                    data/providers.js     (für file://)

ASSUMPTIONS in build-data.py ──────► data/unit-economics.csv
                                     data/unit-economics.js
```

`.json` ist die Fassung für Menschen und Werkzeuge, `.js` dieselben Daten als
`window.KORA_*`. Die Doppelung hat einen Grund: ein `fetch()` auf eine lokale
`.json` scheitert an der Same-Origin-Regel, wenn die Demo per Doppelklick über
`file://` geöffnet wird. Ein `<script src>` nicht. Damit läuft die Anwendung ohne
Server und mit Server gleich, und ein Vorführtermin hängt nicht daran, dass
jemand `python3 -m http.server` findet.

## Bekannte Grenzen

- **Google-Bewertungen sind ein Hilfsmerkmal, kein Qualitätsnachweis.** Sie sind
  manipulierbar, altersabhängig und sagen über die Sachkunde nach § 34a nichts.
  In der Zuordnung tragen sie derzeit 35 % — das ist zu viel für eine Zahl dieser
  Güte und nur damit zu rechtfertigen, dass es die einzige verfügbare ist.
- **Ein Stichtag.** Abruf 13.08.2026, keine Zeitreihe. Ob ein Betrieb wächst oder
  schrumpft, ist nicht erkennbar.
- **13 Städte, Schwerpunkt Berlin.** Kein ländlicher Raum. Ob der Ablauf dort
  trägt, wo drei Betriebe im Umkreis von 50 km sitzen, ist offen.
- **Nur die Anbieterseite ist quantifiziert.** 34 Auftraggeber-Leads sind zu
  wenig für eine Aussage über die Nachfrage — und die Nachfrage ist das Risiko,
  nicht das Angebot.
