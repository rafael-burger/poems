"""
website_config.py

Functions and classes associated with managing website configuration
"""

from pathlib import Path
import re
import os
import uuid as uuid_module


class ConfigEntry:
    NUM_FIELDS = 2
    def __init__(self, name: str):
        self.name = name
        self.file = f"{ConfigDatabase.BASE_DIR}/{name}.cfg"

    def getName(self):
        return self.name

    def getFile(self):
        return self.file

    def toString(self):
        return f"{self.name} --> {self.file}"

    def toCsv(self):
        return f"{self.name},{self.file}"

    def fromCsv(s: str):
        """
        Try to create a ConfigEntry from the input string.
        If success, return a ConfigEntry. Otherwise, return None
        """
        l = s.split(',')
        if len(l) == ConfigEntry.NUM_FIELDS:
            return ConfigEntry(l[0])
        else:
            return None


class PoemEntry:
    NUM_FIELDS = 4
    FILENAME_PATTERN = r"^(\d\d\d\d.\d\d.\d\d)_\d+_(.*)\.txt$"

    def __init__(self, uuid: str, date: str, title: str, filepath: str):
        self.uuid = uuid
        self.date = date
        self.title = title
        self.filepath = filepath

    def fromFile(filepath: str):
        """
        Static method. Validates filename against FILENAME_PATTERN, generates UUID.
        Raises ValueError on mismatch.
        """
        basename = Path(filepath).name
        match = re.search(PoemEntry.FILENAME_PATTERN, basename)
        if not match:
            raise ValueError(f"Filename '{basename}' does not match expected pattern")
        date = match.group(1)
        title = match.group(2)
        new_uuid = str(uuid_module.uuid4())
        return PoemEntry(new_uuid, date, title, filepath)

    def fromCsv(s: str):
        """
        Static method. Splits on ',' up to 4 parts.
        """
        parts = s.strip().split(',', 3)
        if len(parts) == PoemEntry.NUM_FIELDS:
            return PoemEntry(parts[0], parts[1], parts[2], parts[3])
        return None

    def toCsv(self):
        return f"{self.uuid},{self.date},{self.title},{self.filepath}\n"

    def toString(self):
        title_display = self.title.replace('-', ' ')
        return f"{self.date}  {title_display}  [{self.uuid}]  ({self.filepath})"


class PoemConfig:
    def __init__(self, config_entry: ConfigEntry):
        self.config_entry = config_entry

    def getPoems(self):
        """Return list of PoemEntry objects from the config file."""
        poems = []
        cfg_file = Path(self.config_entry.getFile())
        if not cfg_file.is_file():
            return poems
        with open(cfg_file, 'r') as f:
            for line in f.readlines():
                poem = PoemEntry.fromCsv(line)
                if poem is not None:
                    poems.append(poem)
        return poems

    def addPoem(self, poem: PoemEntry):
        """
        Add poem to config. Returns False if duplicate filepath exists, True otherwise.
        """
        existing = self.getPoems()
        for p in existing:
            if p.filepath == poem.filepath:
                return False
        with open(self.config_entry.getFile(), 'a') as f:
            f.write(poem.toCsv())
        return True

    def removePoem(self, identifier: str):
        """
        Remove poem matching uuid, title, filepath, or basename.
        Returns True if found and removed, False otherwise.
        """
        poems = self.getPoems()
        poems_to_keep = []
        found = False
        for poem in poems:
            basename = Path(poem.filepath).name
            if (poem.uuid == identifier or
                    poem.title == identifier or
                    poem.filepath == identifier or
                    basename == identifier):
                found = True
            else:
                poems_to_keep.append(poem)
        if found:
            with open(self.config_entry.getFile(), 'w') as f:
                for poem in poems_to_keep:
                    f.write(poem.toCsv())
        return found


