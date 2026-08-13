#!/usr/bin/env python3
"""
Erzeugt die veröffentlichbaren Datensätze unter data/.

Zwei Quellen, zwei Vertrauensgrade:

  1. Die Lead-Liste (155 Betriebe, Google Places, Abruf 13.08.2026) liegt NICHT
     im Repository. Sie enthält Firmennamen, Anschriften und Direktnummern
     realer Unternehmen — personenbezogene Daten, deren Veröffentlichung weder
     durch die DSGVO noch durch die Google-Nutzungsbedingungen gedeckt ist.
     Aus ihr wird nur Aggregat abgeleitet: Betriebe pro Stadt, Bewertungslage,
     Kategorieverteilung. Kein Datensatz lässt sich einem Unternehmen zuordnen.

  2. Der Anbieter-Pool für die Demo ist synthetisch. Namen sind Platzhalter,
     Bewertungen und Betriebsgrößen werden aus der echten Verteilung gezogen
     (fester Seed, also reproduzierbar). Die Marktform ist echt, die einzelne
     Zeile ist es nicht.

Aufruf:

    python3 scripts/build-data.py                          # nur Aggregat + Pool aus data/market.json
    python3 scripts/build-data.py --leads /pfad/KORA-Leads.xlsx   # Aggregat neu aus der Rohliste

Schreibt:
    data/market.json          Aggregierte Marktdaten (echt)
    data/providers.json       Anbieter-Pool für die Demo (synthetisch)
    data/unit-economics.csv   36-Monats-Projektion des Abo-Modells
"""

import argparse
import csv
import json
import random
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# ── Belegte Marktzahlen ───────────────────────────────────────────────────────
# Quellen siehe docs/MARKET.md
MARKET_FACTS = {
    "betriebe_wz_801": 5330,          # Destatis, WZ 80.1, Stand Sept. 2023
    "taetige_personen": 232303,       # Destatis, Stand Sept. 2023
    "branchenumsatz_2024_eur": 14_020_000_000,   # BDSW
    "prognose_2025_eur": 14_750_000_000,         # BDSW
    "top25_anteil": 0.40,             # Lünendonk-Liste 2026, ohne Geld-/Wertlogistik
    "top25_umsatz_eur": 5_630_000_000,
}

# ── Abo-Modell: Annahmen (identisch zu business/KORA-Abomodell.xlsx) ──────────
ASSUMPTIONS = {
    "abopreis_monat_eur": 99,
    "adressierbarer_anteil": 0.45,
    "top25_anzahl": 25,
    "neukunden_monat_1": 5,
    "wachstum_monatlich": 0.15,
    "neukunden_obergrenze": 60,
    "churn_monatlich": 0.04,
    "cac_eur": 250,
    "fixkosten_monat_eur": 8000,
}


# ── 1. Aggregat aus der Rohliste ──────────────────────────────────────────────
def aggregate_from_leads(xlsx_path: Path) -> dict:
    """Liest die Lead-Liste und gibt ausschliesslich Aggregat zurück."""
    import openpyxl  # nur hier nötig

    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    rows = [r for r in wb["Leads"].iter_rows(min_row=2, values_only=True) if r[1]]

    def tally(idx):
        out = {}
        for r in rows:
            out[r[idx]] = out.get(r[idx], 0) + 1
        return dict(sorted(out.items(), key=lambda kv: -kv[1]))

    anbieter = [r for r in rows if r[3] == "Anbieter"]
    ratings = [r[7] for r in anbieter if isinstance(r[7], (int, float))]
    reviews = [r[8] for r in anbieter if isinstance(r[8], (int, float))]

    # Bewertungen pro Stadt nur als Kennzahl, nicht als Einzelwert
    per_city = {}
    for r in anbieter:
        c = per_city.setdefault(r[4], {"anbieter": 0, "_r": [], "_n": []})
        c["anbieter"] += 1
        if isinstance(r[7], (int, float)):
            c["_r"].append(r[7])
        if isinstance(r[8], (int, float)):
            c["_n"].append(r[8])

    staedte = {}
    for city, c in sorted(per_city.items(), key=lambda kv: -kv[1]["anbieter"]):
        staedte[city] = {
            "anbieter": c["anbieter"],
            "bewertung_mittel": round(statistics.fmean(c["_r"]), 2) if c["_r"] else None,
            "bewertungen_median": int(statistics.median(c["_n"])) if c["_n"] else None,
        }

    # Häufigkeitstabelle der Bewertungen, auf 0,1 gerundet. Eine reine
    # Verteilung ohne weitere Merkmale — daraus lässt sich kein Betrieb
    # zuordnen, weil die Verknüpfung mit der Stadt bewusst nicht veröffentlicht
    # wird. Der Anbieter-Pool zieht daraus, statt eine Normalverteilung zu
    # unterstellen: die echte Lage ist linksschief (Median 4,9 über Mittel 4,65),
    # das bekommt eine Glockenkurve nicht hin.
    hist = {}
    for x in ratings:
        k = f"{round(x, 1):.1f}"
        hist[k] = hist.get(k, 0) + 1
    histogramm = dict(sorted(hist.items(), key=lambda kv: float(kv[0])))

    # Dezile der Bewertungsanzahl, ebenfalls als Verteilung ohne Zuordnung.
    srt = sorted(reviews)
    dezile = [int(srt[min(len(srt) - 1, round(q / 10 * (len(srt) - 1)))]) for q in range(11)]

    return {
        "_hinweis": (
            "Aggregat aus einer Erhebung von 155 Betrieben (Google Places, "
            "Abruf 13.08.2026). Die Rohliste mit Firmennamen und Rufnummern ist "
            "aus Datenschutzgründen nicht Teil dieses Repositories."
        ),
        "erhebung": {
            "betriebe_erhoben": len(rows),
            "abrufdatum": "2026-08-13",
            "quelle": "Google Places",
            "staedte": len(per_city),
        },
        "seiten": tally(3),
        "kategorien": tally(2),
        "anbieter_bewertung": {
            "n": len(ratings),
            "mittel": round(statistics.fmean(ratings), 2),
            "median": statistics.median(ratings),
            "min": min(ratings),
            "max": max(ratings),
            "anteil_ab_45": round(sum(1 for x in ratings if x >= 4.5) / len(ratings), 3),
            "histogramm": histogramm,
        },
        "anbieter_bewertungsanzahl": {
            "median": int(statistics.median(reviews)),
            "mittel": int(statistics.fmean(reviews)),
            "max": int(max(reviews)),
            "anteil_unter_60": round(sum(1 for x in reviews if x < 60) / len(reviews), 3),
            "dezile": dezile,
        },
        "staedte": staedte,
        "markt": MARKET_FACTS,
    }


