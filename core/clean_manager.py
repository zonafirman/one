# core/clean_manager.py
import subprocess
import os
import sys
import shutil
from core.base_manager import BaseManager

class CleanManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.C_SUBTLE  = "\033[90m"

    def _get_folder_size(self, path):
        total = 0
        if os.path.exists(path):
            for dirpath, _, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp): total += os.path.getsize(fp)
        return total / (1024 * 1024)

    def run(self):
        deep = "--all" in sys.argv
        self.info("Initiating Smart System Cleaner...")
        apt_cache = "/var/cache/apt/archives/"
        thumbs = os.path.expanduser("~/.cache/thumbnails/")
        
        print(f"\n  {self.C_SUBTLE}[ Space Analysis ]{self.C_RESET}")
        print(f"      › APT Package Cache : {self._get_folder_size(apt_cache):.1f} MB")
        print(f"      › Local Thumbnails  : {self._get_folder_size(thumbs):.1f} MB")
        if deep: print(f"      › System Logs       : Deep vacuum enabled (Cap at 50M).")
        print("")

        if input(f"  {self.C_YELLOW}❓ Proceed with cleanup? (y/n): {self.C_RESET}").lower() != 'y':
            return

        print(f"\n  {self.C_SUBTLE}⚙️  Cleaning system...{self.C_RESET}\n")
        if os.path.exists(thumbs):
            try:
                shutil.rmtree(thumbs)
                print(f"      {self.C_GREEN}✅ Thumbnails cleared.{self.C_RESET}")
            except: pass

        tasks = [
            {"desc": "APT Cache (.deb archives)", "cmd": ["sudo", "apt-get", "clean"]},
            {"desc": "Orphaned Dependencies", "cmd": ["sudo", "apt-get", "autoremove", "-y"]}
        ]
        if deep:
            tasks.append({"desc": "Optimizing System Logs (Journalctl)", "cmd": ["sudo", "journalctl", "--vacuum-size=50M"]})

        for t in tasks:
            print(f"  ⚡ {t['desc']}...")
            try:
                subprocess.run(t['cmd'], capture_output=True, check=True)
                print(f"      {self.C_GREEN}✅ Success.{self.C_RESET}")
            except: print(f"      {self.C_RED}❌ Failed to execute.{self.C_RESET}")
        self.success("System cleanup completed successfully.")