class ConfigDatabase:
    BASE_DIR="./config"
    BASE_FILE=f"{BASE_DIR}/_base.cfg"

    def __init__(self):
        base_path = Path(ConfigDatabase.BASE_FILE)
        if not base_path.is_file():
           # if the base config file doesn't exist, try to make it
           base_path.parent.mkdir(parents=True, exist_ok=True)
           # touch the file
           base_path.touch()

    def getEntries(self):
        """
        Returns the entries in the current configuration database
        """
        entries = []
        with open(self.BASE_FILE, 'r') as file:
            for line in file.readlines():
                cfg = ConfigEntry.fromCsv(line)
                if cfg is not None:
                    entries.append(cfg.toString())
        return entries

    def addEntry(self, entry: ConfigEntry):
        """
        Create a configuration entry with the specified name and add it to the configuration database
        """
        # make sure the config entry isn't already present
        with open(self.BASE_FILE, 'r') as base_cfg_file:
            for line in base_cfg_file.readlines():
                cur_cfg: ConfigEntry = ConfigEntry.fromCsv(line)
                if cur_cfg is not None and cur_cfg.getName() == entry.getName():
                    return f"Error: config {entry.getName()} already exists."

        # if not already exists, add it
        with open(self.BASE_FILE, 'a') as file:
            file.write(f"{entry.toCsv()}\n")

        # and initialize the new entry's configuration file
        new_cfg_path = Path(entry.getFile())
        new_cfg_path.touch()

    def removeEntry(self, entry: ConfigEntry):
        """
        Remove the specified entry from the database
        """
        entries_to_keep: list = []
        entry_found: bool = False
        removed_entry = None
        with open(self.BASE_FILE, 'r') as base_cfg_file:
            for line in base_cfg_file.readlines():
                cur_cfg: ConfigEntry = ConfigEntry.fromCsv(line)
                if cur_cfg is None:
                    raise Exception(f"error while parsing config entry line '{line}'")
                elif cur_cfg.getName() == entry.getName():
                    entry_found = True
                    removed_entry = cur_cfg
                else:
                    entries_to_keep.append(cur_cfg)
        # if the entry to be removed was found, overwrite the config file
        if entry_found:
            with open(self.BASE_FILE, 'w') as base_cfg_file:
                for e in entries_to_keep:
                    base_cfg_file.write(e.toCsv() + "\n")
            # and remove the config file for the removed entry
            os.remove(removed_entry.getFile())

    def getEntry(self, name: str):
        """
        Get the specified configuration entry. If not found, return None
        """
        with open(self.BASE_FILE, 'r') as file:
            for line in file.readlines():
                entry = ConfigEntry.fromCsv(line)
                if entry is not None:
                    if entry.getName() == name:
                        return entry
        return None

    def getFirstEntry(self):
        """
        Get the first ConfigEntry from the base file, or None if empty.
        """
        with open(self.BASE_FILE, 'r') as file:
            for line in file.readlines():
                entry = ConfigEntry.fromCsv(line)
                if entry is not None:
                    return entry
        return None


class HtmlPage:
    NUM_FIELDS = 2
    #                           1            2      3
    #                       date            num     title
    SOURCE_PATTERN = r"^(\d\d\d\d.\d\d.\d\d)(_\d+_)(.*)\.txt$"

    # instance fields. Lay them out here for clarity
    source_file: str = ""
    page_file: str = ""
    date: str = ""
    title: str = ""

    def __init__(self, source_file: str, title: str|None = None):
        """
        Tries to create a HtmlPage from the inputs. Throws an exception if the source file is formatted incorrectly.
        """
        match = re.search(HtmlPage.SOURCE_PATTERN, source_file)
        if not match:
            raise ValueError(f"unable to parse source file {source_file}")
        else:
            # store the source file
            self.source_file = source_file
            # pull the date from the source file
            self.date = match.group(1)
            # if title not provided, pull it from the source file.
            # otherwise, use the provided one
            if title is None:
                self.title = match.group(3)
            else:
                self.title = title
            # set the page title (same as the source, with html extension)
            self.page_file = f"{match.group(1)}{match.group(2)}{match.group(3)}.html"

    def write(self, dest_dir: Path = Path(".")):
        out_path = dest_dir / self.page_file
        with open(out_path, 'w') as file:
            file.write("<!DOCTYPE html>")
            file.write("<html lang=\"en\">")
            file.write("<head>")
            file.write("    <meta charset=\"UTF-8\">")
            file.write("    <link rel=\"stylesheet\" href=\"/styles.css\">")
            file.write(f"    <title>{self.title}</title>")
            file.write("</head>")
            file.write("<body>")
            file.write("    <div id=\"poem\"></div>")
            file.write("    <script>")
            file.write(f"        fetch('/src/{self.source_file}')")
            file.write("        .then(response => response.text())")
            file.write("        .then(data => {")
            file.write("            document.getElementById('poem').innerText = data;")
            file.write("        })")
            file.write("        .catch(error => console.error('Error loading poem:', error));")
            file.write("    </script>")
            file.write("</body>")
            file.write("</html>")


def generate_index(pages, dest_dir: Path):
    """Generate an index.html table of contents for the given HtmlPage objects."""
    rows = ""
    for page in pages:
        title_display = page.title.replace('-', ' ')
        rows += f'        <tr><td><a href="{page.page_file}">{title_display}</a></td><td>{page.date}</td></tr>\n'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="/styles.css">
    <title>Poems</title>
</head>
<body>
    <table>
{rows}    </table>
</body>
</html>"""

    out_path = dest_dir / "index.html"
    with open(out_path, 'w') as f:
        f.write(html)