# ── 2. Synthetischer Anbieter-Pool für die Demo ───────────────────────────────
LEISTUNGEN = ["Event Security", "Objektschutz", "Baustellenbewachung", "Empfangsdienst"]

# Platzhalternamen. Bewusst generisch, damit sie keinem realen Betrieb ähneln.
STAMM = [
    "Aegis", "Nordwacht", "Castellum", "Vigil", "Turmfalke", "Silberpfeil",
    "Kastell", "Wachtmeister", "Orion", "Bastion", "Grenzstein", "Lupus",
    "Palisade", "Zenit", "Ankerpunkt", "Falkenauge", "Rondell", "Sentinel",
    "Steinwacht", "Argus", "Kompass", "Wehrturm", "Nordlicht", "Solid",
    "Perimeter", "Schildwache", "Meridian", "Zugbrücke", "Ronde", "Vertex",
]
RECHTSFORM = ["GmbH", "Sicherheitsdienst GmbH", "Security GmbH", "Wach- und Sicherheitsdienst", "Security Service GmbH"]


def _ziehe_bewertung(rng: random.Random, histogramm: dict) -> float:
    """Zieht eine Bewertung aus der Häufigkeitstabelle der Erhebung."""
    werte = [float(k) for k in histogramm]
    gewichte = list(histogramm.values())
    return rng.choices(werte, weights=gewichte, k=1)[0]


def _ziehe_anzahl(rng: random.Random, dezile: list) -> int:
    """Zieht eine Bewertungsanzahl aus den Dezilen, linear interpoliert.

    Umkehrung der empirischen Verteilungsfunktion. Reproduziert Median und
    rechten Rand der Erhebung, ohne eine Verteilungsfamilie zu unterstellen —
    eine Lognormalverteilung lag beim Median richtig und beim Maximum um den
    Faktor neun daneben.
    """
    u = rng.random() * 10
    i = min(9, int(u))
    lo, hi = dezile[i], dezile[i + 1]
    return max(3, int(round(lo + (hi - lo) * (u - i))))


def build_providers(market: dict, seed: int = 20260813) -> dict:
    """Baut einen Pool, dessen Verteilung der Erhebung entspricht."""
    rng = random.Random(seed)
    b = market["anbieter_bewertung"]
    dezile = market["anbieter_bewertungsanzahl"]["dezile"]
    providers = []
    pid = 0

    for city, stats in market["staedte"].items():
        for _ in range(stats["anbieter"]):
            pid += 1
            rating = round(_ziehe_bewertung(rng, b["histogramm"]), 1)
            reviews = _ziehe_anzahl(rng, dezile)
            # Kleinbetriebe können weniger Kräfte stellen
            max_kraefte = min(60, max(3, int(rng.lognormvariate(2.5, 0.7))))
            # Sachkunde § 34a hat nicht jeder Betrieb im Bestand
            sachkunde = rng.random() < 0.62
            leistungen = sorted(rng.sample(LEISTUNGEN, rng.randint(2, 4)))

            providers.append({
                "id": f"P{pid:03d}",
                "name": f"{rng.choice(STAMM)} {rng.choice(RECHTSFORM)}",
                "stadt": city,
                "bewertung": rating,
                "bewertungen": reviews,
                "leistungen": leistungen,
                "max_kraefte": max_kraefte,
                "sachkunde_34a": sachkunde,
                "einsatzleitung": rng.random() < 0.55,
                # Stundensatz pro Kraft, netto. Marktüblich 26–44 €.
                "satz_eur_h": round(rng.uniform(26, 44), 2),
                # Wie schnell der Betrieb typischerweise antwortet
                "reaktion_min": rng.choice([4, 7, 11, 18, 25, 40, 55, 90]),
                "geprueft": rating >= 4.3,
            })

    # Namen eindeutig machen
    seen = {}
    for p in providers:
        n = p["name"]
        seen[n] = seen.get(n, 0) + 1
        if seen[n] > 1:
            p["name"] = f"{n} {p['stadt']}"

    return {
        "_hinweis": (
            "SYNTHETISCH. Firmennamen sind Platzhalter und bezeichnen keinen "
            "realen Betrieb. Städteverteilung und Bewertungslage sind aus der "
            "echten Erhebung gezogen (data/market.json), die einzelne Zeile ist "
            "erzeugt. Fester Seed, damit die Demo reproduzierbar bleibt."
        ),
        "seed": seed,
        "anzahl": len(providers),
        "leistungen": LEISTUNGEN,
        "anbieter": providers,
    }


