import subprocess
import shutil
from core.base_manager import BaseManager

class SpeedManager(BaseManager):
    def __init__(self):
        super().__init__()

    def run(self):
        self.info("Starting Internet Speed Test...")
        if not shutil.which("speedtest-cli") and not shutil.which("speedtest"):
            self.error("speedtest-cli is not installed. Please install it first.")
            self.info("You can install it using: one install speedtest-cli")
            return
        
        self.info("Testing bandwidth, this may take a minute...")
        try:
            res = subprocess.run(["speedtest-cli", "--simple"], capture_output=True, text=True, timeout=45)
            if res.returncode != 0:
                self.error("Speedtest server failed to respond.")
                return
            for line in res.stdout.split("\n"):
                ls = line.strip().lower()
                if ls.startswith("ping:"): print(f"  {self.C_YELLOW}Latency{self.C_RESET}    : {line.split(':',1)[1].strip()}")
                elif ls.startswith("download:"): print(f"  {self.C_GREEN}Download{self.C_RESET}   : {line.split(':',1)[1].strip()}")
                elif ls.startswith("upload:"): print(f"  {self.C_CYAN}Upload{self.C_RESET}     : {line.split(':',1)[1].strip()}")
            self.success("Speed test completed.")
        except subprocess.TimeoutExpired:
            self.error("Speed test timed out.")
        except Exception as e:
            self.error(f"An unexpected error occurred: {e}")