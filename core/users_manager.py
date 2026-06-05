import subprocess
from core.base_manager import BaseManager

class UsersManager(BaseManager):
    def run(self):
        self.info("Auditing System Users and Active Sessions...")
        
        print(f"\n{self.C_BOLD}{self.C_CYAN}[ Active Sessions (w) ]{self.C_RESET}")
        try:
            subprocess.run(["w"], check=True)
        except Exception:
            self.warn("Could not retrieve active sessions.")

        print(f"\n{self.C_BOLD}{self.C_CYAN}[ Recent Logins (last) ]{self.C_RESET}")
        try:
            subprocess.run(["last", "-a", "-n", "5"], check=True)
        except Exception:
            self.warn("Could not retrieve recent logins.")