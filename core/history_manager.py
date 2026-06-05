import os
import sys
from core.base_manager import BaseManager

class HistoryManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.history_file = os.path.expanduser("~/.one_history")

    def run(self):
        args = sys.argv[2:]
        if "--clear" in args:
            self.clear_history()
        else:
            self.show_history()

    def show_history(self):
        self.info(f"Displaying command history from: {self.history_file}")
        if not os.path.exists(self.history_file):
            self.warn("History file not found. No commands have been logged yet.")
            return
        
        try:
            with open(self.history_file, "r") as f:
                history_lines = f.readlines()
            
            if not history_lines:
                self.success("Command history is empty.")
                return

            for i, line in enumerate(history_lines[-100:]): # Show last 100 commands
                parts = line.strip().split(" | ", 1)
                if len(parts) == 2:
                    timestamp, command = parts
                    print(f"  {str(i+1).rjust(4)}  {self.C_YELLOW}{timestamp}{self.C_RESET}   {command}")
        except Exception as e:
            self.error(f"Failed to read history file: {e}")

    def clear_history(self):
        if os.path.exists(self.history_file):
            try:
                os.remove(self.history_file)
                self.success("Command history has been cleared.")
            except Exception as e:
                self.error(f"Failed to clear history file: {e}")
        else:
            self.warn("History file does not exist. Nothing to clear.")