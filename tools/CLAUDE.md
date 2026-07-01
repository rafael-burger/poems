# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Python CLI tool (`poem_tool` package, installed as the `poem` command) for managing a static poetry website. It handles poem registration, config management, and HTML generation.

## Running the tool

Install once (editable install, from the `tools/` directory):

```bash
pip install -e .
```

This registers a `poem` console script (via `pyproject.toml`'s `[project.scripts]`) that works from any directory — it no longer requires `cd`ing into `tools/`.

```bash
poem <command> [args]
poem --help
poem <command> --help
```

There is no build step or test suite.

## Commands

| Command (alias)              | Description                                      |
|------------------------------|--------------------------------------------------|
| `list-configs` (`lscfg`)     | List all saved configurations                    |
| `add-config` (`addcfg`)      | Add a new configuration                          |
| `remove-config` (`rmcfg`)    | Remove a configuration                           |
| `list-poems` (`lsp`)         | List poems in a configuration                    |
| `add-poem` (`addp`)          | Register a poem file into a configuration        |
| `remove-poem` (`rmp`)        | Remove a poem from a configuration               |
| `generate-html` (`genhtml`)  | Generate HTML pages + index for a configuration  |

## Poem filename format

Poem source files must match: `YYYY.MM.DD_N_title-with-dashes.txt`

Example: `2026.06.28_0_torches-angels.txt`

The date, sequence number, and hyphenated title are all parsed from the filename automatically when adding a poem.

## Architecture

The CLI lives in the `poem_tool/` package (installed via `pyproject.toml`):

**`poem_tool/cli.py`** — Entrypoint (`main()`, wired up as the `poem` console script). Parses command/args/help flag and dispatches via `doCommand`.

**`poem_tool/commands.py`** — Defines `Command` objects (keywords, nargs, callback) and `CommandParser` (registry + arg parsing). Help text is loaded from `command-help/<command-name>.txt` (resolved via `paths.COMMAND_HELP_DIR`) between `STARTHELP` / `ENDHELP` markers.

**`poem_tool/handler.py`** — `Handler` class contains one static method per command. Delegates all data access to `website_config.py` classes.

**`poem_tool/website_config.py`** — Data layer and HTML generation:
- `ConfigDatabase` — reads/writes `config/_base.cfg` (CSV: `name,filepath`) as the master list of configs
- `ConfigEntry` — represents one named config; its poems live in `config/<name>.cfg`
- `PoemEntry` — one poem record (UUID, date, title, filepath); persisted as CSV. `filepath` is stored as an absolute path, resolved at add-time
- `PoemConfig` — reads/writes a config's poem list; deduplicates by filepath
- `HtmlPage` — generates a single poem HTML page (fetches `.txt` via JS `fetch()`)
- `generate_index()` — generates `index.html` table of contents

**`poem_tool/paths.py`** — Resolves `config/` and `command-help/` relative to the installed package's location on disk (`tools/`), not the caller's cwd. This is what lets `poem` be invoked from any directory.

## HTML output structure

`generate-html` writes to `./output/` (or `--dest-dir`):
- `output/index.html` — table of contents linking to all poem pages
- `output/<date>_<n>_<title>.html` — individual poem page (loads text via `fetch('src/<filename>')`)
- `output/src/<filename>.txt` — copy of the source poem file

Each poem page loads its content from the `src/` subdirectory via JavaScript at runtime; the HTML pages themselves contain no poem text.

## Config storage

- `config/_base.cfg` — master list of named configurations (CSV: `name,./config/<name>.cfg`)
- `config/<name>.cfg` — poem list for that config (CSV: `uuid,date,title,filepath`)

The `site` config (pointing to `config/site.cfg`) is pre-created and is the default when no config name is specified.

## Legacy script

`make-poem-pages.py` is an older standalone script superseded by the current tool. It reads from a local `src/` directory and writes to `poem-pages/`. It is no longer the primary workflow.
