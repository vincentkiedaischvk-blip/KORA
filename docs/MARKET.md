# Markt

## Belegte Zahlen

| Größe | Wert | Quelle |
|---|---|---|
| Branchenumsatz 2024 | 14,02 Mrd. € | BDSW |
| Prognose 2025 | rund 14,75 Mrd. € | BDSW |
| Betriebe im WZ 80.1 | 5.330 | Destatis / Bewacherregister, Strukturerhebung Dienstleistungsbereich, Stichtag Sept. 2023 |
| Tätige Personen | 232.303 | Destatis, Stichtag Sept. 2023 |
| Umsatz der Top 25 | 5,63 Mrd. € ≈ 40 % | Lünendonk-Liste 2026, ohne Geld- und Wertlogistik |

WZ 80.1 ist die Wirtschaftszweig-Klassifikation „Private Wach- und
Sicherheitsdienste". Die Zahl der Betriebe stammt aus derselben Erhebung wie die
Beschäftigtenzahl, ist also intern konsistent.

## Die Marktlücke

Die Top 25 halten rund 40 Prozent des Volumens. Die verbleibenden 60 Prozent
verteilen sich auf über 5.300 Betriebe — im Schnitt also ein Jahresumsatz im
niedrigen einstelligen Millionenbereich, bei einer langen Spitze nach unten.

**Die Konzerne kommen nicht auf einen Marktplatz.** Securitas hat einen
Vertriebsapparat, Rahmenverträge und Ausschreibungsbetreuung. Ein Marktplatz löst
für sie kein Problem, er kostet nur Marge.

**Die kleinen Betriebe haben das umgekehrte Problem.** Gute Arbeit, keine
Vertriebsabteilung, Aufträge über Bekanntschaft. Das deckt sich mit der eigenen
Erhebung: auf der Anbieterseite liegt der Median bei 37 Google-Bewertungen, das
Mittel bei 48, das Maximum bei 159. **Nach oben gibt es keine Ausreisser** —
68 Prozent liegen unter 60 Bewertungen. Und die Qualität ist da: 79 Prozent der
erhobenen Anbieter haben 4,5 Sterne oder besser, der Median liegt bei 4,9.

Der Ausreisser mit 6.323 Bewertungen in der Erhebung gehört zur
Auftraggeberseite — eine Eventlocation, kein Sicherheitsdienst. Über beide Seiten
gerechnet ergäbe das ein Mittel von 194 und ein schiefes Bild, deshalb sind alle
Kennzahlen zur Anbieterseite auf die 121 Sicherheitsdienste beschränkt.

Kleine Betriebe mit guter Arbeit und ohne Vertrieb — das ist die Zielgruppe, und
sie ist groß.

## Eigene Erhebung

155 Betriebe über Google Places, Abruf 13.08.2026.

| | |
|---|---|
| Anbieterseite (Sicherheitsdienste) | 121 |
| Auftraggeberseite | 34 — Eventagenturen, Eventlocations, Clubs, Messebau |
| Städte | 13, Schwerpunkt Berlin |

Verteilung der Anbieterseite: Berlin, Hamburg, München, Köln, Frankfurt, Leipzig,
Hannover, Düsseldorf mit je 10, Nürnberg 9, Stuttgart, Dortmund, Dresden, Bremen
mit je 8.

Aggregat in [`../data/market.json`](../data/market.json), Herkunft und
Datenschutzentscheidungen in [DATA.md](DATA.md).

**Grenzen:** ein Stichtag, keine Zeitreihe. Nur Großstädte, kein ländlicher Raum.
Und 34 Auftraggeber sind zu wenig für eine Aussage über die Nachfrage — was
bedauerlich ist, weil die Nachfrage das eigentliche Risiko ist.

## Warum jetzt

Kein Argument aus einer Marktprognose, sondern aus dem Ablauf: die kurzfristige
Beauftragung von Sicherheitspersonal läuft bis heute über Telefon und
Bekanntschaft. Es gibt keinen etablierten Marktplatz für geprüfte Anbieter in
Deutschland, während vergleichbare Gewerbe — Handwerk, Logistik, Zeitarbeit — ihre
seit Jahren haben.

Das ist kein Beweis, dass es funktioniert. Es kann genauso bedeuten, dass es schon
jemand versucht hat und die Nachfrageseite nicht zusammenkam. Genau das ist die
Frage, die die Warteliste beantworten soll, bevor mehr gebaut wird.

## Regulatorischer Rahmen

Bewachungsgewerbe ist erlaubnispflichtig nach § 34a GewO. Relevant für die
Zuordnung:

- **Unterrichtung nach § 34a Abs. 1a GewO** — 40 Stunden IHK, Mindestqualifikation
- **Sachkundeprüfung nach § 34a Abs. 1a Nr. 4 GewO** — Pflicht bei bestimmten
  Tätigkeiten, unter anderem Kontrollgängen im öffentlichen Verkehrsraum und
  Einlasskontrollen im Gastgewerbe
- **Bewacherregister nach § 11b GewO** — zentrale Erfassung, über die Sachkunde
  und Zuverlässigkeit belastbar prüfbar wären

Die Demo unterscheidet Unterrichtung, Sachkunde und Einsatzleitung als
Anforderung, weil das der Unterschied ist, an dem eine Anfrage in der Praxis
scheitert. Ein Anbieter ohne Sachkunde im Bestand darf eine Einlasskontrolle nicht
übernehmen — deshalb ist das ein hartes Ausschlusskriterium und kein Ranking-Faktor,
siehe [MATCHING.md](MATCHING.md).

**Der Abruf des Bewacherregisters ist nicht implementiert.** „Geprüft" bedeutet
derzeit eine Bewertungsschwelle. Das ist die größte Lücke zwischen dem, was das
Produkt verspricht, und dem, was es einlöst.

## Akquise

**Telefonwerbung** gegenüber Unternehmen ist nach § 7 Abs. 2 UWG nur bei
mutmaßlicher Einwilligung zulässig. Bei einem Sicherheitsdienst, dem eine
Auftragsvermittlung angeboten wird, ist die Vermutung tragfähig — der Anruf liegt
im sachlichen Interesse des Betriebs.

**Kalte Werbe-E-Mails an Firmen sind ohne Einwilligung nicht zulässig.** Auch nicht
an `info@`-Adressen, auch nicht mit Abmeldelink. Das ist der häufigste Fehler in
dieser Phase und der teuerste.
