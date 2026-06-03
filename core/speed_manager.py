# core/speed_manager.py
import subprocess
import shutil

class SpeedManager:
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

    def execute_speedtest(self):
        """Menguji kecepatan Download & Upload internet dengan parsing tangguh"""
        print(f"\n{self.C_BOLD}{self.C_IRIS}🚀 --- One-CLI Smart Internet Speedtest ---{self.C_RESET}\n")

        # Cek ketersediaan perintah speedtest-cli
        if not shutil.which("speedtest-cli") and not shutil.which("speedtest"):
            print(f"  {self.C_GOLD}💡 Paket 'speedtest-cli' belum terpasang di komputermu.{self.C_RESET}")
            print(f"  {self.C_SUBTLE}Kamu bisa memasangnya dengan mengetik:{self.C_RESET} {self.C_FOAM}one install speedtest-cli{self.C_RESET}\n")
            return

        print(f"  {self.C_SUBTLE}Mencari server terbaik dan menguji kecepatan (Mohon tunggu sekitar 10-20 detik, sayang)...{self.C_RESET}\n")
        
        try:
            # Menggunakan subprocess.run untuk mengambil seluruh output teks secara utuh setelah selesai
            result = subprocess.run(["speedtest-cli", "--simple"], capture_output=True, text=True, timeout=45)
            
            if result.returncode != 0:
                print(f"  {self.C_LOVE}❌ Gagal terhubung ke server Speedtest. Periksa jaringanmu, sayang.{self.C_RESET}\n")
                return

            # Pecah output teks menjadi baris-baris
            lines = result.stdout.split("\n")
            
            found_data = False
            for line in lines:
                line_str = line.strip()
                # Cek dengan mengabaikan huruf besar/kecil (case-insensitive) biar lebih aman
                if line_str.lower().startswith("ping:"):
                    val = line_str.split(":", 1)[1].strip()
                    print(f"      › Latensi Jaringan : {self.C_GOLD}{val}{self.C_RESET}")
                    found_data = True
                elif line_str.lower().startswith("download:"):
                    val = line_str.split(":", 1)[1].strip()
                    print(f"      › Kecepatan Unduh  : {self.C_FOAM}{val}{self.C_RESET}")
                    found_data = True
                elif line_str.lower().startswith("upload:"):
                    val = line_str.split(":", 1)[1].strip()
                    print(f"      › Kecepatan Unggah : {self.C_ROSE}{val}{self.C_RESET}")
                    found_data = True

            # Jika output tidak sesuai format "--simple", kita keluarkan output mentahnya agar tidak kosong
            if not found_data and result.stdout.strip():
                print(f"  {self.C_SUBTLE}[ Output Mentah Sistem ]{self.C_RESET}")
                for line in lines:
                    if line.strip():
                        print(f"      › {line.strip()}")

            print(f"\n{self.C_BOLD}{self.C_IRIS}🌸 Pengujian selesai! Internetmu siap dipakai berselancar, sayang!{self.C_RESET}\n")

        except subprocess.TimeoutExpired:
            print(f"  {self.C_LOVE}❌ Waktu pengujian habis (Timeout). Koneksi internetmu terlalu lambat atau terputus.{self.C_RESET}\n")
        except Exception as e:
            print(f"  {self.C_LOVE}❌ Gagal menjalankan uji kecepatan internet: {e}{self.C_RESET}\n")