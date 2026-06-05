import os
import subprocess
from core.base_manager import BaseManager

class UpgradeManager(BaseManager):
    def __init__(self):
        super().__init__()

    def run(self):
        self.info("Checking for and applying One-CLI updates from the Git repository...")
        repo_dir = os.path.expanduser("~/one")
        if not os.path.exists(os.path.join(repo_dir, ".git")):
            self.error("Project is not a Git repository. Cannot upgrade.")
            return
        try:
            os.chdir(repo_dir)
            subprocess.run(["git", "fetch"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            sc = subprocess.run(["git", "status", "-sb"], capture_output=True, text=True, check=True)
            if "behind" in sc.stdout:
                self.warn("New version found. Pulling latest changes...")
                subprocess.run(["git", "pull"], check=True)
                self.success("One-CLI has been successfully upgraded.")
            else:
                self.success("One-CLI is already up to date.")
        except Exception as e:
            self.error(f"Automatic upgrade failed. Please check your Git connection and configuration. Error: {e}")