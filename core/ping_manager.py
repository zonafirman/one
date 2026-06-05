import subprocess
import sys
import re
import shutil
from core.base_manager import BaseManager

class PingManager(BaseManager):
    def __init__(self):
        super().__init__()

    def run(self):
        host = sys.argv[2] if len(sys.argv) > 2 else "1.1.1.1"
        self.info(f"Pinging host: {host} (4 packets)")

        if not shutil.which("ping"):
            self.error("Utility 'ping' is not installed.")
            return
        try:
            proc = subprocess.Popen(["ping", "-c", "4", host], stdout=subprocess.PIPE, text=True)
            while True:
                line = proc.stdout.readline()
                if not line and proc.poll() is not None: break
                if "bytes from" in line and "time=" in line:
                    match = re.search(r"time=([\d\.]+)\s*ms", line)
                    if match:
                        ms = float(match.group(1))
                        color = self.C_GREEN if ms < 50 else (self.C_YELLOW if ms < 150 else self.C_RED)
                        print(f"  Reply from {host}: time={color}{ms:.1f}ms{self.C_RESET}")
            proc.wait()
            if proc.returncode == 0:
                self.success(f"Ping to {host} successful.")
            else:
                self.error(f"Ping to {host} failed. Host may be unreachable.")
        except Exception as e:
            self.error(f"Ping execution failed: {e}")