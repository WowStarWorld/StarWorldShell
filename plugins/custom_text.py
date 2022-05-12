import os
import rich.console
import rich.markdown
import datetime


console = rich.console.Console()

plugin_path:str
custom_text_list = {

}



info = {
    "name": "Custom text",
    "author": "WoWStarWorld",
    "description": "Custom text",
    "version": "1.0",
    "website": "https://github.com/WowStarWorld",
    "license": "MIT License",
    "commands": [
        {
            "name": "custom_text",
            "description": "List of custom text",
            "usage": "custom_text",
            "function": lambda: console.log("Custom Texts: "+", ".join(custom_text_list.keys())),
        }
    ]
}
def onLoad(*args):
    if os.path.isdir(os.path.join(plugin_path,"custom_text")):
        for file in os.listdir(os.path.join(plugin_path,"custom_text")):
           if file.endswith(".txt"):
                with open(os.path.join(plugin_path,"custom_text",file),"rb") as f:
                    custom_text_list["".join(filter(str.isalnum, file.split(".")[0])).replace(" ","")] = f.read().decode("utf-8")
    else:
        os.mkdir(os.path.join(plugin_path,"custom_text"))
    console.log("\[Custom text] Enabled",style="bold green")


def onMessage(args):
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    if args[0] == "*":
        if args[1:] in custom_text_list:
            console.log(rich.markdown.Markdown(custom_text_list[args[1:]].replace("%now_year%",str(date.year)).replace("%now_month%",str(date.month)).replace("%now_day%",str(date.day)).replace("%now_hour%",str(currentDateTime.hour)).replace("%now_minute%",str(currentDateTime.minute)).replace("%now_second%",str(currentDateTime.second)).replace("%placeholder%","%")))
        else:
            return False
    else:
        return False
    return True
def onDisable(*args):
    console.log("\[Custom text] Disabled",style="bold red")


def onReload(*args):
    console.log("\[Custom text] Reloading",style="bold green")
    onLoad()

def onHelp(*args):
    console.log("[bold yellow]Type \"*[Text]\" to print custom text")