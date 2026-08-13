/* ═══════════════════════════════════════════════════════════════════════════
   KORA — Matching
   ═══════════════════════════════════════════════════════════════════════════

   Ordnet eine Anfrage den Anbietern im Pool zu. Zwei Stufen, bewusst getrennt:

   1. AUSSCHLUSS (harte Kriterien). Wer die Anforderung nicht erfüllen kann,
      wird nicht angefragt. Kein Score, keine Gewichtung — entweder oder.
      Das ist der Teil, der das Versprechen „geprüft" trägt: ein Betrieb ohne
      Sachkunde § 34a bekommt eine Anfrage, die Sachkunde verlangt, nie zu
      sehen.

   2. RANGFOLGE (weiche Kriterien). Unter den geeigneten Betrieben wird
      gewichtet sortiert. Preis wird innerhalb der geeigneten Menge normiert,
      nicht absolut — ein Stundensatz von 32 € ist in München anders zu lesen
      als in Leipzig.

   Jede Entscheidung ist nachvollziehbar: eligible[i].gruende erklärt den
   Score, rejected[i].grund den Ausschluss. Eine Blackbox wäre für einen
   Marktplatz, der Vertrauen verkauft, das falsche Werkzeug.

   Kein Framework, kein Build. Läuft auch über file://.
   ═══════════════════════════════════════════════════════════════════════════ */

