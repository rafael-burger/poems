"""
website_config.py

Functions and classes associated with managing website configuration
"""

from pathlib import Path
import re
import os

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
        Lists (prints) the entries in the current configuration database
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
        # find the entry to remove
        entries_to_keep: list = [] 
        entry_found: bool = False
        print(f"trying to open file {self.BASE_FILE}")
        with open(self.BASE_FILE, 'r') as base_cfg_file:
            print(f"trying to remove entry with name={entry.getName()}")
            for line in base_cfg_file.readlines():
                cur_cfg: ConfigEntry = ConfigEntry.fromCsv(line)
                if cur_cfg is not None:
                    print(f"comparing it to cur_entry with name={cur_cfg.getName()}")
                if cur_cfg is None:
                    raise Exception("error while parsing config entry line '{line}'")
                elif cur_cfg.getName() == entry.getName():
                    print("Removing config '{entry.getName()}'")
                    entry_found = True
                else:
                    entries_to_keep.append(cur_cfg)
        # if the entry to be removed was found, overwrite the config file
        if entry_found:
            with open(self.BASE_FILE, 'w') as base_cfg_file:
                for entry in entries_to_keep:
                    base_cfg_file.write(entry.toCsv())
            # and remove the config file for the removed entry
            print(f"trying to remove file '{entry.getFile()}")
            os.remove(entry.getFile())
            


        
                    
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


class HtmlPage:
    NUM_FIELDS = 2
    #                           1            2      3
    #                       date            num     title
    SOURCE_PATTERN = r"$(\d\d\d\d.\d\d.\d\d)(_\d+_)(.*)\.txt^"
    
    # instance fields. Lay them out here for clarity
    source_file: str = ""
    page_file: str = ""
    date: str = ""
    title: str = ""

    def __init__(self, source_file: str, title: str|None):
        """ 
        Tries to create a HtmlPage from the inputs. Throws an exception if the source file is formatted incorrectly.
        """
        match = re.search(SOURCE_PATTERN, source_file) 
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

    def write(self):
        with open(self.page_file, 'w') as file: 
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
