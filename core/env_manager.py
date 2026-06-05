import os
import sys
from core.base_manager import BaseManager

class EnvManager(BaseManager):
    def run(self):
        query = sys.argv[2].upper() if len(sys.argv) > 2 else None
        
        if query:
            self.info(f"Searching Environment Variables for: '{query}'")
        else:
            self.info("Displaying all Environment Variables...")
            
        count = 0
        for key, value in sorted(os.environ.items()):
            if query:
                if query in key.upper() or query in value.upper():
                    print(f"  {self.C_GREEN}{key}{self.C_RESET}={value}")
                    count += 1
            else:
                print(f"  {self.C_GREEN}{key}{self.C_RESET}={value}")
                count += 1
        
        self.success(f"Displayed {count} environment variable(s).")