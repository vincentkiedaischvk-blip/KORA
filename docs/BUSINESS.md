# Geschäftsmodell

Abo auf der Anbieterseite, 99 € im Monat, netto. Für Auftraggeber kostenlos.

Quelle: [`../business/KORA-Abomodell.xlsx`](../business/KORA-Abomodell.xlsx)
(Formeln, alle Eingaben veränderbar) und
[`../data/unit-economics.csv`](../data/unit-economics.csv) (dieselbe Rechnung in
Python, ohne Excel prüfbar). Beide ergeben dieselben Zahlen — die Doppelung ist
Absicht, damit ein Diff zeigt, wenn sich eine Annahme verschiebt.

## Warum die Anbieterseite zahlt

Der Auftraggeber hat Alternativen: fünf Telefonate. Der Anbieter hat keine — für
einen kleinen Betrieb ohne Vertrieb ist die Auftragslage das Problem, nicht die
Gebühr. Ein einziger vermittelter Event-Auftrag liegt bei rund 1.440 € (6 Kräfte
× 8 Stunden × 30 €). Das Jahresabo kostet 1.188 €.

Das Argument ist damit nicht der Preis, sondern die Amortisation: **ein Auftrag
deckt das Jahr.** Deshalb steht der Preis auch nicht zur Debatte — die Frage ist,
ob überhaupt Aufträge durchlaufen.

Eine Provision wäre das nähere Modell, scheitert aber daran, dass die Abrechnung
zwischen Auftraggeber und Anbieter außerhalb der Plattform stattfindet. Ohne
Zahlungsabwicklung ist eine Provision nicht durchsetzbar, sondern Vertrauenssache
— und ein Betrieb, der 8 % abführen soll, telefoniert beim zweiten Auftrag direkt.

## Zielgruppe

| | |
|---|---|
| Betriebe im WZ 80.1 | 5.330 (Destatis, Sept. 2023) |
| abzüglich Top 25 | eigener Vertrieb, nicht adressierbar |
| × 45 % adressierbar | **Annahme:** Betriebe mit Event- oder Kurzfristgeschäft |
| **Zielgruppe** | **2.387 Betriebe** |

Die 45 % sind eine Annahme, keine Erhebung. Begründung: langfristiger Werkschutz
läuft über Rahmenverträge und Ausschreibungen, nicht über einen Marktplatz. Wer
einen Standort dauerhaft bewacht, sucht keinen neuen Auftraggeber pro Woche.
Adressierbar ist das kurzfristige Geschäft — Events, Baustellen, Vertretungen.

## Annahmen

| Größe | Wert | Grundlage |
|---|---|---|
| Abopreis | 99 €/Monat | gesetzt |
| Neukunden Monat 1 | 5 | Annahme, manuelle Telefonakquise |
| Wachstum Neuabschlüsse | 15 %/Monat | Annahme |
| Obergrenze Neukunden | 60/Monat | Annahme, Kapazitätsgrenze ohne Vertriebsteam |
| Churn | 4 %/Monat | Annahme, KMU-SaaS mit monatlicher Kündbarkeit |
| CAC | 250 € | Annahme, Mix aus Eigenakquise und Paid Ads |
| Fixkosten | 8.000 €/Monat | Annahme, Team, Technik, Recht |

Belegt ist in dieser Tabelle nichts außer dem Preis, und der ist gesetzt. Das ist
kein Mangel des Modells, sondern sein Zweck: es zeigt, welche Annahme wie stark
durchschlägt.

## Projektion

| Monat | Aktive Abos | MRR | ARR | Deckungsbeitrag kumuliert | Marktdurchdringung |
|---|---|---|---|---|---|
| 1 | 5 | 495 € | 5.940 € | −755 € | 0,2 % |
| 6 | 42 | 4.158 € | 49.896 € | 2.016 € | 1,8 % |
| 12 | 125 | 12.375 € | 148.500 € | 27.355 € | 5,2 % |
| 24 | 572 | 56.628 € | 679.536 € | 289.851 € | 24,0 % |
| 36 | 933 | 92.367 € | 1.108.404 € | 1.038.570 € | 39,1 % |

