import os
import sys
import shutil
import subprocess
from core.base_manager import BaseManager

class FileManager(BaseManager):
    def __init__(self):
        super().__init__()

    def run(self):
        if len(sys.argv) < 3:
            self.error("Usage: one file <path_to_delete>")
            self.info("This command permanently deletes a file or directory.")
            return
        
        raw_path = sys.argv[2]
        self.delete_item(raw_path)

    def delete_item(self, raw_path: str):
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