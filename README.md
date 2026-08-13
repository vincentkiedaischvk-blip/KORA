# KORA Safety

**Marktplatz für geprüfte Security-Dienstleistungen.** Ein Unternehmen stellt
eine Anfrage, geprüfte Anbieter in der Region werden zugeordnet, Angebote kommen
herein, der Auftraggeber vergleicht und beauftragt.

Status: Pre-Launch, Warteliste offen · [korasafety.de](https://www.korasafety.de)

```bash
git clone https://github.com/vincentkiedaischvk-blip/KORA.git
cd KORA
python3 -m http.server 8000
# → http://localhost:8000
```

Kein Build, kein Backend, keine Abhängigkeiten. Reines HTML, CSS und JavaScript.
Die Demo läuft auch per Doppelklick auf `app/index.html`.

---

## Das Problem

Ein Veranstalter braucht am Freitag sechs Sicherheitskräfte. Er ruft Betrieb für
Betrieb ab: einer hat keine Kapazität, einer meldet sich nicht, einer nennt einen
Preis ohne Vergleichswert, einer hat die Sachkunde nach § 34a nicht im Bestand.
Nach fünf Telefonaten steht ein Angebot, das niemand vergleichen kann.

Umgekehrt sitzen 5.330 Betriebe in Deutschland, von denen die meisten keine
Vertriebsabteilung haben. Die Top 25 halten rund 40 Prozent des Marktvolumens.
Die verbleibenden 60 Prozent bekommen Aufträge über Bekanntschaft — oder nicht.

Beide Seiten haben dasselbe Problem und finden sich nicht.

## Die Lösung

Eine Anfrage. KORA ordnet sie den Betrieben zu, die sie tatsächlich erfüllen
können, und lädt die drei besten zur Abgabe ein. Der Auftraggeber vergleicht
Angebote statt Telefonnotizen.

| Schritt | Auftraggeber | Anbieter |
|---|---|---|
| 01 | Bedarf eingeben — Anlass, Ort, Datum, Kräfte, Anforderung | — |
| 02 | Zuordnung sehen, Angebote erhalten | Anfrage im Postfach, Einsatz besetzen, Preis rechnen, Angebot abgeben |
| 03 | Vergleichen und beauftragen | Auftrag erhalten |

---

## Was hier echt ist und was nicht

Für einen Prototyp ist das die wichtigste Tabelle im Repository.

| | Stand |
|---|---|
| **Marktzahlen** | Belegt. Destatis, BDSW, Lünendonk — Quellen in [docs/MARKET.md](docs/MARKET.md) |
| **Erhebung von 155 Betrieben** | Echt. Google Places, Abruf 13.08.2026, 13 Städte. Aggregat in [`data/market.json`](data/market.json) |
| **Anbieter-Pool der Demo** | Synthetisch. Städteverteilung und Bewertungslage aus der echten Erhebung gezogen, die einzelne Zeile erzeugt. Warum, steht in [docs/DATA.md](docs/DATA.md) |
| **Zuordnung** | Echter Code. [`app/matching.js`](app/matching.js), harte Ausschlusskriterien plus gewichtete Rangfolge |
| **Preisrechnung** | Echt. Stundensatz × Kräfte × Stunden, Aufschlag über den Regler |
| **Abo-Modell** | Rechnung belegt, Annahmen offengelegt. Churn ist die kritische Zahl, nicht der Preis — [docs/BUSINESS.md](docs/BUSINESS.md) |
| **Konten, Zahlung, Nachweisprüfung** | Nicht gebaut. Ein Marktplatz, der „geprüft" verkauft, braucht eine echte Prüfstelle — siehe [Was fehlt](#was-fehlt) |
| **Warteliste** | Formular fertig, Endpunkt nicht gesetzt. `WAITLIST_ENDPOINT` in [`landing/index.html`](landing/index.html) |

---

## Der Kern: Zuordnung

Ohne Zuordnung ist KORA ein Formular, das Rundmails verschickt. Deshalb steht sie
sichtbar im Interface und nicht in einem Log.

Zwei Stufen, bewusst getrennt:

**1. Ausschluss.** Harte Kriterien, kein Score. Falsche Region, Leistung nicht im
Portfolio, Kapazität zu klein, Sachkunde § 34a nicht im Bestand, keine eigene
Einsatzleitung, Prüfkriterium verfehlt. Wer eine Anforderung nicht erfüllen kann,
sieht die Anfrage nie. Das ist der Teil, der das Versprechen „geprüft" trägt.

**2. Rangfolge.** Unter den geeigneten Betrieben wird gewichtet sortiert:
Bewertung 35 %, Preis 25 %, Erfahrung 15 %, Kapazitätsreserve 15 %,
Reaktionszeit 10 %. Der Preis wird innerhalb der geeigneten Menge normiert, nicht
absolut — 32 € pro Stunde sind in München anders zu lesen als in Leipzig.

Die Demo zeigt den Trichter offen: *121 im Netzwerk → 10 in Berlin → 3 erfüllen
die Anforderung → 3 angefragt*, und auf Klick, woran die anderen 118
gescheitert sind. Für einen Marktplatz, der Vertrauen verkauft, ist eine Blackbox
das falsche Werkzeug.

Ausführlich in [docs/MATCHING.md](docs/MATCHING.md).

---

## Inhalt

| Pfad | Was |
|---|---|
| [`index.html`](index.html) | Übersicht, Einstiegspunkt |
| [`app/`](app/) | Interaktive Demo, beide Marktseiten |
| [`app/matching.js`](app/matching.js) | Die Zuordnung |
| [`landing/`](landing/) | Landingpage mit Warteliste, Impressum, Datenschutz |
| [`brand/`](brand/) | Wortmarke, Farben, Schriften, Styleguide |
| [`data/`](data/) | Marktaggregat, Anbieter-Pool, Projektion |
| [`business/`](business/) | Abo-Modell als Arbeitsmappe |
| [`assets/`](assets/) | Sechs Social-Posts, vier Ads, je 1080 × 1350 |
| [`scripts/`](scripts/) | Generatoren für Daten und Assets |
| [`docs/`](docs/) | Markt, Modell, Zuordnung, Daten, Recht |

## Marke

Reine Wortmarke: **KORA** in Inter Display ExtraBold, **SAFETY** in Stahlgrau
darunter, auf die Namensbreite gesperrt. Kein Bildzeichen.

| Rolle | Hex | Verwendung |
|---|---|---|
| Off-White | `#F4F4F2` | Grundfläche |
| Ink | `#0A0A0A` | Typografie, Buttons |
| Stahlgrau | `#8A8A8A` | Sekundärzeile, Fließtext |
| Limette | `#C8F169` | Badges, Akzent — sparsam |
| Karte | `#FFFFFF` | Flächen auf Off-White |

Schriften liegen unter `brand/fonts/` (Inter, SIL Open Font License) und werden
**lokal eingebunden, nicht über `fonts.googleapis.com`**. Ein Request dorthin
überträgt die IP jedes Besuchers an Google; dafür gab es in Deutschland
reihenweise Abmahnungen, und Abschnitt 5 der Datenschutzerklärung sagt
ausdrücklich, dass es nicht passiert.

`brand/styleguide.html` zeigt alles im Browser.

## Neu erzeugen

```bash
pip3 install --user pillow openpyxl

python3 scripts/build-data.py     # → data/  (Aggregat, Anbieter-Pool, Projektion)
python3 scripts/build-social.py   # → assets/social/
python3 scripts/build-ads.py      # → assets/ads/
python3 scripts/build-model.py    # → business/KORA-Abomodell.xlsx
```

`build-data.py` arbeitet standardmäßig auf dem bereits abgeleiteten
`data/market.json`. Das Aggregat neu aus der Rohliste zu ziehen, verlangt den
Pfad zur Datei, die nicht im Repository liegt:

```bash
python3 scripts/build-data.py --leads /pfad/zu/KORA-Leads.xlsx
```

## Was fehlt

Der Prototyp beweist den Ablauf, nicht den Betrieb. Offen ist:

- **Echte Prüfstelle.** „Geprüft" ist derzeit eine Bewertungsschwelle. Belastbar
  wäre der Abruf des Bewacherregisters nach § 11b GewO, Sachkundenachweise,
  Betriebshaftpflicht, Gewerbeanmeldung.
- **Nachfrageseite.** Das Abo-Modell rechnet die Anbieterseite. Ohne Anfragen im
  System kündigen Anbieter nach zwei bis drei Monaten, dann ist die
  Churn-Annahme von 4 % deutlich zu optimistisch. Das ist das eigentliche Risiko.
- **Warteliste an einen Endpunkt hängen.** Aktuell schreibt sie nur in
  `localStorage`. Dazu Double-Opt-In.
- **Verträge.** Sobald KORA wirklich vermittelt: AGB, Anbieter-Nutzungs­bedingungen,
  erweiterte Datenschutzerklärung. Über einen Anwalt für IT-Recht, nicht über eine
  Vorlage.
- **Platzhalter im Impressum ersetzen.** Alle gelb hinterlegt, Liste in
  [docs/LEGAL.md](docs/LEGAL.md).

## Recht

Impressum und Datenschutzerklärung liegen unter `landing/legal/`. Alle
Platzhalter sind gelb hinterlegt und müssen vor dem Livegang ersetzt werden.
Die Vorlagen ersetzen keine Rechtsberatung. Details und offene Punkte in
[docs/LEGAL.md](docs/LEGAL.md).

## Lizenz

Code und Inhalte dieses Repositories: siehe [LICENSE](LICENSE).
Die Schriftfamilie Inter steht unter der SIL Open Font License, siehe
[LICENSE-FONTS.md](LICENSE-FONTS.md).
