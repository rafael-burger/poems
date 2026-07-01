# poems

Personal poetry collection and website generator.

## Directory structure

```
poems/
  src/          poem source files (.txt), named YYYY.MM.DD_N_title.txt
  docs/         generated website output (HTML, CSS)
  tools/        Python CLI package (poem_tool) and supporting files
```

## Tools

All Python source lives in `tools/poem_tool/`, installed as a package (see Setup below).

### `poem_tool/cli.py`

Entrypoint. Parses the command and arguments from the command line, looks up
the matching `Command` object, and dispatches to the handler. Prints output or
an error if the command is unrecognized. Exposes `main()`, which is wired up
as the `poem` console script.

### `poem_tool/commands.py`

Defines the `Command` class and the `CommandParser`. `CommandParser.COMMANDS`
is the registry of all supported commands, each mapping one or more keyword
strings to a handler callback and an argument-count range. Also defines
`doCommand`, which validates arg count before calling the handler.

Available commands (and their short aliases):

| command         | alias    | description                                      |
|-----------------|----------|--------------------------------------------------|
| `list-configs`  | `lscfg`  | List saved configurations                        |
| `add-config`    | `addcfg` | Create a new named configuration                 |
| `remove-config` | `rmcfg`  | Delete a configuration                           |
| `list-poems`    | `lsp`    | List poems in a configuration                    |
| `add-poem`      | `addp`   | Add a poem file to a configuration               |
| `remove-poem`   | `rmp`    | Remove a poem from a configuration               |
| `generate-html` | `genhtml`| Generate HTML pages from a configuration         |

Pass `--help` after any command for its detailed help text.

### `poem_tool/handler.py`

Contains the `Handler` class with one static method per command. Handlers
instantiate the data-layer objects (`ConfigDatabase`, `PoemConfig`, etc.) and
coordinate the actual work. `_resolve_config` is a shared helper that picks a
config by name from args, or falls back to the first available config.

### `poem_tool/website_config.py`

Data layer. Defines:

- **`ConfigDatabase`** — reads and writes `tools/config/_base.cfg`, a CSV index
  of named configurations. Each configuration maps to its own `.cfg` file.
- **`ConfigEntry`** — a single row in the config database (name + file path).
- **`PoemConfig`** — reads and writes a named configuration's `.cfg` file, which
  is a CSV list of poems (uuid, date, title, filepath).
- **`PoemEntry`** — one poem record. Parsed from a filename matching
  `YYYY.MM.DD_N_title.txt`; assigned a UUID on first add. `filepath` is stored
  as an absolute path (resolved at add-time), independent of cwd.
- **`HtmlPage`** — renders a single poem's HTML page (a thin shell that fetches
  the `.txt` source via JS).
- **`generate_index`** — renders an `index.html` table of contents for a set of
  `HtmlPage` objects.

### `poem_tool/paths.py`

Resolves `config/` and `command-help/` relative to `tools/` (the installed
package's location on disk), not the caller's current directory. This is what
lets `poem` be run from anywhere.

### `make-poem-pages.py`

Older standalone script (predates the CLI). Iterates over every `.txt` file in
`src/` and generates a corresponding HTML page, without any configuration layer.
Superseded by `generate-html` but kept for reference.

## Usage

### Setup

`poem_tool` is an installable Python package. From the `tools/` directory,
install it (editable, so code changes take effect immediately):

```bash
pip install -e ./tools
# or, from inside tools/:
pip install -e .
```

This registers a `poem` console script on PATH (inside whatever Python
environment/venv you installed it into). Call it as:

```bash
poem <command> [args]
```

It works from any directory — `poem_tool` resolves its `config/` and
`command-help/` data relative to its own location in the repo, not your
current directory.

### Help

```bash
poem                             # show general help (list of commands)
poem --help                      # same
poem add-poem --help             # show help for a specific command
```

### Examples

Run from the repo root (or anywhere — paths below assume repo root for
readability):

```bash
poem add-config website          # create a config named "website"
poem lscfg                       # list configs

poem addp website src/2026.01.30_0_curved-lines.txt
poem lsp website                 # list poems in "website"

poem generate-html website -d docs/poem-pages
poem rmp website curved-lines    # remove by title slug or UUID
```

`--dest-dir` for `generate-html` resolves relative to wherever you invoke
`poem` from, like any normal CLI argument.