# ── 3. Abo-Modell nachrechnen ─────────────────────────────────────────────────
def unit_economics(a: dict = ASSUMPTIONS, monate: int = 36) -> list[dict]:
    """Rechnet die Projektion aus business/KORA-Abomodell.xlsx in Python nach."""
    zielgruppe = round((MARKET_FACTS["betriebe_wz_801"] - a["top25_anzahl"]) * a["adressierbarer_anteil"])
    rows, aktiv, db = [], 0, 0.0

    for m in range(1, monate + 1):
        neu = min(a["neukunden_obergrenze"], round(a["neukunden_monat_1"] * (1 + a["wachstum_monatlich"]) ** (m - 1)))
        kuend = round(aktiv * a["churn_monatlich"])
        aktiv = aktiv + neu - kuend
        mrr = aktiv * a["abopreis_monat_eur"]
        cac = neu * a["cac_eur"]
        db += mrr - cac
        rows.append({
            "monat": m,
            "neukunden": neu,
            "kuendigungen": kuend,
            "aktive_abos": aktiv,
            "mrr_eur": mrr,
            "arr_eur": mrr * 12,
            "akquisekosten_eur": cac,
            "deckungsbeitrag_kumuliert_eur": round(db),
            "marktdurchdringung": round(aktiv / zielgruppe, 5),
        })
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--leads", type=Path, help="Pfad zur KORA-Leads.xlsx (nicht im Repo)")
    args = ap.parse_args()

    DATA.mkdir(exist_ok=True)
    market_path = DATA / "market.json"

    if args.leads:
        if not args.leads.exists():
            ap.error(f"nicht gefunden: {args.leads}")
        market = aggregate_from_leads(args.leads)
        market_path.write_text(json.dumps(market, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"data/market.json      neu aus {args.leads.name} ({market['erhebung']['betriebe_erhoben']} Betriebe)")
    else:
        if not market_path.exists():
            ap.error("data/market.json fehlt — einmalig mit --leads /pfad/KORA-Leads.xlsx erzeugen")
        market = json.loads(market_path.read_text(encoding="utf-8"))
        print("data/market.json      unverändert übernommen")

    providers = build_providers(market)
    (DATA / "providers.json").write_text(json.dumps(providers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"data/providers.json   {providers['anzahl']} Anbieter, Seed {providers['seed']}")

    # Dieselben Daten als JS-Datei. Ein fetch() auf die .json scheitert, wenn die
    # Demo über file:// geöffnet wird — ein <script src> nicht. Damit läuft die
    # App per Doppelklick und über den Webserver gleich.
    (DATA / "providers.js").write_text(
        "/* Erzeugt von scripts/build-data.py — nicht von Hand ändern. */\n"
        "window.KORA_PROVIDERS = "
        + json.dumps(providers, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    print("data/providers.js     dieselben Daten für file://-Betrieb")

    (DATA / "market.js").write_text(
        "/* Erzeugt von scripts/build-data.py — nicht von Hand ändern. */\n"
        "window.KORA_MARKET = " + json.dumps(market, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print("data/market.js        Marktdaten für die Übersichtsseite")

    rows = unit_economics()
    with (DATA / "unit-economics.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    (DATA / "unit-economics.js").write_text(
        "/* Erzeugt von scripts/build-data.py — nicht von Hand ändern. */\n"
        "window.KORA_ECONOMICS = "
        + json.dumps({"annahmen": ASSUMPTIONS, "projektion": rows}, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    m12, m24, m36 = rows[11], rows[23], rows[35]
    print(f"data/unit-economics.csv  M12 {m12['aktive_abos']} Abos / {m12['arr_eur']:,} € ARR"
          f" · M24 {m24['aktive_abos']} / {m24['arr_eur']:,} €"
          f" · M36 {m36['aktive_abos']} / {m36['arr_eur']:,} €".replace(",", "."))


if __name__ == "__main__":
    main()
