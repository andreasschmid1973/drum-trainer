# Drum-Trainer

Übe-App für Schlagzeug in der Coverband: Song wählen, MP3 läuft, das Drum-Chart scrollt mit, ein Click folgt exakt dem Takt der Aufnahme, und eine Stimme sagt die Teile (Verse, Chorus …) einen Takt vorher an.

**App öffnen:** https://andreasschmid1973.github.io/drum-trainer/  
Auf dem iPad in Safari öffnen → Teilen → „Zum Home-Bildschirm“. Danach läuft die App auch offline.

## Bedienung (kurz)
- **Charts & MP3s laden:** einmal alle PDFs und MP3s auswählen (Dateinamen mit Setlist-Nummer vorne, z. B. `03 Paranoid.mp3`). Sie bleiben auf dem Gerät gespeichert, nichts wird hochgeladen.
- **Play** zählt ein (1–4 Takte, pro Song einstellbar).
- **Ins Chart tippen** springt an den Anfang dieses Takts; Play zählt ein und spielt ab dort.
- **Zurück-Taste:** erster Druck an den Songanfang, zweiter Druck vorheriger Song.
- **Click:** Ton, Kuhglocke oder Claves; bei 12/8-Songs wählbar als 12/8, 6/8, 6/4 oder nur punktierte Viertel.
- **Ansagen** (Stimme „Karen“), **Positionsstrich**, **Mitscrollen**, **Lautheit angleichen**, Regler für Song, Click, Stimme und **Ausgang** (bis +12 dB mit Begrenzer).
- **JSON speichern / Importieren:** alle Einstellungen sichern und wiederherstellen.

## Inhalt des Repositorys
| Ordner / Datei | Inhalt |
|---|---|
| `index.html`, `sw.js`, `manifest.webmanifest`, `lib/`, `fonts/`, Icons | die veröffentlichte Offline-Web-App (GitHub Pages) |
| `source/drum-trainer.html` | Quelltext der App (eine Datei) |
| `source/standalone/` | einzeln lauffähige HTML-Version |
| `source/parts/` | Bausteine: Chart-Daten & Taktanalyse, Taktkarten-Abgleich, Chart-Layouts & Teile |
| `ansagen/` | Ansagen mit der Stimme „Karen“ (macOS `say`), in die App eingebaut |
| `analysis/audio/` | Python/Node-Skripte der Taktanalyse (Drum-Transienten, madmom, Abgleich mit den Charts) |
| `analysis/charts/` | Skripte zur Takterkennung in den Chart-PDFs |
| `analysis/data/` | Ergebnisse: Taktkarten aller Songs, Taktarten/Tempi aus den Charts, Chart-Layouts, Teile |

MP3s und Drum-Charts sind bewusst **nicht** enthalten (Urheberrecht); sie liegen nur lokal bzw. in iCloud.

## Versionen
- **1.8** Regler „Ausgang“ (+0…+12 dB) mit Begrenzer
- **1.7** Ansagen als eingebaute Aufnahmen – iOS regelt Song und Click nicht mehr herunter
- **1.6** Offline-Web-App; Anzeige-Korrektur
- **1.5** Jump-Intro um eine Achtel korrigiert; Versionsanzeige oben links
- **1.4** Takt per Tippen ins Chart; Zurück-Taste zum Songanfang
- **1.3** Neue Taktkarten (War Pigs, Wanted Dead or Alive, Silent Lucidity, Jump), Lautheitsausgleich, 12/8-Click-Modi
- **1.2** Pausen, Wiederholungen, 12/8-Click, Jump-Intro
- **1.1** Einzählen, Positionsstrich, Ansagen, Click-Sounds, JSON-Speichern
- **1.0** erste Version
