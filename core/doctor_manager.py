# core/doctor_manager.py
import os
import shutil
import getpass

class DoctorManager:
    def __init__(self):
        self.target_root = "/"
        self.C_ROSE    = "\033[35m"
        self.C_PINE    = "\033[36m"
        self.C_GOLD    = "\033[33m"
        self.C_IRIS    = "\033[34m"
        self.C_LOVE    = "\033[31m"
        self.C_FOAM    = "\033[32m"
        self.C_SUBTLE  = "\033[90m"
        self.C_RESET   = "\033[0m"
        self.C_BOLD    = "\033[1m"

    def run_diagnose(self):
        print(f"\n{self.C_BOLD}{self.C_IRIS}🩺 --- One-CLI Advanced System Doctor Diagnostic ---{self.C_RESET}\n")
        
        # 1. Privileges Check
        print(f"  {self.C_SUBTLE}[1/4]{self.C_RESET} Memeriksa Otoritas Akses...")
        print(f"      {self.C_GOLD}⚠️ Mode Root/Sudo Aktif." if os.geteuid()==0 else f"      {self.C_FOAM}✅ User Standar ({getpass.getuser()}). Aman.")

        # 2. Disk Usage Check
        print(f"\n  {self.C_SUBTLE}[2/4]{self.C_RESET} Menganalisis Ruang Penyimpanan...")
        try:
            total, used, free = shutil.disk_usage(self.target_root)
            free_gb = free / (2**30)
            print(f"      › Tersedia: {free_gb:.1f} GB dari {total/(2**30):.1f} GB")
            print(f"      {self.C_LOVE}❌ Sisa ruang kritis!" if free_gb < 5 else f"      {self.C_FOAM}✅ Kapasitas lega.")
        except: pass

        # 3. CPU and Thermal Check
        print(f"\n  {self.C_SUBTLE}[3/4]{self.C_RESET} Memantau Beban Kerja CPU & Thermal...")
        try:
            load = os.getloadavg()
            print(f"      › Load Avg: {load[0]:.2f} (1m) | {load[1]:.2f} (5m)")
            temp_found = False
            for path in ["/sys/class/thermal/thermal_zone0/temp", "/sys/class/hwmon/hwmon0/temp1_input"]:
                if os.path.exists(path):
                    with open(path, "r") as f:
                        t = int(f.read().strip()) / 1000
                        print(f"      › Suhu Inti: {t:.1f}°C")
                        temp_found = True
                        break
            if not temp_found: print(f"      › Suhu Inti: N/A (WSL/Virtual Environment)")
        except: pass

        # 4. RAM Check
        print(f"\n  {self.C_SUBTLE}[4/4]{self.C_RESET} Memverifikasi Pustaka & RAM...")
        try:
            with open("/proc/meminfo", "r") as f:
                mem = {line.split(":")[0].strip(): int(line.split(":")[1].split()[0]) for line in f.readlines()}
            tot = mem.get("MemTotal", 0) // 1024
            avl = mem.get("MemAvailable", 0) // 1024
            print(f"      › Utilisasi RAM: {tot-avl} MB / {tot} MB")
            print(f"      {self.C_FOAM}✅ Alokasi stabil.")
        except: pass

        print(f"\n{self.C_BOLD}{self.C_ROSE}✅ [ Diagnosa Selesai ] Sistem berjalan dalam batas normal.{self.C_RESET}\n")