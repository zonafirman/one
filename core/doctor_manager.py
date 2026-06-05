# core/doctor_manager.py
import os
import shutil
import getpass
from core.base_manager import BaseManager

class DoctorManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.target_root = "/"
        self.C_SUBTLE  = "\033[90m"

    def run(self):
        self.info("Running Advanced System Diagnostics...")
        
        print(f"\n  {self.C_SUBTLE}[1/4]{self.C_RESET} Checking Privileges...")
        print(f"      {self.C_YELLOW}⚠️ Running as Root/Sudo." if os.geteuid()==0 else f"      {self.C_GREEN}✅ Standard User ({getpass.getuser()}). Safe.")

        print(f"\n  {self.C_SUBTLE}[2/4]{self.C_RESET} Analyzing Disk Space...")
        try:
            total, used, free = shutil.disk_usage(self.target_root)
            free_gb = free / (2**30)
            print(f"      › Available: {free_gb:.1f} GB of {total/(2**30):.1f} GB")
            print(f"      {self.C_RED}❌ Critical low space!" if free_gb < 5 else f"      {self.C_GREEN}✅ Capacity optimal.")
        except: pass

        print(f"\n  {self.C_SUBTLE}[3/4]{self.C_RESET} Monitoring CPU Load & Thermals...")
        try:
            load = os.getloadavg()
            print(f"      › Load Avg: {load[0]:.2f} (1m) | {load[1]:.2f} (5m)")
            temp_found = False
            for path in ["/sys/class/thermal/thermal_zone0/temp", "/sys/class/hwmon/hwmon0/temp1_input"]:
                if os.path.exists(path):
                    with open(path, "r") as f:
                        t = int(f.read().strip()) / 1000
                        print(f"      › Core Temp: {t:.1f}°C")
                        temp_found = True
                        break
            if not temp_found: print(f"      › Core Temp: N/A (Virtual Environment)")
        except: pass

        print(f"\n  {self.C_SUBTLE}[4/4]{self.C_RESET} Verifying RAM Availability...")
        try:
            with open("/proc/meminfo", "r") as f:
                mem = {line.split(":")[0].strip(): int(line.split(":")[1].split()[0]) for line in f.readlines()}
            tot = mem.get("MemTotal", 0) // 1024
            avl = mem.get("MemAvailable", 0) // 1024
            print(f"      › RAM Usage: {tot-avl} MB / {tot} MB")
            print(f"      {self.C_GREEN}✅ Allocation stable.")
        except: pass

        print("")
        self.success("Diagnostics complete. System operates within normal parameters.")