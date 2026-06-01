# core/fetch_manager.py
import os
import platform
import subprocess
import getpass

class FetchManager:
    def __init__(self):
        # Definisikan Palet Warna Rosé Pine (Estetik Modern)
        self.C_PINE = "\033[36m"     # Teal / Pine
        self.C_ROSE = "\033[35m"     # Rose / Magenta
        self.C_GOLD = "\033[33m"     # Gold / Yellow
        self.C_IRIS = "\033[34m"     # Iris / Blue
        self.C_TEXT = "\033[37m"     # Muted Text
        self.C_RESET = "\033[0m"

    def _get_os_name(self):
        """Mengambil nama OS secara rapi dari os-release"""
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="):
                        return line.split("=")[1].strip().strip('"')
        except:
            return platform.system()

    def _get_uptime(self):
        """Mengambil info berapa lama komputer sudah menyala"""
        try:
            with open("/proc/uptime", "r") as f:
                uptime_seconds = float(f.readline().split()[0])
                hours = int(uptime_seconds // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                if hours > 0:
                    return f"{hours} jam, {minutes} menit"
                return f"{minutes} menit"
        except:
            return "Tidak diketahui"

    def _get_memory(self):
        """Mengambil statistik penggunaan RAM komputer"""
        try:
            with open("/proc/meminfo", "r") as f:
                lines = f.readlines()
                mem_total = int(lines[0].split()[1]) // 1024  # Convert ke MB
                mem_free = int(lines[1].split()[1]) // 1024
                # Estimasi RAM yang terpakai
                mem_cached = int(lines[4].split()[1]) // 1024
                mem_buffers = int(lines[3].split()[1]) // 1024
                mem_used = mem_total - mem_free - mem_cached - mem_buffers
                return f"{mem_used} MB / {mem_total} MB"
        except:
            return "Tidak diketahui"

    def _get_cpu_model(self):
        """Mengambil nama prosesor/CPU komputer"""
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        except:
            return platform.processor()

    def show_fetch(self):
        """Menampilkan output spesifikasi sistem ala Rosé Pine kustom, sayang"""
        # Ambil semua data sistem aktif
        username = getpass.getuser()
        hostname = platform.node()
        os_name = self._get_os_name()
        kernel = platform.release()
        uptime = self._get_uptime()
        cpu = self._get_cpu_model()
        ram = self._get_memory()
        
        # Deteksi otomatis Desktop Environment (DE)
        de = os.environ.get("XDG_CURRENT_DESKTOP", "Unknown DE")

        # Struktur Logo ASCII Minimalis Kustom berbentuk angka "1" (One-CLI)
        logo = [
            f"  {self.C_ROSE}◼◼◼◼{self.C_RESET}      ",
            f"    {self.C_ROSE}◼◼{self.C_RESET}      ",
            f"    {self.C_ROSE}◼◼{self.C_RESET}      ",
            f"    {self.C_ROSE}◼◼{self.C_RESET}      ",
            f"    {self.C_ROSE}◼◼{self.C_RESET}      ",
            f"  {self.C_ROSE}◼◼◼◼◼◼{self.C_RESET}    "
        ]

        # Struktur Informasi Sistem di sebelah kanan logo
        info = [
            f"{self.C_GOLD}{username}{self.C_TEXT}@{self.C_PINE}{hostname}{self.C_RESET}",
            f"{self.C_TEXT}---------------------------{self.C_RESET}",
            f"{self.C_PINE}OS      {self.C_RESET}: {os_name}",
            f"{self.C_PINE}Kernel  {self.C_RESET}: {kernel}",
            f"{self.C_PINE}Uptime  {self.C_RESET}: {uptime}",
            f"{self.C_PINE}Desktop {self.C_RESET}: {de}",
            f"{self.C_PINE}CPU     {self.C_RESET}: {cpu}",
            f"{self.C_PINE}Memory  {self.C_RESET}: {ram}"
        ]

        # Cetak penggabungan logo dan info secara horizontal dan presisi
        print("")
        max_lines = max(len(logo), len(info))
        for i in range(max_lines):
            left = logo[i] if i < len(logo) else "            "
            right = info[i] if i < len(info) else ""
            print(f"{left}  {right}")
        print("")