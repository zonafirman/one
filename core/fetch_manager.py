import os
import platform
import subprocess
import getpass
from core.base_manager import BaseManager

class FetchManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.C_SUBTLE = "\033[90m" # Keep a subtle color for separators

    def run(self):
        usr = getpass.getuser()
        host = platform.node()
        distro = "Ubuntu Linux"
        try: distro = subprocess.check_output(["lsb_release", "-sd"], text=True).strip().replace('"', '')
        except: pass
        
        logo = [
            f"      {self.C_CYAN}████████████{self.C_RESET}",
            f"    {self.C_CYAN}████████████████{self.C_RESET}",
            f"   {self.C_CYAN}████████  ████████{self.C_RESET}",
            f"  {self.C_CYAN}█████████  █████████{self.C_RESET}",
            f"  {self.C_CYAN}█████████  █████████{self.C_RESET}",
            f"  {self.C_CYAN}█████████  █████████{self.C_RESET}",
            f"  {self.C_CYAN}█████████  █████████{self.C_RESET}",
            f"   {self.C_CYAN}████████  ████████{self.C_RESET}",
            f"    {self.C_CYAN}████████████████{self.C_RESET}",
            f"      {self.C_CYAN}████████████{self.C_RESET}"
        ]

        info = [
            f"{self.C_BOLD}{self.C_GREEN}{usr}{self.C_RESET}{self.C_BOLD}{self.C_SUBTLE}@{self.C_RESET}{self.C_BOLD}{self.C_YELLOW}{host}{self.C_RESET}",
            f"{self.C_SUBTLE}" + "─" * (len(usr) + len(host) + 1) + f"{self.C_RESET}",
            f"{self.C_CYAN}OS      {self.C_SUBTLE}› {self.C_RESET}{distro}",
            f"{self.C_CYAN}Kernel  {self.C_SUBTLE}› {self.C_RESET}{platform.release()}",
            f"{self.C_CYAN}Shell   {self.C_SUBTLE}› {self.C_RESET}{self.C_YELLOW}{os.environ.get('SHELL','/bin/bash').split('/')[-1]}{self.C_RESET}",
            f"{self.C_CYAN}DE/WM   {self.C_SUBTLE}› {self.C_RESET}{os.environ.get('XDG_CURRENT_DESKTOP','N/A')}",
            f"    {self.C_RED}■ {self.C_GREEN}■ {self.C_YELLOW}■ {self.C_CYAN}■{self.C_RESET}"
        ]

        print("")
        ml = max(len(logo), len(info))
        for i in range(ml):
            l = logo[i] if i < len(logo) else " " * 28
            r = info[i] if i < len(info) else ""
            print(f" {l}   {r}")
        print("")