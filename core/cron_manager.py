import subprocess
import getpass
from core.base_manager import BaseManager

class CronManager(BaseManager):
    def run(self):
        user = getpass.getuser()
        self.info(f"Retrieving active Cron Jobs for user: {user}")
        try:
            res = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
            if res.returncode == 0 and res.stdout.strip():
                print(f"\n{self.C_YELLOW}--- User Cron Jobs ---{self.C_RESET}")
                for line in res.stdout.splitlines():
                    if not line.strip().startswith("#") and line.strip():
                        print(f"  {self.C_GREEN}⏱️  {line.strip()}{self.C_RESET}")
            else:
                self.success(f"No active cron jobs found for user '{user}'.")
        except Exception:
            self.error("Could not fetch cron jobs.")

        print(f"\n{self.C_CYAN}Note: System-wide cron jobs are located in /etc/crontab and /etc/cron.d/{self.C_RESET}")