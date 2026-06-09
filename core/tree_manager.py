import os
import sys
from core.base_manager import BaseManager

class TreeManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.prefix_item = "├── "
        self.prefix_last_item = "└── "
        self.prefix_indent = "│   "
        self.prefix_last_indent = "    "

    def run(self):
        args = sys.argv[2:]
        path = "."
        max_depth = 2  # Batas kedalaman default agar tidak menampilkan seluruh filesystem
        
        for arg in args:
            if arg.isdigit():
                max_depth = int(arg)
            else:
                path = arg
        
        if not os.path.isdir(path):
            self.error(f"Path not found or is not a directory: '{path}'")
            return
        
        abs_path = os.path.abspath(path)
        self.info(f"Displaying directory tree for: {abs_path} (Max Depth: {max_depth})")
        print(f"{self.C_CYAN}{abs_path}{self.C_RESET}")
        self._print_tree(path, "", current_depth=1, max_depth=max_depth)

    def _print_tree(self, directory, prefix, current_depth, max_depth):
        if current_depth > max_depth:
            return
            
        try:
            files = sorted(os.listdir(directory))
            entries = [os.path.join(directory, f) for f in files]
            
            for i, entry in enumerate(entries):
                is_last = i == (len(entries) - 1)
                connector = self.prefix_last_item if is_last else self.prefix_item
                
                if os.path.isdir(entry):
                    print(f"{prefix}{connector}{self.C_BOLD}{self.C_CYAN}{os.path.basename(entry)}{self.C_RESET}")
                    indent = self.prefix_last_indent if is_last else self.prefix_indent
                    self._print_tree(entry, prefix + indent, current_depth + 1, max_depth)
                else:
                    print(f"{prefix}{connector}{os.path.basename(entry)}")
        except PermissionError:
            print(f"{prefix}└── {self.C_RED}[Permission Denied]{self.C_RESET}")