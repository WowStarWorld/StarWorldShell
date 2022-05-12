import os
import importlib
import rich.console
import sys

plugins = {}
scoreboards = {}
console = rich.console.Console()
print = console.print
input = console.input
log = console.log
swlocals:dict
version = "1.0.0"

def quits():
    log("[green]Disabling...[/green]")
    for plugin in plugins:
        if hasattr(plugins[plugin]["plugin"], "onDisable"):
            try:
                plugins[plugin]["plugin"].onDisable()
            except:
                pass
    raise ExitError(0)


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

def command_lists(*args):
    if args[1] == ():
        log("[bold blue]Available commands:[yellow]\n {}".format(", ".join(registered_commands.keys())))
    else:
        if args[1][0] in command_informations:
            log("[green]{}[/green]".format(args[1][0]))
            log("[green]Name: {}[/green]".format(command_informations[args[1][0]]["name"]))
            log("[green]Description: {}[/green]".format(command_informations[args[1][0]]["description"]))
            log("[green]Usage: {}[/green]".format(command_informations[args[1][0]]["usage"]))
            log("[green]Plugin: {}[/green]".format(command_informations[args[1][0]]["plugin"]))
        else:
            raise CommandNotFoundError("Command not found")
def plugin_lists(*args):
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


def reloads(*args):
    for i in plugins:
        importlib.reload(plugins[i]["plugin"])
        if hasattr(plugins[i]["plugin"], "onReload"):
            plugins[i]["plugin"].onReload()
        



registered_commands = {
    "plugins": plugin_lists,
    "exit": quits,
    "help": lambda *args :command_lists(registered_commands,args),
    "reload":reloads,
    "version":lambda *args:log("[green]StarWorldShell version: {}[/green]".format(version)),
    "clear":lambda *args:console.clear(),
}

class CommandNotFoundError(Exception): pass
class ExitError(Exception): pass
class PluginNotFoundError(Exception): pass




def exception_format():
    return sys.exc_info()[0].__name__ + ": " + str(sys.exc_info()[1]) if str(sys.exc_info()[1]) != "" else \
        sys.exc_info()[0].__name__


def parse_command(command_string):
    command_string = command_string.split(' ')
    for i in range(len(command_string)):
        command_string[i-1] = command_string[i-1].replace("${space}", " ").replace("${replace}", "$")
    for i in plugins:
        if hasattr(plugins[i]["plugin"], "onCommand"):
            plugins[i]['plugin'].onCommand(command_string)
    if command_string[0] in registered_commands:
        
        if len(command_string) > 1:
            try:
                return registered_commands[command_string[0]](*command_string[1:])
            except ExitError:
                if sys.exc_info()[1]:
                    sys.exit(int(str(sys.exc_info()[1])))
                else:
                    sys.exit(0)
            except PluginNotFoundError:
                raise PluginNotFoundError("Plugin not found")
            except:
                console.log("[red]An internal error occurred while attempting to perform this[/red]")
        else:
            try:
                return registered_commands[command_string[0]]()
            except ExitError:
                if sys.exc_info()[1]:
                    sys.exit(int(str(sys.exc_info()[1])))
                else:
                    sys.exit(0)
            except PluginNotFoundError:
                raise PluginNotFoundError("Plugin not found")
            except:
                console.log("[red]An internal error occurred while attempting to perform this[/red]")
    else:
        raise CommandNotFoundError("Command not found")


def load_plugins_from_plugins_folder():
    plugins_path = os.path.join(os.path.dirname(__file__), 'plugins')
    if not os.path.join(os.path.dirname(__file__), 'plugins'):
        os.mkdir(plugins_path)
    for plugin_path in os.listdir(plugins_path):
        if plugin_path.endswith('.py'):
            plugin_name = plugin_path[:-3]
            try:
                pl = importlib.import_module('plugins.' + plugin_name)
            except:
                return
            pl.swshell = swlocals
            pl.plugin_path = os.path.join(os.path.dirname(__file__), 'plugins')
            if hasattr(pl, 'info'):
                plugins["[green]" + (pl.info["name"].replace(" ","_").replace("\\","").replace("[", "\[")) + "[/green]"] = {"info": pl.info, "plugin": pl}
            else:
                console.log('[red]Invalid Plugin \"{}\"'.format(plugin_path))
                return
            if hasattr(pl, 'onLoad'):
                try:
                    pl.onLoad(*sys.argv)
                except:
                    plugins.pop("[green]" + (pl.info["name"].replace(" ","_").replace("\\","").replace("[", "\[")) + "[/green]")
                    plugins["[red]" + (pl.info["name"].replace(" ","_").replace("\\","").replace("[", "\[")) + "[/red]"] = {"info": pl.info,
                                                                                          "plugin": pl}
                    console.log(exception_format(), style="red")
            if "commands" in pl.info:
                for command in range(len(pl.info["commands"])):
                    if "[red]" + (pl.info["name"].replace(" ","_").replace("\\","").replace("[", "\[")) + "[/red]" in plugins:
                        pl.info["commands"][command-1]["function"] = lambda *args:console.log("[red]An internal error occurred while attempting to perform this[/red]")

swlocals = locals()
if __name__ == '__main__':
    console.log("[yellow]StarWorldShell v{}".format(version))
    console.log("[bold yellow]Loading Plugins...")
    load_plugins_from_plugins_folder()
    console.log("[bold yellow]Plugins Loaded.")
    console.log("[bold yellow]Loading Commands...")
    for plugin in plugins:
        if "commands" in plugins[plugin]["info"]:
            for command in plugins[plugin]["info"]["commands"]:
                registered_commands[command["name"]] = command["function"]
                registered_commands["".join(filter(str.isalnum, plugins[plugin]["info"]["name"])).lower().replace(" ","_")+":"+command["name"]] = command["function"]
                command.pop("function")
                command["plugin"] = plugins[plugin]["info"]["name"]
                command_informations[command["name"]] = command
                command_informations["".join(filter(str.isalnum, command["plugin"])).lower().replace(" ","_")+":"+command["name"]] = command
    console.log("[bold yellow]Commands Loaded.") 
    console.log(f"[bold yellow]Done.")
    console.log("[bold yellow]Type \"/help\" for a list of commands.")
    for i in plugins:
        if hasattr(plugins[i]["plugin"], "onHelp"):
            plugins[i]["plugin"].onHelp()
    while True:
        try:
            command = input("[green]==> ")
        except:
            quits()
        try:
            if command.strip() == "":
                pass
            elif command[0] != "/":
                r = 0
                for i in plugins:
                    if hasattr(plugins[i]["plugin"], "onMessage"):
                        if plugins[i]['plugin'].onMessage(command):
                            r += 1
                if r == 0:
                    console.log(command)
                del r

            else:
                command = command[1:].strip()
                while "  " in command:
                    command = command.replace("  "," ")
                parse_command(command.replace("\t",""))
        except CommandNotFoundError:
            console.log("[red]Command not found")
        except PluginNotFoundError:
            console.log("[red]Plugin not found")
        except Exception:
            console.log(exception_format(), style="red")

