import sys
import subprocess
import shutil
import os
from core.base_manager import BaseManager

class RemoveManager(BaseManager):
    def run(self):
        args = sys.argv[2:]
        if not args:
            self.error("Usage: one remove [-d] <target>")
            return
            
        if args[0] == "-d":
            if len(args) < 2:
                self.error("Usage: one remove -d <path_to_delete>")
                return
            target = args[1]
            self.remove_file(target)
            return
            
        target = args[0]
        self.smart_remove(target)
        
    def remove_file(self, raw_path: str):
        target = os.path.abspath(raw_path)
        name = os.path.basename(target)
        if not os.path.exists(target):
            self.error(f"Target not found: '{name}'")
            return

        if os.path.isdir(target):
            self.info(f"Deleting directory and its contents: '{name}'...")
            try:
                shutil.rmtree(target)
                self.success(f"Directory '{name}' successfully deleted.")
            except PermissionError:
                self.warn("Permission denied. Escalating with sudo...")
                subprocess.run(["sudo", "rm", "-rf", target], check=True)
                self.success(f"Directory '{name}' successfully deleted with root privileges.")
        else:
            self.info(f"Deleting file: '{name}'...")
            try:
                os.remove(target)
                self.success(f"File '{name}' successfully deleted.")
            except PermissionError:
                self.warn("Permission denied. Escalating with sudo...")
                subprocess.run(["sudo", "rm", "-f", target], check=True)
                self.success(f"File '{name}' successfully deleted with root privileges.")

    def smart_remove(self, pkg_name):
        self.info(f"Attempting to remove '{pkg_name}'...")
        removed = False
        
        if shutil.which("apt-get"):
            try:
                res = subprocess.run(["dpkg", "-s", pkg_name], capture_output=True, text=True)
                if "Status: install ok installed" in res.stdout:
                    self.info(f"Found '{pkg_name}' in APT. Removing...")
                    subprocess.run(["sudo", "apt-get", "remove", "-y", pkg_name], check=True)
                    subprocess.run(["sudo", "apt-get", "autoremove", "-y"], capture_output=True)
                    self.success(f"Removed '{pkg_name}' from APT.")
                    removed = True
            except: pass
            
        if shutil.which("snap") and not removed:
            try:
                res = subprocess.run(["snap", "list"], capture_output=True, text=True)
                if pkg_name in [line.split()[0] for line in res.stdout.splitlines()[1:]]:
                    self.info(f"Found '{pkg_name}' in Snap. Removing...")
                    subprocess.run(["sudo", "snap", "remove", pkg_name], check=True)
                    self.success(f"Removed '{pkg_name}' from Snap.")
                    removed = True
            except: pass

        if shutil.which("flatpak") and not removed:
            try:
                res = subprocess.run(["flatpak", "list", "--app", "--columns=application"], capture_output=True, text=True)
                if pkg_name in res.stdout:
                    self.info(f"Found '{pkg_name}' in Flatpak. Removing...")
                    subprocess.run(["flatpak", "uninstall", "-y", pkg_name], check=True)
                    self.success(f"Removed '{pkg_name}' from Flatpak.")
                    removed = True
            except: pass
            
        if not removed:
            self.error(f"Could not find package '{pkg_name}' installed via APT, Flatpak, or Snap.")