"""
poem_tool_handler.py
"""

import argparse
import os
import shutil
from pathlib import Path
from website_config import ConfigDatabase, ConfigEntry, PoemEntry, PoemConfig, HtmlPage, generate_index


def _resolve_config(db, args, name_index=0):
    """
    Return (ConfigEntry, remaining_args) or (None, None) on error.
    If args has an element at name_index, uses it as the config name.
    Otherwise uses the first config entry.
    """
    if name_index < len(args):
        entry = db.getEntry(args[name_index])
        if entry is None:
            print(f"Error: config '{args[name_index]}' not found")
            return None, None
        remaining = list(args[:name_index]) + list(args[name_index + 1:])
        return entry, remaining
    else:
        entry = db.getFirstEntry()
        if entry is None:
            print("Error: no configurations found. Use add-config to add one.")
            return None, None
        return entry, list(args)


class Handler:

    def listConfigs(args: list):
        db = ConfigDatabase()
        entries = db.getEntries()
        if len(entries) == 0:
            print("No saved configs")
        else:
            for entry in entries:
                print(entry)

    def addConfig(args: list):
        config_name = args[0]
        db = ConfigDatabase()
        new_config = ConfigEntry(config_name)
        result = db.addEntry(new_config)
        if result is not None:
            print(result)
        else:
            print(f"Added config '{config_name}'")

    def removeConfig(args: list):
        config_name = args[0]
        db = ConfigDatabase()
        entry = ConfigEntry(config_name)
        db.removeEntry(entry)
        print(f"Removed config '{config_name}'")

    def listPoems(args: list):
        db = ConfigDatabase()
        config, _ = _resolve_config(db, args, 0)
        if config is None:
            return
        poem_config = PoemConfig(config)
        poems = poem_config.getPoems()
        if len(poems) == 0:
            print(f"No poems in config '{config.getName()}'")
        else:
            for poem in poems:
                print(poem.toString())

    def addPoem(args: list):
        db = ConfigDatabase()
        if len(args) == 1:
            config, _ = _resolve_config(db, [], 0)
            poem_file = args[0]
        else:
            config, remaining = _resolve_config(db, args, 0)
            poem_file = remaining[0]
        if config is None:
            return
        if not os.path.isfile(poem_file):
            print(f"Error: poem file '{poem_file}' does not exist")
            return
        try:
            poem = PoemEntry.fromFile(poem_file)
        except ValueError as e:
            print(f"Error: {e}")
            return
        poem_config = PoemConfig(config)
        if poem_config.addPoem(poem):
            print(f"Added poem '{poem.title}' to config '{config.getName()}'")
        else:
            print(f"Error: poem '{poem_file}' already exists in config '{config.getName()}'")

    def removePoem(args: list):
        db = ConfigDatabase()
        if len(args) == 1:
            config, _ = _resolve_config(db, [], 0)
            identifier = args[0]
        else:
            config, remaining = _resolve_config(db, args, 0)
            identifier = remaining[0]
        if config is None:
            return
        poem_config = PoemConfig(config)
        if poem_config.removePoem(identifier):
            print(f"Removed poem '{identifier}' from config '{config.getName()}'")
        else:
            print(f"Error: poem '{identifier}' not found in config '{config.getName()}'")

    def generateHtml(args: list):
        parser = argparse.ArgumentParser(prog="generate-html", add_help=False)
        parser.add_argument("config_name", nargs="?", default=None)
        parser.add_argument("-d", "--dest-dir", default="./output")
        parsed = parser.parse_args(args)

        db = ConfigDatabase()
        if parsed.config_name is not None:
            config = db.getEntry(parsed.config_name)
            if config is None:
                print(f"Error: config '{parsed.config_name}' not found")
                return
        else:
            config = db.getFirstEntry()
            if config is None:
                print("Error: no configurations found. Use add-config to add one.")
                return

        dest_dir = Path(parsed.dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)
        src_dir = dest_dir / "src"
        src_dir.mkdir(exist_ok=True)

        poem_config = PoemConfig(config)
        poems = poem_config.getPoems()

        pages = []
        skipped_copies = 0
        for poem in poems:
            basename = Path(poem.filepath).name
            try:
                page = HtmlPage(basename, poem.title)
                dest_src_path = src_dir / basename
                if Path(poem.filepath).resolve() != dest_src_path.resolve():
                    shutil.copy2(poem.filepath, dest_src_path)
                else:
                    skipped_copies += 1
                page.write(dest_dir)
                pages.append(page)
            except ValueError as e:
                print(f"Warning: skipping '{poem.filepath}': {e}")

        if skipped_copies > 0:
            print(f"Warning: {skipped_copies} poem file(s) already in dest-dir/src; skipped copy.")

        generate_index(pages, dest_dir)
        print(f"Generated {len(pages)} poem page(s) and index.html in '{dest_dir}'")
