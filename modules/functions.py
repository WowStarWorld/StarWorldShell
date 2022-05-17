import rich.console
from .exceptions import ExitError, PluginNotFoundError,CommandNotFoundError
import importlib
import sys

console = rich.console.Console()

# Quit the program 
def quits(plugins):
    console.log("[green]Disabling...[/green]")
    for plugin in plugins:
        if hasattr(plugins[plugin]["plugin"], "onDisable"):
            try:
                plugins[plugin]["plugin"].onDisable()
            except:
                pass
    raise ExitError(0)

# Show the list of plugins
def plugin_lists(*args,plugins,log=console.log):
    if args == ():
        log("[bold blue]Available plugins:[yellow]\n {}".format(", ".join(plugins.keys())))
    else:
        if "[green]"+args[0]+"[/green]" in plugins:
            log("[green]{}[/green]".format(args[0]))
            log("[green]Name: {}[/green]".format(plugins["[green]"+args[0]+"[/green]"]["info"]["name"]))
            log("[green]Description: {}[/green]".format(plugins["[green]"+args[0]+"[/green]"]["info"]["description"]))
            log("[green]Version: {}[/green]".format(plugins["[green]"+args[0]+"[/green]"]["info"]["version"]))
            log("[green]Author: {}[/green]".format(plugins["[green]"+args[0]+"[/green]"]["info"]["author"]))
            log("[green]Website: {}[/green]".format(plugins["[green]"+args[0]+"[/green]"]["info"]["website"]))
            log("[green]License: {}[/green]".format(plugins["[green]"+args[0]+"[/green]"]["info"]["license"]))
            cmds = []
            for cmd in plugins["[green]"+args[0]+"[/green]"]["info"]["commands"]:
                cmds.append(cmd["name"])
            log("[green]Commands: {}[/green]".format(", ".join(cmds)))
        elif "[red]"+args[0]+"[/red]" in plugins:
            log("[red]{}[/red]".format(args[0]))
            log("[red]Name: {}[/red]".format(plugins["[red]"+args[0]+"[/red]"]["info"]["name"]))
            log("[red]Description: {}[/red]".format(plugins["[red]"+args[0]+"[/red]"]["info"]["description"]))
            log("[red]Version: {}[/red]".format(plugins["[red]"+args[0]+"[/red]"]["info"]["version"]))
            log("[red]Author: {}[/red]".format(plugins["[red]"+args[0]+"[/red]"]["info"]["author"]))
            log("[red]Website: {}[/red]".format(plugins["[red]"+args[0]+"[/red]"]["info"]["website"]))
            log("[red]License: {}[/red]".format(plugins["[red]"+args[0]+"[/red]"]["info"]["license"]))
            cmds = []
            for i in plugins["[red]"+args[0]+"[/red]"]["info"]["commands"]:
                cmds.append(i["name"])
            log("[red]Commands: {}[/red]".format(", ".join(cmds)))
        else:
            raise PluginNotFoundError("Plugin not found")

# Show the command list
def command_lists(*args,registered_commands,command_informations):
    if args[1] == ():
        console.log("[bold blue]Available commands:[yellow]\n {}".format(", ".join(registered_commands.keys())))
    else:
        if args[1][0] in command_informations:
            console.log("[green]{}[/green]".format(args[1][0]))
            console.log("[green]Name: {}[/green]".format(command_informations[args[1][0]]["name"]))
            console.log("[green]Description: {}[/green]".format(command_informations[args[1][0]]["description"]))
            console.log("[green]Usage: {}[/green]".format(command_informations[args[1][0]]["usage"]))
            console.log("[green]Plugin: {}[/green]".format(command_informations[args[1][0]]["plugin"]))
        else:
            raise CommandNotFoundError("Command not found")

# Reload the plugin
def reloads(*args,plugins):
    for i in plugins:
        importlib.reload(plugins[i]["plugin"])
        if hasattr(plugins[i]["plugin"], "onReload"):
            plugins[i]["plugin"].onReload(*sys.argv)