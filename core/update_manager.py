import subprocess
from core.base_manager import BaseManager

class UpdateManager(BaseManager):
    def __init__(self):
        super().__init__()

    def run(self):
        self.info("Synchronizing package index files (apt update)...")
        try:
            subprocess.run(["sudo", "apt", "update"], check=True)
            self.success("Package database updated successfully.")
        except subprocess.CalledProcessError:
            self.error("Failed to refresh package repositories. Check for errors above.")
        except Exception as e:
            self.error(f"An unexpected error occurred: {e}")