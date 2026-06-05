# core/log_manager.py
import subprocess
from core.base_manager import BaseManager

class LogManager(BaseManager):
    def audit(self):
        self.info("Auditing recent system kernel errors (journalctl)...")
        try:
            subprocess.run(["sudo", "journalctl", "-p", "3", "-xb", "-n", "15", "--no-pager"], check=True)
            self.success("System log audit completed.")
        except Exception:
            self.error("Failed to read system journal. Root privileges may be required.")