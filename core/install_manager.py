# core/install_manager.py
import subprocess
import sys
import shutil
from core.base_manager import BaseManager

class InstallManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.C_SUBTLE  = "\033[90m"

    def _get_smart_suggestions(self, query):
        suggestions = []
        if shutil.which("flatpak"):
            try:
                out = subprocess.check_output(["flatpak", "search", "--columns=application", query], text=True, stderr=subprocess.DEVNULL)
                for line in out.strip().split("\n"):
                    if line.strip() and "." in line and line.strip() != "Application":
                        suggestions.append({"type": "Flatpak", "id": line.strip()})
                    if len(suggestions) >= 2: break
            except: pass
        if shutil.which("snap") and len(suggestions) < 5:
            try:
                out = subprocess.check_output(["snap", "find", query], text=True, stderr=subprocess.DEVNULL)
                for line in out.strip().split("\n"):
                    if line.startswith("Name") or not line.strip(): continue
                    parts = [p.strip() for p in line.split("  ") if p.strip()]
                    if parts and not any(s["id"] == parts[0] for s in suggestions):
                        suggestions.append({"type": "Snap", "id": parts[0]})
                    if len(suggestions) >= 4: break
            except: pass
        try:
            out = subprocess.check_output(["apt-cache", "pkgnames", query], text=True, stderr=subprocess.DEVNULL)
            for line in out.strip().split("\n"):
                if line.strip() and len(suggestions) < 5:
                    if not any(s["id"] == line.strip() for s in suggestions):
                        suggestions.append({"type": "APT", "id": line.strip()})
        except: pass
        return suggestions[:5]

    def run(self):
        args = sys.argv[2:]
        if not args:
            self.error("Usage: one install [-l] <package_name>")
            return
            
        if args[0] == "-l":
            if len(args) < 2:
                self.error("Usage: one install -l <path_to_deb_file>")
                return
            self.install_local(args[1])
            return
            
        self.smart_install(args[0])

    def install_local(self, file_path):
        import os
        abs_path = os.path.abspath(file_path)
        if not os.path.exists(abs_path):
            self.error(f"File not found: {file_path}")
            return
        if not abs_path.endswith(".deb"):
            self.error("Local installation only supports .deb files.")
            return
            
        self.info(f"Installing local package: {os.path.basename(abs_path)}")
        try:
            subprocess.run(["sudo", "apt-get", "install", "-y", abs_path], check=True)
            self.success(f"Successfully installed {os.path.basename(abs_path)}")
        except subprocess.CalledProcessError:
            self.error("Failed to install local package.")

    def smart_install(self, pkg_name):
        if not pkg_name:
            self.error("Package name cannot be empty.")
            return
        if "." in pkg_name and shutil.which("flatpak"):
            subprocess.run(["flatpak", "install", "flathub", pkg_name, "-y"])
            return

        self.info(f"Searching for best candidates to install '{pkg_name}'...")
        choices = self._get_smart_suggestions(pkg_name)
        if not choices:
            self.error(f"Package '{pkg_name}' not found in any registered repository.")
            return

        print(f"\n  {self.C_BOLD}{self.C_SUBTLE}[ Select Package Source ]{self.C_RESET}")
        for idx, item in enumerate(choices, start=1):
            c = self.C_YELLOW if item['type']=="APT" else (self.C_GREEN if item['type']=="Flatpak" else self.C_RED)
            print(f"      {c}{idx}. {item['id']:<40} [{item['type']}]{self.C_RESET}")
        print("")
        
        try:
            inp = input(f"  {self.C_CYAN}❓ Choose a number (1-{len(choices)} or 'c' to cancel): {self.C_RESET}").strip()
            if inp.lower() == 'c': return
            idx = int(inp) - 1
            if 0 <= idx < len(choices):
                t = choices[idx]
                if t['type'] == "APT": subprocess.run(["sudo", "apt-get", "install", "-y", t['id']])
                elif t['type'] == "Flatpak": subprocess.run(["flatpak", "install", "flathub", t['id'], "-y"])
                elif t['type'] == "Snap": subprocess.run(["sudo", "snap", "install", t['id']])
                self.success("Installation completed successfully.")
            else: self.error("Invalid selection.")
        except ValueError: self.error("Invalid input, please enter a valid number.")