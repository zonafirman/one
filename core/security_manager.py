import subprocess
import shutil
from core.base_manager import BaseManager

class SecurityManager(BaseManager):
    def run(self):
        self.info("Initiating System Security Audit...")
        
        print(f"\n{self.C_BOLD}{self.C_CYAN}[1] Firewall Status (UFW){self.C_RESET}")
        if shutil.which("ufw"):
            subprocess.run(["sudo", "ufw", "status", "verbose"], check=False)
        else:
            self.warn("UFW is not installed.")

        print(f"\n{self.C_BOLD}{self.C_CYAN}[2] Active Listening Ports{self.C_RESET}")
        if shutil.which("ss"):
            subprocess.run(["sudo", "ss", "-tulnp"], check=False)
        else:
            self.warn("'ss' command not found.")

        print(f"\n{self.C_BOLD}{self.C_CYAN}[3] Failed SSH Login Attempts{self.C_RESET}")
        try:
            res = subprocess.run(["sudo", "journalctl", "-u", "ssh", "--grep", "Failed password", "--no-pager", "-n", "10"], capture_output=True, text=True)
            if res.stdout.strip():
                print(res.stdout)
            else:
                self.success("No recent failed SSH logins detected.")
        except Exception:
            self.warn("Could not check SSH logs. Root privileges might be required.")
            
        self.success("Security audit completed.")