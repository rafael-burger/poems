"""
poem_tool_handler.py
"""

from website_config import ConfigDatabase, ConfigEntry

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
        # check the args
        if len(args) != 1:
            return "Error: invalid args"
        else:
            print(f"adding config: args={args}")
            config_name = args[0]
            db = ConfigDatabase()
            new_config = ConfigEntry(config_name)
            print("created new_config with:")
            print(f"  name={new_config.getName()}")
            print(f"  file={new_config.getFile()}")
            
            db.addEntry(new_config)

    def removeConfig(args: list):
        # check the args
        if len(args) != 1:
            return "Error: invalid args"
        else:
            print(f"removing config: args={args}")
            config_name = args[0];
            db = ConfigDatabase()
            entry = ConfigEntry(config_name)
            db.removeEntry(entry)
            

        print("TODO: remove config")

    def listPoems(args: list):
        print("TODO: list poems")

    def addPoem(args: list):
        print("TODO: add poem")

    def removePoem(args: list):
        print("TODO: remove poem")
