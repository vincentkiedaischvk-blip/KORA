# Zuordnung

Wie aus einer Anfrage und 121 Betrieben drei Angebote werden.
Implementierung: [`../app/matching.js`](../app/matching.js).

## Warum das der Produktkern ist

Ein Marktplatz, der jede Anfrage an alle verschickt, produziert zwei Probleme
gleichzeitig. Der Auftraggeber bekommt Angebote von Betrieben, die den Auftrag
nicht erfüllen können. Und der Anbieter bekommt Anfragen, die ihn nichts angehen —
nach der dritten liest er sie nicht mehr, nach der zehnten kündigt er das Abo.

Die Zuordnung entscheidet damit über beide Seiten der Bilanz: über die
Vergleichbarkeit für den Auftraggeber und über den Churn auf der Anbieterseite,
die kritischste Zahl im [Geschäftsmodell](BUSINESS.md).

## Stufe 1 — Ausschluss

Harte Kriterien. Kein Score, keine Gewichtung, entweder oder. Reihenfolge ist die
der Prüfung:

| Kriterium | Ausschluss wenn |
|---|---|
| Region | Betrieb sitzt nicht in der angefragten Stadt |
| Portfolio | angefragte Leistung nicht im Angebot |
| Prüfung | Bewertung unter 4,3 |
| Kapazität | `max_kraefte` kleiner als die angefragte Zahl |
| Sachkunde § 34a | Anforderung verlangt Sachkunde, Betrieb hat sie nicht im Bestand |
| Einsatzleitung | Anforderung verlangt Einsatzleitung vor Ort, Betrieb stellt keine |

Wer eines dieser Kriterien verfehlt, sieht die Anfrage nie. Das ist der Teil, der
das Versprechen „geprüft" trägt — er darf nicht verhandelbar sein, sonst ist es
kein Versprechen, sondern eine Präferenz.

Die Schwelle von 4,3 Sternen ist eine gesetzte Zahl, keine gefundene. In der
Erhebung liegen 79 % der Betriebe bei 4,5 oder besser; die Schwelle schneidet
also das untere Fünftel ab. Sobald eine echte Prüfstelle existiert
(Bewacherregister nach § 11b GewO, Sachkundenachweise, Betriebshaftpflicht),
gehört sie ersetzt — eine Google-Bewertung ist ein Hilfsmerkmal, kein Nachweis.

## Stufe 2 — Rangfolge

Unter den geeigneten Betrieben wird gewichtet sortiert. Summe der Gewichte 1,0.

| Merkmal | Gewicht | Normierung |
|---|---|---|
| Bewertung | 0,35 | linear zwischen 2,7 (schlechtester Wert der Erhebung) und 5,0 |
| Preis | 0,25 | invertiert, innerhalb der geeigneten Menge |
| Erfahrung | 0,15 | `log10` der Bewertungsanzahl, Decke 160 |
| Kapazitätsreserve | 0,15 | `max_kraefte / bedarf`, Optimum bei doppelter Kapazität |
| Reaktionszeit | 0,10 | invertiert, zwischen 4 und 90 Minuten |

Drei Entscheidungen, die erklärungsbedürftig sind:

**Preis relativ, nicht absolut.** Ein Stundensatz von 32 € ist in München
unauffällig und in Leipzig teuer. Normiert wird deshalb gegen die Spanne der
geeigneten Betriebe dieser Anfrage, nicht gegen einen bundesweiten Festwert.

**Erfahrung logarithmisch.** Der Sprung von 5 auf 40 Bewertungen sagt mehr über
die Belastbarkeit der Bewertung aus als der von 120 auf 155. Die Decke liegt bei
160, weil 159 die höchste Bewertungsanzahl der Erhebung ist — eine höhere Decke
hiesse, dass kein Betrieb im Netz die Skala je ausschöpft.

**Kapazitätsreserve mit Optimum, nicht monoton.** Ein Betrieb, der genau sechs
Kräfte stellen kann, hat bei sechs angefragten keinen Puffer für einen Ausfall.
Ein Betrieb mit 60 Kräften ist deswegen aber nicht zehnmal besser als einer mit
zwölf. Das Optimum liegt bei doppelter Kapazität, darüber bringt Größe nichts
mehr.

## Nachvollziehbarkeit

Jedes Ergebnis trägt seine Begründung:

- `eligible[i].score` — Gesamtwert, 0…1
- `eligible[i].teil` — die fünf Einzelwerte, jeder 0…1
- `eligible[i].gruende` — die zwei stärksten Argumente als Text, für das Interface
- `rejected[i].grund` — der Ausschlussgrund, im Klartext mit Zahlen
- `stats.ausschluesse` — Ausschlussgründe gezählt, für den Trichter

Die Demo zeigt das offen: den Trichter über den Angeboten, die Ausschlussliste auf
Klick. Ein Betrieb, der wissen will, warum er eine Anfrage nicht bekommen hat,
bekommt eine Antwort. Das ist bei einem Marktplatz, der Vertrauen verkauft, keine
Zusatzfunktion.

## Aufruf

```js
const ergebnis = KORAMatch.match(
  { anlass: "Event Security", ort: "Berlin", anzahl: 6, stunden: 8,
    anf: "Sachkunde § 34a erforderlich" },
  window.KORA_PROVIDERS.anbieter
);

ergebnis.stats
// { pool: 121, in_region: 10, geeignet: 3, eingeladen: 3,
//   ausschluesse: { "andere Region": 111,
//                   "Leistung nicht im Portfolio": 3,
//                   "Prüfkriterium verfehlt": 2,
//                   "Sachkunde § 34a nicht im Bestand": 1,
//                   "Kapazität zu klein": 1 } }
```

Läuft synchron. 121 Betriebe sind kein Grund für einen Webworker.

## Geprüfte Invarianten

Über alle 624 Kombinationen aus 13 Städten × 4 Anlässen × 4 Personalstärken
× 3 Anforderungen:

- `eligible` und `rejected` sind eine vollständige, disjunkte Partition des Pools
- `eligible` ist absteigend nach Score sortiert
- jeder Score liegt in 0…1
- kein Betrieb in `eligible` verletzt ein hartes Kriterium
- 13 von 13 Städten liefern bei einer Standardanfrage mindestens drei geeignete
  Betriebe
- 15 der 624 Kombinationen (2 %) haben keinen Treffer, überwiegend hohe
  Personalstärken in Verbindung mit Sachkunde § 34a

Der leere Fall ist im Interface abgefangen. Produktiv wäre die richtige Antwort
darauf, den Radius zu erweitern, statt eine leere Liste zu zeigen.

## Was fehlt

- **Verfügbarkeit am Datum.** Aktuell wird Kapazität geprüft, nicht der Kalender.
  Ein Betrieb mit 20 Kräften, von denen am Freitag 18 im Einsatz sind, gilt als
  geeignet.
- **Entfernung statt Stadtgleichheit.** `stadt !== ort` schließt einen Betrieb
  20 km hinter der Stadtgrenze aus und lässt einen 40 km entfernten im selben
  Stadtgebiet zu. Richtig wäre ein Radius über Koordinaten.
- **Rückkopplung.** Wer Angebote abgibt und Aufträge erhält, sollte steigen; wer
  Anfragen ignoriert, sinken. Ohne diese Schleife bleibt die Rangfolge eine
  Momentaufnahme aus Fremddaten.
- **Preisspanne pro Region.** Die Normierung nutzt die Spanne der Treffer. Bei
  drei geeigneten Betrieben ist das eine dünne Basis.
