import os
import importlib
import sys

import modules.exceptions
import modules.functions
import modules.parser
import modules.variables

input = modules.variables.input
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
                modules.variables.console.print_exception()
                continue
            pl.swshell = swlocals
            pl.plugin_path = os.path.join(os.path.dirname(__file__), 'plugins')
            if hasattr(pl, 'info'):
                modules.variables.plugins["[green]" + (pl.info["name"].replace(" ","_").replace("\\","").replace("[", "\[")) + "[/green]"] = {"info": pl.info, "plugin": pl}
            else:
                modules.variables.console.log('[red]Invalid Plugin \"{}\"'.format(plugin_path))
                return
            if hasattr(pl, 'onLoad'):
                try:
                    pl.onLoad(*sys.argv)
                except:
                    modules.variables.plugins.pop("[green]" + (pl.info["name"].replace(" ","_").replace("\\","").replace("[", "\[")) + "[/green]")
                    modules.variables.plugins["[red]" + (pl.info["name"].replace(" ","_").replace("\\","").replace("[", "\[")) + "[/red]"] = {"info": pl.info,
                                                                                          "plugin": pl}
                    modules.variables.console.print_exception(show_locals=True)
            if "commands" in pl.info:
                for command in range(len(pl.info["commands"])):
                    if "[red]" + (pl.info["name"].replace(" ","_").replace("\\","").replace("[", "\[")) + "[/red]" in modules.variables.plugins:
                        pl.info["commands"][command-1]["function"] = lambda *args:modules.variables.console.log("[red]An internal error occurred while attempting to perform this[/red]")

swlocals = locals()
if __name__ == '__main__':
    modules.variables.console.log("[yellow]StarWorldShell v{}".format(modules.variables.version))
    modules.variables.console.log("[bold yellow]Loading Plugins...")
    load_plugins_from_plugins_folder()
    modules.variables.console.log("[bold yellow]Plugins Loaded.")
    modules.variables.console.log("[bold yellow]Loading Commands...")
    for plugin in modules.variables.plugins:
        if "commands" in modules.variables.plugins[plugin]["info"]:
            for command in modules.variables.plugins[plugin]["info"]["commands"]:
                modules.variables.registered_commands[command["name"]] = command["function"]
                modules.variables.registered_commands["".join(filter(str.isalnum, modules.variables.plugins[plugin]["info"]["name"])).lower().replace(" ","_")+":"+command["name"]] = command["function"]
                command.pop("function")
                command["plugin"] = modules.variables.plugins[plugin]["info"]["name"]
                modules.variables.command_informations[command["name"]] = command
                modules.variables.command_informations["".join(filter(str.isalnum, command["plugin"])).lower().replace(" ","_")+":"+command["name"]] = command
    modules.variables.console.log("[bold yellow]Commands Loaded.") 
    modules.variables.console.log(f"[bold yellow]Done.")
    modules.variables.console.log("[bold yellow]Type \"/help\" for a list of commands.")
    for i in modules.variables.plugins:
        if hasattr(modules.variables.plugins[i]["plugin"], "onHelp"):
            modules.variables.plugins[i]["plugin"].onHelp()
    print()
    while True:
        try:
            command = input(f"[green]{os.getcwd()}> ")
        except KeyboardInterrupt:
            print()
            modules.variables.console.print_exception()
        except EOFError:
            print()
            modules.variables.console.print_exception()
        except Exception:
            modules.functions.quits(modules.variables.plugins)
        try:
            if command.strip() == "":
                pass
            elif command[0] != "/":
                modules.parser.parse_message(modules.variables.plugins,command)
            else:
                command = command[1:].strip()
                while "  " in command:
                    command = command.replace("  "," ")
                modules.parser.parse_command(command.replace("\t",""), modules.variables.registered_commands, modules.variables.command_informations)
        except modules.exceptions.CommandNotFoundError:
            modules.variables.console.log("[red]Command not found")
        except modules.exceptions.PluginNotFoundError:
            modules.variables.console.log("[red]Plugin not found")
        except Exception:
            modules.variables.console.print_exception()
