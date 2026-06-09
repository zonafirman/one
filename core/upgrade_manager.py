import os
import subprocess
from core.base_manager import BaseManager

class UpgradeManager(BaseManager):
    def __init__(self):
        super().__init__()


    def run(self):
        self.info("Checking for and applying One-CLI updates from the Git repository...")
        
        core_dir = os.path.dirname(os.path.abspath(__file__))
        repo_dir = os.path.dirname(core_dir)
        
        if not os.path.exists(os.path.join(repo_dir, ".git")):
            self.error(f"Project is not a Git repository. Cannot upgrade. (Looked in: {repo_dir})")
            return
        try:
            os.chdir(repo_dir)
            self.info("Fetching latest changes from remote...")
            subprocess.run(["git", "fetch"], check=True, capture_output=True)
            
            self.info("Pulling updates...")
            res = subprocess.run(["git", "pull"], capture_output=True, text=True, check=True)
            
            if "Already up to date." in res.stdout:
                self.success("One-CLI is already up to date.")
            else:
                self.success("One-CLI has been successfully upgraded.")
                print(f"{self.C_CYAN}{res.stdout.strip()}{self.C_RESET}")
                
        except subprocess.CalledProcessError as e:
            self.error("Failed to pull updates. You may have uncommitted changes or network issues.")
            if e.stderr:
                print(f"  {self.C_RED}{e.stderr.strip()}{self.C_RESET}")
        except Exception as e:
            self.error(f"Automatic upgrade failed. Error: {e}")