import rich.console
import os
import traceback

swshell:dict
console = rich.console.Console()
info = {
    "name": "Shell Command Parser",
    "author": "WoWStarWorld",
    "description": "SCP(ShellCommandParser) is a plugin that parses commands and executes them.",
    "version": "1.0",
    "website": "https://github.com/WowStarWorld",
    "license": "MIT License",
    "commands":[
    ]
}

class parser:
    names = {"help","chdir \[path]","start \[path]","echo \[*message]","pwd","eval \[*command]","command \[*command]","message \[*message]"}
    help = {
        "help":"Shows this help",
        "chdir \[path]":"Changes the current directory",
        "start \[path]":"Starts a program",
        "echo \[*message]":"Prints the message",
        "pwd":"Prints the current working directory",
        "eval \[*command]":"Evaluates a command",
        "command \[*command]":"Executes a command",
        "message \[*message]":"Send a message"
    }
    def __init__(self,command) -> None:
        self.__command = command
        self.__command_compiled = self.__command.split(" ")
        for i in range(len(self.__command_compiled)):
            self.__command_compiled[i-1] = self.__command_compiled[i-1].replace("${}", " ").replace("${r}", "$")
        self.__command_name = self.__command_compiled[0].lower()
        self.__command_args = self.__command_compiled[1:]
        self.__status__ = self.run()
    def run(self) -> None:
        if self.__command_name == "help":
            for i in self.names:
                console.log("[green]"+i)
                console.log("[white]    "+self.help[i])
        elif self.__command_name == "chdir":
            if len(self.__command_args) == 0:
                console.log("[red][SCP] Please enter a path")
            elif len(self.__command_args) == 1:
                os.chdir(self.__command_args[0])
            else:
                console.log("[red][SCP] Too many arguments")
        elif self.__command_name == "start":
            if len(self.__command_args) == 0:
                console.log("[red][SCP] Please enter a path")
            elif len(self.__command_args) == 1:
                os.startfile(self.__command_args[0])
            else:
                console.log("[red][SCP] Too many arguments")
        elif self.__command_name == "echo":
            if len(self.__command_args) == 0:
                console.log("[red][SCP] Please enter a message")
            else:
                console.log(" ".join(self.__command_args))
        elif self.__command_name == "pwd":
            console.log(os.getcwd())
        elif self.__command_name == "eval":
            if len(self.__command_args) == 0:
                console.log("[red][SCP] Please enter a command")
            else:
                arg = " ".join(self.__command_args[0:])
                if not self.__class__(arg.strip()).__status__:
                    console.log("[red][SCP] Invalid command")
        elif self.__command_name == "command":
            if len(self.__command_args) == 0:
                console.log("[red][SCP] Please enter a command")
            else:
                arg = " ".join(self.__command_args[0:])
                swshell["modules"].parser.parse_command(arg,swshell["modules"].variables.registered_commands, swshell["modules"].variables.command_informations)
        elif self.__command_name == "message":
            if len(self.__command_args) == 0:
                console.log("[red][SCP] Please enter a message")
            else:
                r = 0
                plugins = swshell["modules"].variables.plugins
                command = " ".join(self.__command_args[0:])
                for i in plugins:
                    if hasattr(plugins[i]["plugin"], "onMessage"):
                        if plugins[i]['plugin'].onMessage(command):
                            r += 1
                if r == 0:
                    console.log(command)
                del r
        else:
            return False
        return True

def onLoad(*args):
    console.log("[green][SCP] Enabled !")
def onDisable(*args):
    console.log("[red][SCP] Disabled !")
def onHelp(*args):
    console.log("[bold yellow]Type \"$help\" to see the help")
def onMessage(args):
    if args[0] == "$":
        if not parser(args[1:].strip()).__status__:
            console.log("[red][SCP] Invalid command")
    else:
        return False
    return True