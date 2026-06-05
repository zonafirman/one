# core/network_manager.py
import subprocess
import shutil
from core.base_manager import BaseManager

class NetworkManager(BaseManager):
    def show_listening_ports(self):
        self.info("Scanning active local TCP/UDP ports...")
        if not shutil.which("ss"):
            self.error("Utility 'ss' is not installed.")
            return

        try:
            res = subprocess.run(["sudo", "ss", "-tulnp"], capture_output=True, text=True)
            if res.returncode == 0:
                lines = res.stdout.strip().splitlines()
                if not lines:
                    self.warn("No active ports found.")
                    return
                
                print(f"  {self.C_CYAN}{self.C_BOLD}{'PROTO':<6} | {'LOCAL ADDRESS:PORT':<25} | {'PROCESS / APP'}{self.C_RESET}")
                print("  " + "-"*65)
                
                for line in lines[1:]:
                    parts = line.split()
                    if len(parts) >= 6:
                        proto = parts[0]
                        local_addr = parts[4]
                        process_info = " ".join(parts[6:]) if len(parts) > 6 else "-"
                        process_name = process_info.split('\"')[1] if '\"' in process_info else process_info
                        
                        color = self.C_YELLOW if "tcp" in proto else self.C_CYAN
                        print(f"  {color}{proto:<6}{self.C_RESET} | {local_addr:<25} | {process_name}")
                self.success("Port scanning complete.")
            else:
                self.error("Failed to scan network. Sudo access is required.")
        except Exception as e:
            self.error(f"Network scan error: {e}")