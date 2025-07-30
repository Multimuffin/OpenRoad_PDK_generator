# PDK Generator

Dieses Projekt bietet ein modulares Python-Framework zur automatisierten Generierung und Konfiguration von PDK-Plattformen.

## Features
- Interaktive Auswahl der Technologie und des Metal-Stacks
- Automatische Erstellung von Verzeichnisstrukturen und Symlinks
- Flexible Auswahl und Einbindung von LIB-Dateien
- Konfigurationsdatei (`config.mk`) wird automatisch angepasst
- Erweiterbar und testbar durch modulare Struktur

## Installation
Python 3.10 und das Paket `click` werden benötigt.

```sh
python3.10 -m pip install --user click
```

## Nutzung
Starte die CLI aus dem Projektverzeichnis:

```sh
python3.10 -m pdk_generator.cli
```

Folge den interaktiven Auswahlmenüs für Technologie, Metal-Stack und LIB-Files.

## Struktur
- `pdk_generator/cli.py` – Einstiegspunkt (CLI)
- `pdk_generator/generator.py` – Hauptworkflow
- `pdk_generator/config_updater.py` – Konfigurationslogik
- `pdk_generator/dir_utils.py` – Verzeichnisfunktionen
- `pdk_generator/ui_utils.py` – User-Interaktion
- `pdk_generator/symlink_utils.py` – Symlink-Handling
- `tests/` – Unittests

## Entwicklung
Änderungen können wie gewohnt mit Git versioniert werden:

```sh
git add .
git commit -m "Beschreibung"
git push
```

## Lizenz
MIT
