import rich.console
import os


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
    help = [
        {"description":"Shows this help","usage":"help"},
        {"description":"Changes the current directory","usage":"chdir \[path]"},
        {"description":"Starts a program","usage":"start \[path]"},
        {"description":"Prints the message","usage":"echo \[*message]"}
    ]
    def __init__(self,command) -> None:
        self.__command = command
        self.__command_compiled = command.split(" ")
        for i in range(len(self.__command_compiled)):
            self.__command_compiled[i-1] = self.__command_compiled[i-1].replace("${}", " ").replace("${r}", "$")
        self.__command_name = self.__command_compiled[0].lower()
        self.__command_args = self.__command_compiled[1:]
        self.__status__ = self.run()
    def run(self) -> None:
        if self.__command_name == "help":
            for i in self.help:
                console.log("[green]"+i["usage"])
                console.log("[white]    "+i["description"])
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