(function (global) {
  "use strict";

  // Gewichte der Rangfolge. Summe 1.0.
  const GEWICHTE = {
    bewertung: 0.35,   // Wie gut ist der Betrieb bewertet
    erfahrung: 0.15,   // Wie belastbar ist diese Bewertung
    kapazitaet: 0.15,  // Reserve über dem Bedarf
    preis: 0.25,       // Günstiger ist besser, relativ zum Feld
    reaktion: 0.10,    // Wer schnell antwortet, besetzt schneller
  };

  const MIN_BEWERTUNG = 2.7;   // schlechteste Bewertung der Erhebung
  const PRUEF_SCHWELLE = 4.3;  // ab hier gilt ein Betrieb als geprüft
  const EINLADUNGEN = 3;       // so viele Betriebe werden angefragt

  // Obergrenze der Erfahrungsskala. 159 ist die höchste Bewertungsanzahl der
  // Erhebung auf der Anbieterseite — eine höhere Decke hiesse, dass kein
  // Betrieb im Netz die Skala je ausschöpft.
  const ERFAHRUNG_DECKE = 160;

  /** Was die Anforderung aus der Anfrage konkret verlangt. */
  function anforderungProfil(anf) {
    const s = String(anf || "");
    return {
      sachkunde: s.includes("Sachkunde"),
      einsatzleitung: s.includes("Einsatzleitung"),
    };
  }

  /**
   * Harte Kriterien. Gibt null zurück, wenn der Betrieb geeignet ist,
   * sonst den Ausschlussgrund als Text.
   */
  function ausschlussgrund(p, req) {
    const braucht = anforderungProfil(req.anf);

    if (p.stadt !== req.ort) return "andere Region";
    if (!p.leistungen.includes(req.anlass)) return `${req.anlass} nicht im Portfolio`;
    if (!p.geprueft) return `Prüfkriterium verfehlt (${p.bewertung.toFixed(1)} < ${PRUEF_SCHWELLE})`;
    if (p.max_kraefte < req.anzahl) return `Kapazität ${p.max_kraefte} < ${req.anzahl} Kräfte`;
    if (braucht.sachkunde && !p.sachkunde_34a) return "Sachkunde § 34a nicht im Bestand";
    if (braucht.einsatzleitung && !p.einsatzleitung) return "keine eigene Einsatzleitung";

    return null;
  }

  /** 0…1, linear zwischen lo und hi, ausserhalb geklemmt. */
  function norm(x, lo, hi) {
    if (hi === lo) return 1;
    return Math.min(1, Math.max(0, (x - lo) / (hi - lo)));
  }

  /**
   * Ordnet eine Anfrage dem Pool zu.
   *
   * @param {object} req    Anfrage: {anlass, ort, anzahl, stunden, anf}
   * @param {Array}  pool   Anbieter aus data/providers.js
   * @returns {{eligible:Array, rejected:Array, stats:object}}
   */
  function match(req, pool) {
    const geeignet = [];
    const rejected = [];

    for (const p of pool) {
      const grund = ausschlussgrund(p, req);
      if (grund) rejected.push({ anbieter: p, grund });
      else geeignet.push(p);
    }

    // Preis relativ zum Feld: erst die Spanne der geeigneten Betriebe bestimmen
    const saetze = geeignet.map((p) => p.satz_eur_h);
    const satzMin = saetze.length ? Math.min(...saetze) : 0;
    const satzMax = saetze.length ? Math.max(...saetze) : 0;

    const eligible = geeignet.map((p) => {
      const teil = {
        bewertung: norm(p.bewertung, MIN_BEWERTUNG, 5),
        // Bewertungsanzahl logarithmisch: der Sprung von 5 auf 40 sagt mehr
        // als der von 400 auf 435.
        erfahrung: norm(Math.log10(p.bewertungen + 1), 0, Math.log10(ERFAHRUNG_DECKE)),
        // Reserve über dem Bedarf, doppelte Kapazität gilt als Optimum.
        kapazitaet: norm(p.max_kraefte / req.anzahl, 1, 2),
        // Invertiert: der günstigste Satz im Feld bekommt 1.
        preis: 1 - norm(p.satz_eur_h, satzMin, satzMax),
        reaktion: 1 - norm(p.reaktion_min, 4, 90),
      };

      let score = 0;
      for (const k in GEWICHTE) score += GEWICHTE[k] * teil[k];

      return {
        ...p,
        score: Math.round(score * 1000) / 1000,
        teil,
        gruende: begruendung(p, teil, req),
        preis_eur: Math.round(p.satz_eur_h * req.anzahl * req.stunden),
      };
    });

    eligible.sort((a, b) => b.score - a.score);

    return {
      eligible,
      rejected,
      stats: {
        pool: pool.length,
        in_region: pool.filter((p) => p.stadt === req.ort).length,
        geeignet: eligible.length,
        eingeladen: Math.min(EINLADUNGEN, eligible.length),
        ausschluesse: zaehleGruende(rejected),
      },
    };
  }

  /** Die zwei stärksten Argumente für diesen Betrieb, als Text. */
  function begruendung(p, teil, req) {
    const kandidaten = [
      { k: "bewertung", t: `${p.bewertung.toFixed(1)} Sterne aus ${p.bewertungen} Bewertungen` },
      { k: "kapazitaet", t: `${p.max_kraefte} Kräfte verfügbar, ${req.anzahl} gebraucht` },
      { k: "preis", t: `${p.satz_eur_h.toFixed(2)} € pro Kraft und Stunde` },
      { k: "reaktion", t: `antwortet typischerweise in ${p.reaktion_min} Min.` },
      { k: "erfahrung", t: `${p.bewertungen} dokumentierte Einsätze` },
    ];
    return kandidaten
      .sort((a, b) => teil[b.k] - teil[a.k])
      .slice(0, 2)
      .map((c) => c.t);
  }

  function zaehleGruende(rejected) {
    const out = {};
    for (const r of rejected) {
      // "Kapazität 8 < 12 Kräfte" → "Kapazität zu klein", damit sich zählen lässt
      const key = r.grund
        .replace(/Kapazität \d+ < \d+ Kräfte/, "Kapazität zu klein")
        .replace(/Prüfkriterium verfehlt \([^)]*\)/, "Prüfkriterium verfehlt")
        .replace(/^.+ nicht im Portfolio$/, "Leistung nicht im Portfolio");
      out[key] = (out[key] || 0) + 1;
    }
    return Object.fromEntries(Object.entries(out).sort((a, b) => b[1] - a[1]));
  }

  global.KORAMatch = { match, ausschlussgrund, GEWICHTE, EINLADUNGEN, PRUEF_SCHWELLE };
})(window);