Der kumulierte Deckungsbeitrag wird in **Monat 5** erstmals positiv.
**Deckungsbeitrag ist kein Gewinn** — Personal, Entwicklung und Steuern sind hier
nicht abgebildet.

## Break-even

| | |
|---|---|
| Fixkosten | 8.000 €/Monat |
| Benötigte Abos | **81** |
| entspricht Marktdurchdringung | 3,4 % |
| erreicht in | Monat 10 |

81 Betriebe von 2.387 sind eine Zahl, die man sich vorstellen kann. Das ist das
stärkste Argument des Modells: die Schwelle liegt nicht bei Marktführerschaft.

## Die kritische Zahl ist der Churn

| Churn/Monat | Lebensdauer | LTV | LTV/CAC |
|---|---|---|---|
| 4 % | 25 Monate | 2.475 € | 9,9 |
| 8 % | 12,5 Monate | 1.238 € | 5,0 |

Amortisation des CAC nach 2,5 Monaten. Sieht in beiden Fällen tragfähig aus — und
genau das ist die Falle.

**8 % sind realistisch, nicht pessimistisch.** Ein Anbieter zahlt 99 €, bekommt
drei Monate keine Anfrage und kündigt. Das ist nicht Unzufriedenheit mit dem
Produkt, sondern die korrekte Reaktion auf ein leeres Postfach. Und es passiert
zwangsläufig am Anfang, weil die Nachfrageseite später kommt als die
Angebotsseite: Anbieter lassen sich per Telefon gewinnen, Auftraggeber nicht.

Was das Modell **nicht** abbildet:

- **Die Nachfrageseite.** Es rechnet Abos, nicht Anfragen. Ohne Anfragen im
  System ist die Churn-Annahme von 4 % falsch, und dann stimmt keine Zeile der
  Projektion mehr. Das ist die einzige Zahl, die das Vorhaben kippen kann.
- **Personalkosten, Entwicklung, Steuern.**
- **Jahresverträge.** Bei 12-Monats-Bindung sinkt der Churn deutlich — die
  Abschlussquote aber auch, und bei 5 Neukunden im ersten Monat ist das der
  falsche Hebel.

## Was daraus folgt

**In der Startphase nicht 99 € nehmen.** Kostenlos oder deutlich günstiger
aufnehmen und erst auf den Zielpreis gehen, wenn nachweislich Anfragen
durchlaufen. Das verschiebt den Break-even nach hinten und ist trotzdem richtig:
ein Anbieter, der drei Monate zahlt und nichts bekommt, kündigt nicht nur, er
erzählt es weiter. In einer Branche mit 5.330 Betrieben und regionalen Netzwerken
ist das teurer als der entgangene Umsatz.

**Nachfrage zuerst messen, nicht Angebot.** Die Warteliste braucht deshalb das
Feld „Ich bin: Auftraggeber / Anbieter" und zwei getrennte Kampagnen statt eines
Adsets — sonst ist hinterher nicht auswertbar, welche Marktseite reagiert hat.
Beides ist umgesetzt, siehe [`../landing/index.html`](../landing/index.html).

## Szenarien

Jahresumsatz bei verschiedenen Preisen und Abo-Zahlen, aus der Arbeitsmappe:

| Abos ↓ / Preis → | 49 € | 79 € | 99 € | 149 € | 199 € |
|---|---|---|---|---|---|
| 50 | 29.400 € | 47.400 € | 59.400 € | 89.400 € | 119.400 € |
| 100 | 58.800 € | 94.800 € | 118.800 € | 178.800 € | 238.800 € |
| 250 | 147.000 € | 237.000 € | 297.000 € | 447.000 € | 597.000 € |
| 500 | 294.000 € | 474.000 € | 594.000 € | 894.000 € | 1.194.000 € |
| 1.000 | 588.000 € | 948.000 € | 1.188.000 € | 1.788.000 € | 2.388.000 € |
