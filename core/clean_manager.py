# core/clean_manager.py
import subprocess
import os
import shutil

class CleanManager:
    def __init__(self):
        self.C_ROSE    = "\033[35m"
        self.C_PINE    = "\033[36m"
        self.C_GOLD    = "\033[33m"
        self.C_IRIS    = "\033[34m"
        self.C_LOVE    = "\033[31m"
        self.C_FOAM    = "\033[32m"
        self.C_SUBTLE  = "\033[90m"
        self.C_RESET   = "\033[0m"
        self.C_BOLD    = "\033[1m"

    def _get_folder_size(self, path):
        total = 0
        if os.path.exists(path):
            for dirpath, _, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp): total += os.path.getsize(fp)
        return total / (1024 * 1024)

    def execute_clean(self, deep=False):
        print(f"\n{self.C_BOLD}{self.C_IRIS}🧹 --- One-CLI Smart System Cleaner ---{self.C_RESET}\n")
        apt_cache = "/var/cache/apt/archives/"
        thumbs = os.path.expanduser("~/.cache/thumbnails/")
        
        print(f"  {self.C_SUBTLE}[ Analisis Ruang Sampah Terdeteksi ]{self.C_RESET}")
        print(f"      › Cache Paket Standar (APT) : {self._get_folder_size(apt_cache):.1f} MB")
        print(f"      › Cache Gambar (Thumbnails) : {self._get_folder_size(thumbs):.1f} MB")
        if deep: print(f"      › Log Sistem (Journal Mode) : Deep vacuum diaktifkan (Maks 50M).")
        print("")

        if input(f"  {self.C_GOLD}❓ Lanjutkan pembersihan? (y/n): {self.C_RESET}").lower() != 'y':
            return

        print(f"\n  {self.C_SUBTLE}⚙️  Memulai pembersihan sistem...{self.C_RESET}\n")
        if os.path.exists(thumbs):
            try:
                shutil.rmtree(thumbs)
                print(f"      {self.C_FOAM}✅ Berhasil membersihkan cache thumbnail.{self.C_RESET}")
            except: pass

        tasks = [
            {"desc": "Cache paket (.deb usang)", "cmd": ["sudo", "apt-get", "clean"]},
            {"desc": "Dependensi yatim (Autoremove)", "cmd": ["sudo", "apt-get", "autoremove", "-y"]}
        ]
        if deep:
            tasks.append({"desc": "Mengoptimalkan Log Sistem (Journalctl)", "cmd": ["sudo", "journalctl", "--vacuum-size=50M"]})

        for t in tasks:
            print(f"  ⚡ {t['desc']}...")
            try:
                subprocess.run(t['cmd'], capture_output=True, check=True)
                print(f"      {self.C_FOAM}✅ Berhasil mengeksekusi.{self.C_RESET}")
            except: print(f"      {self.C_LOVE}❌ Gagal dijalankan.{self.C_RESET}")
        print(f"\n{self.C_BOLD}{self.C_ROSE}🌸 Pembersihan sistem berhasil diselesaikan.{self.C_RESET}\n")