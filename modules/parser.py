import sys
import rich.console
from .exceptions import ExitError,PluginNotFoundError,CommandNotFoundError
console = rich.console.Console()

# Command Parser
def parse_command(command_string,registered_commands,plugins):
    command_string = command_string.split(' ')
    for i in range(len(command_string)):
        command_string[i-1] = command_string[i-1].replace("${}", " ").replace("${r}", "$")
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
                console.print_exception(show_locals=True, )
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
                console.print_exception(show_locals=True)
                console.log("[red]An internal error occurred while attempting to perform this[/red]")
    else:
        raise CommandNotFoundError("Command not found")

# Message Parser
def parse_message(plugins,command):
    r = 0
    for i in plugins:
        if hasattr(plugins[i]["plugin"], "onMessage"):
            if plugins[i]['plugin'].onMessage(command):
                r += 1
    if r == 0:
        console.log(command)
    del r