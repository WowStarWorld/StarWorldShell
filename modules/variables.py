import rich.console
from .functions import plugin_lists, command_lists, quits,reloads

plugins = {}
console = rich.console.Console(stderr=True,)
print = console.print
input = console.input
log = console.log
swlocals:dict
version = "1.2.0"

command_informations = {
    "plugins":{
        "name":"plugins",
        "description":"List all plugins",
        "usage":"plugins | plugins <plugin>",
        "plugin":"StarWorldShell"
    },
    "exit":{
        "name":"exit",
        "description":"Exit the program",
        "usage":"exit",
        "plugin":"StarWorldShell"
    },
    "help":{
        "name":"help",
        "description":"List all commands",
        "usage":"help | help <command>",
        "plugin":"StarWorldShell"
    },
    "version":{
        "name":"version",
        "description":"StarWorldShell version",
        "usage":"version",
        "plugin":"StarWorldShell"
    },
    "reload":{
        "name":"reload",
        "description":"Reload all plugins",
        "usage":"reload",
        "plugin":"StarWorldShell"
    }
}




        
registered_commands = {
    "plugins": lambda *args:plugin_lists(*args,plugins=plugins),
    "exit": lambda:quits(plugins),
    "help": lambda *args :command_lists(registered_commands,args,registered_commands=registered_commands,command_informations=command_informations),
    "reload":lambda: reloads(plugins=plugins),
    "version":lambda *args:log("[green]StarWorldShell version: {}[/green]".format(version)),
    "clear":lambda *args:console.clear(),
}

