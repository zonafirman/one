import subprocess
import shutil
from core.base_manager import BaseManager

class ListManager(BaseManager):
    def run(self):
        self.info("Listing installed visual applications (Flatpak/Snap)...")
        
        print(f"\n{self.C_BOLD}{self.C_GREEN}[ Flatpak Applications ]{self.C_RESET}")
        if shutil.which("flatpak"):
            try:
                res = subprocess.run(["flatpak", "list", "--app"], capture_output=True, text=True)
                if res.stdout.strip():
                    print(res.stdout)
                else:
                    print("  No Flatpak applications installed.")
            except: pass
        else:
            print("  Flatpak not installed.")
            
        print(f"\n{self.C_BOLD}{self.C_RED}[ Snap Applications ]{self.C_RESET}")
        if shutil.which("snap"):
            try:
                res = subprocess.run(["snap", "list"], capture_output=True, text=True)
                if res.stdout.strip():
                    print(res.stdout)
                else:
                    print("  No Snap applications installed.")
            except: pass
        else:
            print("  Snap not installed.")
            
        self.info("Listing active Systemd Services (Top 10)...")
        if shutil.which("systemctl"):
            try:
                res = subprocess.run(["systemctl", "list-units", "--type=service", "--state=running", "--no-pager"], capture_output=True, text=True)
                lines = res.stdout.splitlines()[1:11]
                for line in lines:
                    print(f"  {self.C_CYAN}{line.strip()}{self.C_RESET}")
            except: pass
        
        self.success("List completed.")