"""
poem_tool.py

Entrypoint for the poem tool utility
"""

from poem_tool_commands import Command, CommandParser, doCommand

def getHelp():
    return CommandParser.getGeneralHelp()

if __name__ == "__main__":
    keyword, args, help_flag = CommandParser.parseCommandArgs()
    try: 
        command = CommandParser.getCommand(keyword)
        command_name = command.getName()
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
