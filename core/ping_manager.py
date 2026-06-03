# core/ping_manager.py
import subprocess
import re
import shutil

class PingManager:
    def __init__(self):
        # 🌸 Palet Warna Rosé Pine Asli
        self.C_ROSE    = "\033[38;2;235;188;186m"
        self.C_PINE    = "\033[38;2;49;116;143m"
        self.C_GOLD    = "\033[38;2;246;193;119m"
        self.C_IRIS    = "\033[38;2;196;167;231m"
        self.C_LOVE    = "\033[38;2;235;111;145m"
        self.C_FOAM    = "\033[38;2;156;207;216m"
        self.C_SUBTLE  = "\033[38;2;144;140;170m"
        self.C_RESET   = "\033[0m"
        self.C_BOLD    = "\033[1m"

    def execute_ping(self, host="1.1.1.1"):
        """Memeriksa kualitas koneksi internet dan latensi latency"""
        print(f"\n{self.C_BOLD}{self.C_IRIS}🌐 --- One-CLI Network Latency Checker ---{self.C_RESET}\n")
        print(f"  {self.C_SUBTLE}Menghubungi server aman ({host})...{self.C_RESET}")

        if not shutil.which("ping"):
            print(f"  {self.C_LOVE}❌ Perintah 'ping' tidak ditemukan di sistem Linux kamu, sayang.{self.C_RESET}\n")
            return

        try:
            # Melakukan ping sebanyak 4 kali
            cmd = ["ping", "-c", "4", host]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Membaca output secara interaktif baris demi baris biar kelihatan hidup
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if "time=" in line:
                    # Ambil informasi waktu ms dari baris ping
                    match = re.search(r"time=([\d\.]+)\s*ms", line)
                    if match:
                        ms = float(match.group(1))
                        # Beri warna sesuai tingkat kecepatan ms
                        color = self.C_FOAM if ms < 50 else (self.C_GOLD if ms < 150 else self.C_LOVE)
                        print(f"      › Respon diterima: waktu = {color}{ms:.1f} ms{self.C_RESET}")

            process.wait()
            if process.returncode != 0:
                print(f"\n  {self.C_LOVE}❌ Koneksi gagal. Kamu sedang offline atau server tidak merespon, sayang.{self.C_RESET}\n")
                return

            print(f"\n  {self.C_BOLD}{self.C_ROSE}🌸 Pengecekan selesai! Jaringanmu terpantau stabil.{self.C_RESET}\n")

        except Exception as e:
            print(f"  {self.C_LOVE}❌ Terjadi kesalahan saat menjalankan ping: {e}{self.C_RESET}\n")