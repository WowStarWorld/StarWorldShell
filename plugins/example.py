import rich.console
import time
import os

plugin_path:str
swshell:dict

console = rich.console.Console()
info = {
    "name": "example plugin",
    "author": "WoWStarWorld",
    "description": "example",
    "version": "1.0",
    "website": "https://github.com/WowStarWorld",
    "license": "MIT License",
    "commands": [
        {
            "name": "args",
            "function": lambda *args: console.log(args),
            "description": "Get args",
            "usage": "args <*args>"
        }
    ]
}


def onLoad(*args) -> None:
    console.log("[green]\[Example] Enabled !")

def onDisable(*args) -> None:
    console.log("[red]\[Example] Disabled !")

def onCommand(*args) -> None:
    #console.log("[green]\[Example] Command called !")
    pass

def onReload(*args) -> None:
    console.log("[green]\[Example] Reloaded !")

