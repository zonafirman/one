import os
import sys
import subprocess
import shutil
from core.base_manager import BaseManager

class ExtractManager(BaseManager):
    def __init__(self):
        super().__init__()

    def _ensure_tool(self, cmd, pkg):
        if not shutil.which(cmd):
            self.warn(f"Utility '{cmd}' not found. Attempting to install '{pkg}'...")
            subprocess.run(["sudo", "apt-get", "install", "-y", pkg], check=True)

    def run(self):
        if len(sys.argv) < 3:
            self.error("Usage: one extract <file_path>")
            return
        file_path = sys.argv[2]

        if not os.path.exists(file_path):
            self.error(f"File not found: '{file_path}'")
            return

        lp = file_path.lower()
        self.info(f"Extracting archive: '{os.path.basename(file_path)}'...")
        try:
            if lp.endswith(".zip"):
                self._ensure_tool("unzip", "unzip")
                subprocess.run(["unzip", file_path], check=True)
            elif lp.endswith(".tar.gz") or lp.endswith(".tgz"):
                subprocess.run(["tar", "-xzvf", file_path], check=True)
            elif lp.endswith(".tar.bz2") or lp.endswith(".tbz2"):
                subprocess.run(["tar", "-xjvf", file_path], check=True)
            elif lp.endswith(".tar"):
                subprocess.run(["tar", "-xvf", file_path], check=True)
            elif lp.endswith(".rar"):
                self._ensure_tool("unrar", "unrar-free")
                subprocess.run(["unrar", "x", file_path], check=True)
            elif lp.endswith(".7z"):
                self._ensure_tool("7z", "p7zip-full")
                subprocess.run(["7z", "x", file_path], check=True)
            else:
                self.error("Unsupported archive format.")
                return
            self.success(f"Archive '{os.path.basename(file_path)}' extracted successfully.")
        except Exception as e:
            self.error(f"Extraction failed: {e}")