"""
cli.py

Entrypoint for the poem tool utility
"""

from .commands import CommandParser, doCommand

def getHelp():
    return CommandParser.getGeneralHelp()

def main():
    keyword, args, help_flag = CommandParser.parseCommandArgs()
    try:
        command = CommandParser.getCommand(keyword)
        if help_flag:
            print(command.getHelp())
        else:
            output = doCommand(command, args)
            if output is not None:
                print(output)
    except ValueError:
        if keyword is not None:
            print(f"Unrecognized command keyword {keyword}")
        print(getHelp())

if __name__ == "__main__":
    main()
