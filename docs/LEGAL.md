# Recht

Stand der rechtlichen Unterlagen und was vor einem Livegang zu tun ist.

**Die Vorlagen in `landing/legal/` ersetzen keine Rechtsberatung.** Sie sind so
gebaut, dass die offenen Stellen sichtbar sind, nicht so, dass sie fertig
aussehen.

## Platzhalter ersetzen

Alle Platzhalter sind im Browser gelb hinterlegt (`class="ph"`). 17 im Impressum,
17 in der Datenschutzerklärung.

**`landing/legal/impressum.html`** — Firmenname und Rechtsform, Anschrift,
Geschäftsführung, Kontakt (E-Mail und Telefon), Registergericht und
Registernummer, USt-IdNr., inhaltlich Verantwortlicher nach § 18 Abs. 2 MStV,
Erlaubnis nach § 34a GewO mit erteilender Behörde, Berufshaftpflicht mit
Versicherer und räumlichem Geltungsbereich.

**`landing/legal/datenschutz.html`** — Stand (Monat/Jahr), Verantwortlicher,
Datenschutzbeauftragter *oder Punkt streichen*, im Formular tatsächlich
abgefragte Felder, Speicherdauer, Wartelisten-Tool mit Anbieter und Sitz,
Drittlandgarantien nach Art. 46 DSGVO *falls zutreffend*, Hoster, Löschfrist der
Server-Logs, zuständige Landesdatenschutzbehörde mit Anschrift.

In **Abschnitt 4 · Cookies und Reichweitenmessung** stehen drei Varianten zur
Auswahl — A ohne Cookies und ohne Analyse, B mit cookiefreier Analyse (etwa
Plausible oder Matomo), C mit Google Analytics oder Meta-Pixel. **Nur C erfordert
ein Consent-Banner** nach § 25 Abs. 1 TDDDG. Zwei Varianten löschen, nicht alle
drei stehen lassen.

Suchen mit:

```bash
grep -c 'class="ph"' landing/legal/*.html   # muss am Ende 0 ergeben
```

## Erledigt

**Schriften werden lokal eingebunden.** Ein Request an `fonts.googleapis.com`
überträgt die IP-Adresse jedes Besuchers an Google. Dafür wäre eine Einwilligung
nötig; das LG München I hat 2022 einen Schadensersatz zugesprochen, danach folgte
eine Abmahnwelle. Abschnitt 5 der Datenschutzerklärung sagt ausdrücklich zu, dass
es nicht passiert.

Im Ausgangsmaterial stimmte das an vier Stellen nicht: `app/index.html`,
`brand/styleguide.html` und **beide Rechtstexte selbst** luden Archivo über
Google — die Datenschutzerklärung widersprach also ihrem eigenen Abschnitt 5.
Alle vier laden jetzt Inter aus `brand/fonts/` (SIL Open Font License).

Nachprüfen:

```bash
grep -rn "fonts.googleapis\|fonts.gstatic" --include="*.html" --include="*.css" .
# nur Treffer in Kommentaren und im Warnhinweis der Datenschutzerklärung
```

**Einwilligung im Wartelisten-Formular.** Aktive Checkbox, nicht vorausgewählt,
mit Link auf die Datenschutzerklärung. Einwilligungstext und Zeitstempel gehen mit
in die Nutzlast — ohne diesen Nachweis ist die Einwilligung nach Art. 7 Abs. 1
DSGVO nicht belegbar.

**Rollenwahl als Pflichtfeld.** „Ich bin: Auftraggeber / Anbieter". Kein
rechtlicher Punkt, sondern die Voraussetzung dafür, zwei getrennte Kampagnen
auswerten zu können.

## Offen

**Double-Opt-In fehlt.** Die Warteliste schreibt derzeit nur in `localStorage`,
`WAITLIST_ENDPOINT` in `landing/index.html` ist leer. Sobald ein Endpunkt
gesetzt ist, gehört ein Bestätigungslink dazu — sonst ist bei einer fremd
eingetragenen Adresse nicht nachweisbar, wer eingewilligt hat.

**Verträge, sobald KORA wirklich vermittelt.** AGB, Anbieter-Nutzungsbedingungen
und eine erweiterte Datenschutzerklärung, die die Verarbeitung zwischen den
Marktseiten abdeckt. Dazu die Frage, ob KORA Vermittler oder Vertragspartner ist —
davon hängt die Haftung ab. Das gehört über einen Anwalt für IT-Recht.

**Auftragsverarbeitungsverträge** nach Art. 28 DSGVO mit Hoster und
Wartelisten-Tool.

**„Geprüft" ist derzeit eine Bewertungsschwelle.** Ein Marktplatz, der mit
geprüften Anbietern wirbt, muss die Prüfung belegen können, sonst ist die Aussage
irreführend nach § 5 UWG. Belastbar wäre der Abruf des Bewacherregisters nach
§ 11b GewO plus Sachkundenachweise und Betriebshaftpflicht. Bis dahin sollte im
Interface stehen, worauf sich das Wort stützt.

## Akquise

**Telefonwerbung** gegenüber Unternehmen ist nach § 7 Abs. 2 Nr. 2 UWG nur bei
mutmaßlicher Einwilligung zulässig. Bei einem Sicherheitsdienst, dem eine
Auftragsvermittlung angeboten wird, ist die Vermutung tragfähig.

**Kalte Werbe-E-Mails an Firmen sind ohne Einwilligung unzulässig.** Auch nicht an
`info@`-Adressen, auch nicht mit Abmeldelink. Häufigster und teuerster Fehler in
dieser Phase.

**Die Lead-Liste gehört nicht ins Repository.** Firmennamen mit Direktnummern und
einer selbst gesetzten Vertriebspriorität — Begründung in [DATA.md](DATA.md).
`.gitignore` fängt sie ab.
