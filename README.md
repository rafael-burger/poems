# poems

Personal poetry collection and website generator.

## Directory structure

```
poems/
  src/          poem source files (.txt), named YYYY.MM.DD_N_title.txt
  docs/         generated website output (HTML, CSS)
  tools/        Python CLI and supporting modules
  poem          bash entrypoint — see Usage below
```

## Tools

All Python source lives in `tools/`.

### `poem_tool.py`

Entrypoint. Parses the command and arguments from the command line, looks up
the matching `Command` object, and dispatches to the handler. Prints output or
an error if the command is unrecognized.

### `poem_tool_commands.py`

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

### `poem_tool_handler.py`

Contains the `Handler` class with one static method per command. Handlers
instantiate the data-layer objects (`ConfigDatabase`, `PoemConfig`, etc.) and
coordinate the actual work. `_resolve_config` is a shared helper that picks a
config by name from args, or falls back to the first available config.

### `website_config.py`

Data layer. Defines:

- **`ConfigDatabase`** — reads and writes `tools/config/_base.cfg`, a CSV index
  of named configurations. Each configuration maps to its own `.cfg` file.
- **`ConfigEntry`** — a single row in the config database (name + file path).
- **`PoemConfig`** — reads and writes a named configuration's `.cfg` file, which
  is a CSV list of poems (uuid, date, title, filepath).
- **`PoemEntry`** — one poem record. Parsed from a filename matching
  `YYYY.MM.DD_N_title.txt`; assigned a UUID on first add.
- **`HtmlPage`** — renders a single poem's HTML page (a thin shell that fetches
  the `.txt` source via JS).
- **`generate_index`** — renders an `index.html` table of contents for a set of
  `HtmlPage` objects.

### `make-poem-pages.py`

Older standalone script (predates the CLI). Iterates over every `.txt` file in
`src/` and generates a corresponding HTML page, without any configuration layer.
Superseded by `generate-html` but kept for reference.

## Usage

### Setup

The `poem` script at the repo root is a bash entrypoint. To use it from
anywhere, add the repo root to your PATH, or symlink it:

```bash
# option A: add to PATH (put this in ~/.bashrc or ~/.bash_profile)
export PATH="/path/to/poems:$PATH"

# option B: symlink into an existing PATH directory
ln -s /path/to/poems/poem /usr/local/bin/poem
```

Then call it as:

```bash
poem <command> [args]
```

### Without setup

From the `tools/` directory:

```bash
python3 poem_tool.py <command> [args]
```

### Help

```bash
poem                             # show general help (list of commands)
poem --help                      # same
poem add-poem --help             # show help for a specific command
```

### Examples

```bash
poem add-config website          # create a config named "website"
poem lscfg                       # list configs

poem addp website ../src/2026.01.30_0_curved-lines.txt
poem lsp website                 # list poems in "website"

poem generate-html website -d ../docs/poem-pages
poem rmp website curved-lines    # remove by title slug or UUID
```

> **Note:** when using `generate-html`, pass an absolute path or a path
> relative to `tools/` for `--dest-dir`, since the tool always runs from the
> `tools/` directory.
