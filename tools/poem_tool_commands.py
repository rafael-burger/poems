"""
poem_tool_commands.py

Entrypoint for the poem tool utility
"""

import argparse
import re
from poem_tool_handler import Handler

class Command:
    HELPDIR = "command-help"
    STARTHELP_PATTERN = r"^\s*STARTHELP\s*$"
    ENDHELP_PATTERN = r"^\s*ENDHELP\s*$"
    def __init__(self, keywords: list, help: str, nargs: int, cb: callable):
        self.keywords = keywords
        self.help = help
        self.nargs = nargs     
        self.callback = cb

    def getName(self):
        return self.keywords[0]

    def getHelp(self):
        help_file = f"{Command.HELPDIR}/{self.getName()}.txt"
        help_str = ""
        with open(help_file, 'r') as file:
            ON_FLAG = False # only print lines between "STARTHELP" and "ENDHELP"
            for line in file.readlines():
                match_start = re.search(Command.STARTHELP_PATTERN, line)
                match_end = re.search(Command.ENDHELP_PATTERN, line)
                if match_start:
                    ON_FLAG = True
                elif match_end:
                    ON_FLAG = False
                elif ON_FLAG:
                    help_str += f"{line}"
        return help_str

    def getNargs(self):
        return self.nargs

    def matches(self, keyword: str):
        return keyword in self.keywords

    

class CommandParser:

    COMMANDS = {
        "list-configs": Command(
            ["list-configs", "lscfg"],   "List the available configurations",  0, Handler.listConfigs
            ),
        "add-config": Command(
            ["add-config", "addcfg"],    "Add a configuration",                1, Handler.addConfig
            ),
        "remove-config": Command(
            ["remove-config", "rmcfg"],  "Remove a configuration",             1, Handler.removeConfig
            ),
        "list-poems": Command(
            ["list-poems", "lsp"],       "List the poems in the specified configuration", 1, Handler.listPoems
            ),
        "add-poem": Command(
            ["add-poem", "addp"],        "Add a poem to the specified configuration", 2, Handler.addPoem
            ),
        "remove-poem": Command(
            ["remove-poem", "rmp"],      "Remove a poem from the specified configuration", 2, Handler.removePoem
            )
    }

    def parseCommandArgs():
        parser = argparse.ArgumentParser(description="Poem Tool Command Line Utility.", add_help=False)
        parser.add_argument("command", type=str, nargs='?')
        parser.add_argument("arguments", nargs="*")
        parser.add_argument("-h", "--help", action='store_true')
        args = parser.parse_args()
        return [args.command, args.arguments, args.help]
    
    def getCommand(keyword: str):
        """
        Just checks if the provided command string maps to a valid command. If it does,
        returns the matching command. Otherwise, raises ValueError
        """
        for command in CommandParser.COMMANDS.values():
            if command.matches(keyword):
                return command
        raise ValueError

def doCommand(command: Command, args: list):
    if len(args) != command.getNargs():
        return False
    else:
        return command.callback(args)
