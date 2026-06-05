import subprocess
import sys
import shutil
from core.base_manager import BaseManager

class InfoManager(BaseManager):
    def __init__(self):
        super().__init__()

    def run(self):
        if len(sys.argv) < 3:
            self.error("Usage: one info <package_name>")
            return
        pkg_name = sys.argv[2]
        self.show_info(pkg_name)

    def show_info(self, pkg_name):
        self.info(f"Inspecting package: '{pkg_name}'")
        found = False

        if shutil.which("apt-cache"):
            try:
                res = subprocess.run(["apt-cache", "show", pkg_name], capture_output=True, text=True)
                if res.returncode == 0 and res.stdout.strip():
                    print(f"\n  {self.C_YELLOW}[ APT Repository Details ]{self.C_RESET}")
                    for line in res.stdout.splitlines()[:12]:
                        if any(line.startswith(p) for p in ["Package:", "Version:", "Section:", "Maintainer:", "Description:", "Homepage:"]):
                            print(f"      › {line}")
                    found = True
            except: pass

        if shutil.which("flatpak"):
            try:
                res = subprocess.run(["flatpak", "info", pkg_name], capture_output=True, text=True)
                if res.returncode == 0 and res.stdout.strip():
                    print(f"\n  {self.C_GREEN}[ Flatpak (Flathub) Details ]{self.C_RESET}")
                    print(res.stdout.strip())
                    found = True
            except: pass

        if shutil.which("snap"):
            try:
                res = subprocess.run(["snap", "info", pkg_name], capture_output=True, text=True)
                if res.returncode == 0 and res.stdout.strip():
                    print(f"\n  {self.C_RED}[ Snapcraft Details ]{self.C_RESET}")
                    lines = res.stdout.splitlines()
                    for line in lines[:10]:
                        print(f"      › {line}")
                    found = True
            except: pass

        if not found:
            self.error(f"No information found for '{pkg_name}' in any repository.")
        else:
            self.success("\nPackage inspection complete.")