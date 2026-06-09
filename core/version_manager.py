# core/version_manager.py
from core.base_manager import BaseManager

class VersionManager(BaseManager):
    def __init__(self):
        super().__init__()

    def run(self):
        print(f"\n{self.C_CYAN}{self.C_BOLD}One-CLI{self.C_RESET} {self.VERSION}")
        self.success("You are running the latest installed version.")
