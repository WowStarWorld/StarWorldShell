import os
import rich.console
console = rich.console.Console()

def print_dir(path, level=0):
    try:
        for file in os.listdir(path):
            if os.path.isdir(os.path.join(path, file)):
                console.log("│  " * level + "├─" + file)
                print_dir(os.path.join(path, file), level + 1)
            else:
                console.log("│  " * level + "├─" + file)
    except:pass

def print_dir_command(*args) -> None:
    console.print("_"*console.width)
    if args == ():
        print_dir(os.getcwd())
    else:
        print_dir(args[0])

info = {
    "name": "SWTree",
    "author": "WoWStarWorld",
    "description": "Display directory tree",
    "version": "1.0",
    "website": "https://github.com/WowStarWorld",
    "license": "MIT License",
    "commands": [
        {
            "name": "tree",
            "function": print_dir_command,
            "description": "Print dir tree",
            "usage": "tree | tree <path>"
        }
    ]
}

def onLoad(*args) -> None:
    console.log("[green]\[SWTree] Enabled !")

def onDisable(*args) -> None:
    console.log("[red]\[SWTree] Disabled !")