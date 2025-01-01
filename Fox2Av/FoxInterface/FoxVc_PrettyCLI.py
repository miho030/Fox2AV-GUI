# -*- coding: utf-8 -*-
# Author : github.com/miho030

from datetime import datetime
from pyfiglet import Figlet
from rich.console import Console
from rich.panel import Panel

from Fox2Av.Foxcore import FOX_VERSION, FOX_BUILDDATA, FOX_LASTYEAR, FOX_NAME, Author
cl = Console()


def datetime_caller():
    now = datetime.now().strftime('[%Y-%m-%d | %H:%M:%S]')
    return now

def call_datetime_cli(contents :str):
    curDateTime = datetime_caller()
    cl.print("[bold magenta]%s[/bold magenta]\t[bold blue]%s[/bold blue]" % (curDateTime, contents), style="blue")

def call_cli(contents :str):
    cl.print("\t[bold magenta]> [/bold magenta] [bold yellow]%s[/bold yellow]" % (contents), style="#ffa500")

def software_info():
    panel = Panel("[bold green]Open-Source Anti-Virus Engine[/bold green]\n" + \
                  "[bold red]signature based malware detection service[/bold red]\n" + \
                  "software version: [bold yellow]%s[/bold yellow] \tauthor: [bold underline yellow]%s[/bold underline yellow]" % (FOX_VERSION, Author), style="bold blue")
    cl.print(panel)
    print("\n")

def call_cli_var(var :str):
    cl.print("\t[bold magenta]>  [/bold magenta]" + "[orange]%s[/orange]" % (str(var)), end="\r")

def call_input_datetime(contents):
    curDateTime = datetime_caller()
    cl.print("[bold magenta]%s[/bold magenta]\t[bold blue]%s[/bold blue]" % (curDateTime, contents), style="blue")
    user_input = str(input(""))
    return user_input

def call_input(contents :str):
    cl.print("\t[bold magenta]> [/bold magenta] [bold yellow]%s[/bold yellow]" % (contents), style="#ffa500")
    user_input = str(input("\t"))
    return user_input

def devider():
    cl.print("-"*80, style="white")

def usage():
    print("Usage! \n")

def print_FoxVc_Logo():
    f = Figlet(font='slant')
    title = "Fox2Av " + str(FOX_VERSION)
    print(f.renderText(title))
    software_info()