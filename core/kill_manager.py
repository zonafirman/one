import subprocess
import sys
import shutil
from core.base_manager import BaseManager

class KillManager(BaseManager):
    def run(self):
        if len(sys.argv) < 3:
            self.error("Usage: one kill <process_name | port_number>")
            self.info("Example: one kill 8080 (kills process on port 8080)")
            self.info("Example: one kill nginx (kills all nginx processes)")
            return
        
        target = sys.argv[2]
        
        if target.isdigit():
            self.info(f"Attempting to kill process on port {target}...")
            if not shutil.which("fuser"):
                self.error("'fuser' command not found. Cannot kill by port. (Run: apt install psmisc)")
                return
            try:
                subprocess.run(["sudo", "fuser", "-k", f"{target}/tcp"], check=True, capture_output=True)
                self.success(f"Successfully killed process on port {target}.")
            except subprocess.CalledProcessError:
                self.error(f"Failed to kill or no process found on port {target}.")
        else:
            self.info(f"Attempting to kill process by name: '{target}'...")
            try:
                subprocess.run(["sudo", "killall", "-9", target], check=True, capture_output=True)
                self.success(f"Successfully killed process(es) named '{target}'.")
            except subprocess.CalledProcessError:
                self.error(f"Failed to kill or no process found with name '{target}'.")