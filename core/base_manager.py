# core/base_manager.py
class BaseManager:
    def __init__(self):
        # Palet warna terminal standar sistem (Professional)
        self.C_CYAN   = "\033[36m"
        self.C_GREEN  = "\033[32m"
        self.C_YELLOW = "\033[33m"
        self.C_RED    = "\033[31m"
        self.C_RESET  = "\033[0m"
        self.C_BOLD   = "\033[1m"

    def info(self, msg):
        print(f"{self.C_CYAN}[INFO]{self.C_RESET} {msg}")

    def success(self, msg):
        print(f"{self.C_GREEN}[OK]{self.C_RESET} {msg}")

    def warn(self, msg):
        print(f"{self.C_YELLOW}[WARN]{self.C_RESET} {msg}")

    def error(self, msg):
        print(f"{self.C_RED}[ERR]{self.C_RESET} {msg}")