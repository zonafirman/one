# core/base_manager.py

class BaseManager:
    """
    BaseManager serves as the foundational class for all One-CLI command managers.
    It provides standardized output formatting (colors), logging methods, and
    shared configuration constants to ensure a uniform user experience across the CLI.
    """
    
    # CLI Version
    VERSION = "1.0.0 (Pro Edition)"
    
    def __init__(self):
        # Standard system terminal color palette (Professional)
        # Using ANSI escape codes for cross-platform compatibility where supported.
        self.C_CYAN   = "\033[36m"
        self.C_GREEN  = "\033[32m"
        self.C_YELLOW = "\033[33m"
        self.C_RED    = "\033[31m"
        self.C_RESET  = "\033[0m"
        self.C_BOLD   = "\033[1m"

    def info(self, msg):
        """Prints an informational message in Cyan."""
        print(f"{self.C_CYAN}[INFO]{self.C_RESET} {msg}")

    def success(self, msg):
        """Prints a success message in Green."""
        print(f"{self.C_GREEN}[OK]{self.C_RESET} {msg}")

    def warn(self, msg):
        """Prints a warning message in Yellow."""
        print(f"{self.C_YELLOW}[WARN]{self.C_RESET} {msg}")

    def error(self, msg):
        """Prints an error message in Red."""
        print(f"{self.C_RED}[ERR]{self.C_RESET} {msg}")