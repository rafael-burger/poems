"""
paths.py

Resolves repo-anchored locations for user data (config/) and command help
text (command-help/), independent of the caller's current working directory.
Relies on this being an editable install, so __file__ points at the real
source tree inside the repo rather than a copy in site-packages.
"""

from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent

CONFIG_DIR = TOOLS_DIR / "config"
COMMAND_HELP_DIR = TOOLS_DIR / "command-help"
