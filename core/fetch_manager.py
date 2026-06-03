# core/fetch_manager.py
import os
import platform
import subprocess
import getpass
import shutil

class FetchManager:
    def __init__(self):
        # 🌸 Palet Warna Rosé Pine Asli (True Color ANSI)
        self.C_ROSE    = "\033[38;2;235;188;186m" # Mawar lembut
        self.C_PINE    = "\033[38;2;49;116;143m"  # Hijau pinus teduh
        self.C_GOLD    = "\033[38;2;246;193;119m" # Emas hangat
        self.C_IRIS    = "\033[38;2;196;167;231m" # Ungu iris
        self.C_LOVE    = "\033[38;2;235;111;145m" # Merah cinta
        self.C_SUBTLE  = "\033[38;2;144;140;170m" # Abu-abu elegan
        self.C_FOAM    = "\033[38;2;156;207;216m" # Biru busa laut
        self.C_RESET   = "\033[0m"
        self.C_BOLD    = "\033[1m"

    def _get_shell(self):
        return os.environ.get("SHELL", "unknown").split("/")[-1]

    def _get_uptime(self):
        try:
            with open("/proc/uptime", "r") as f:
                uptime_seconds = float(f.readline().split()[0])
                hours = int(uptime_seconds // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                if hours > 0:
                    return f"{hours} jam, {minutes} menit"
                return f"{minutes} menit"
        except:
            return "unknown"

    def _get_ram_info(self):
        try:
            with open("/proc/meminfo", "r") as f:
                lines = f.readlines()
                total = int(lines[0].split()[1])
                available = int(lines[2].split()[1])
                used = total - available
                percent = int((used / total) * 100)
                return f"{used // 1024} MB / {total // 1024} MB ({percent}%)"
        except:
            return "unknown"

    def _get_cpu_info(self):
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip().replace("(R)", "").replace("(TM)", "")
        except:
            return "Unknown Processor"

    def _get_gpu_info(self):
        try:
            # Mengintip GPU via lshw atau lspci secara aman
            out = subprocess.check_output("lspci | grep -Ei 'vga|3d'", shell=True, text=True)
            if "NVIDIA" in out:
                return "NVIDIA GeForce Graphics"
            elif "Intel" in out:
                return "Intel Integrated Graphics"
            elif "AMD" in out:
                return "AMD Radeon Graphics"
            return out.split(":")[2].strip()
        except:
            return "Standard Display Adapter"

    def _get_disk_info(self):
        try:
            total, used, free = shutil.disk_usage("/")
            total_gb = total // (2**30)
            used_gb = used // (2**30)
            percent = int((used / total) * 100)
            return f"{used_gb} GB / {total_gb} GB ({percent}%)"
        except:
            return "unknown"

    def _get_resolution(self):
        try:
            # Mendeteksi resolusi layar di DE lokal
            out = subprocess.check_output("xrandr | grep '*' | awk '{print $1}'", shell=True, text=True)
            return out.strip().split('\n')[0]
        except:
            return "1920x1080 (Default)"

    def _get_ip_address(self):
        try:
            # Mengambil IP lokal utama yang sedang aktif
            out = subprocess.check_output("hostname -I | awk '{print $1}'", shell=True, text=True)
            return out.strip()
        except:
            return "127.0.0.1"

    def show_fetch(self):
        username = getpass.getuser()
        hostname = platform.node()
        
        os_distro = "Ubuntu Linux"
        try:
            os_distro = subprocess.check_output(["lsb_release", "-sd"], text=True).strip().replace('"', '')
        except:
            pass

        # Mengumpulkan info lengkap ala Zorin
        kernel = platform.release()
        uptime = self._get_uptime()
        shell = self._get_shell()
        de = os.environ.get("XDG_CURRENT_DESKTOP", "GNOME / KDE")
        wm = os.environ.get("XDG_DATA_DIRS", "").split("/")[-1] or "Window Manager"
        cpu = self._get_cpu_info()
        gpu = self._get_gpu_info()
        ram = self._get_ram_info()
        disk = self._get_disk_info()
        res = self._get_resolution()
        ip = self._get_ip_address()

        # 🪐 LOGO KUSTOM: Lingkaran dengan Blank Space membentuk angka 1
        # Menggunakan warna Iris (Ungu lembut) agar menyatu dengan background terminal gelap
        logo = [
            f"      {self.C_IRIS}oo00000000oo{self.C_RESET}",
            f"    {self.C_IRIS}o00000000000000o{self.C_RESET}",
            f"   {self.C_IRIS}00000000  00000000{self.C_RESET}",
            f"  {self.C_IRIS}000000000  000000000{self.C_RESET}",
            f"  {self.C_IRIS}000000000  000000000{self.C_RESET}",
            f"  {self.C_IRIS}000000000  000000000{self.C_RESET}",
            f"  {self.C_IRIS}000000000  000000000{self.C_RESET}",
            f"   {self.C_IRIS}00000000  00000000{self.C_RESET}",
            f"    {self.C_IRIS}o00000000000000o{self.C_RESET}",
            f"      {self.C_IRIS}oo00000000oo{self.C_RESET}"
        ]

        # 📊 INFORMASI SISTEM (Sebelah Kanan)
        info = [
            f"{self.C_BOLD}{self.C_ROSE}{username}{self.C_RESET}{self.C_BOLD}{self.C_SUBTLE}@{self.C_RESET}{self.C_BOLD}{self.C_GOLD}{hostname}{self.C_RESET}",
            f"{self.C_SUBTLE}" + "─" * (len(username) + len(hostname) + 1) + f"{self.C_RESET}",
            f"{self.C_FOAM}󰻀  OS         {self.C_SUBTLE}› {self.C_RESET}{os_distro}",
            f"{self.C_FOAM}󰻠  Kernel     {self.C_SUBTLE}› {self.C_RESET}{kernel}",
            f"{self.C_FOAM}󰅐  Uptime     {self.C_SUBTLE}› {self.C_RESET}{uptime}",
            f"{self.C_FOAM}󰞷  Shell      {self.C_SUBTLE}› {self.C_GOLD}{shell}{self.C_RESET}",
            f"{self.C_FOAM}󰍹  Resolution {self.C_SUBTLE}› {self.C_RESET}{res}",
            f"{self.C_FOAM}󰨇  DE         {self.C_SUBTLE}› {self.C_RESET}{de}",
            f"{self.C_FOAM}󰍛  CPU        {self.C_SUBTLE}› {self.C_RESET}{cpu}",
            f"{self.C_FOAM}󰢚  GPU        {self.C_SUBTLE}› {self.C_RESET}{gpu}",
            f"{self.C_FOAM}󰍛  Memory     {self.C_SUBTLE}› {self.C_PINE}{ram}{self.C_RESET}",
            f"{self.C_FOAM}󰋊  Disk (/)   {self.C_SUBTLE}› {self.C_RESET}{disk}",
            f"{self.C_FOAM}󰩟  Local IP   {self.C_SUBTLE}› {self.C_RESET}{ip}",
            f"",
            f"    {self.C_LOVE}██ {self.C_ROSE}██ {self.C_GOLD}██ {self.C_PINE}██ {self.C_IRIS}██ {self.C_FOAM}██ {self.C_SUBTLE}██{self.C_RESET}"
        ]

        # --- JURUS MENGGABUNGKAN LOGO & INFO (SIDE-BY-SIDE) ---
        print("") # Spasi atas
        max_lines = max(len(logo), len(info))
        for i in range(max_lines):
            left = logo[i] if i < len(logo) else " " * 28
            right = info[i] if i < len(info) else ""
            # Sesuaikan padding agar jarak antara logo bulat dan info pas di mata
            print(f" {left}   {right}")
        print("") # Spasi bawah

if __name__ == "__main__":
    fetch = FetchManager()
    fetch.show_fetch()