# core/clean_manager.py
import subprocess
import os
import shutil

class CleanManager:
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

    def _get_folder_size(self, path):
        """Fungsi pembantu untuk menghitung ukuran sampah dalam Megabyte (MB)"""
        total_size = 0
        if os.path.exists(path):
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
        return total_size / (1024 * 1024)

    def execute_clean(self):
        """Menjalankan runtutan pembersihan sampah sistem secara interaktif"""
        print(f"\n{self.C_BOLD}{self.C_IRIS}🧹 --- One-CLI Smart System Cleaner ---{self.C_RESET}\n")
        
        # 1. Hitung potensi sampah sebelum dibersihkan (Biar informatif!)
        apt_cache_path = "/var/cache/apt/archives/"
        thumb_cache_path = os.path.expanduser("~/.cache/thumbnails/")
        
        apt_size = self._get_folder_size(apt_cache_path)
        thumb_size = self._get_folder_size(thumb_cache_path)
        
        print(f"  {self.C_SUBTLE}[ Analisis Ruang Sampah Terdeteksi ]{self.C_RESET}")
        print(f"      › Cache Paket Standar (APT) : {apt_size:.1f} MB")
        print(f"      › Cache Gambar (Thumbnails) : {thumb_size:.1f} MB")
        print(f"      › Log Sistem Lama (Journal) : Menunggu optimasi ukuran...")
        print("")

        # Konfirmasi interaktif ke pengguna
        confirm = input(f"  {self.C_GOLD}❓ Apakah kamu ingin melanjutkan pembersihan ini, sayang? (y/n): {self.C_RESET}").lower()
        if confirm != 'y' and confirm != 'ya':
            print(f"\n  {self.C_SUBTLE}🌸 Pembersihan dibatalkan. Kamarmu tetap dibiarkan apa adanya.{self.C_RESET}\n")
            return

        print(f"\n  {self.C_SUBTLE}⚙️  Memulai pembersihan... (Sistem mungkin meminta password root jika dibutuhkan){self.C_RESET}\n")

        # 2. Langkah Pembersihan 1: Cache Gambar User (Gak butuh Sudo, aman dijalankan langsung)
        print(f"  {self.C_SUBTLE}[1/4]{self.C_RESET} Membersihkan Cache Gambar Lokal (~/.cache)...")
        if os.path.exists(thumb_cache_path):
            try:
                shutil.rmtree(thumb_cache_path)
                print(f"      {self.C_FOAM}✅ Berhasil mengosongkan folder thumbnail.{self.C_RESET}")
            except Exception as e:
                print(f"      {self.C_LOVE}❌ Gagal membersihkan thumbnail lokal: {e}{self.C_RESET}")
        else:
            print(f"      {self.C_FOAM}✅ Folder thumbnail sudah bersih.{self.C_RESET}")
        print("")

        # 3. Langkah Pembersihan 2-4: Operasi Sistem (Panggil sudo secara internal lewat subprocess)
        # Trik ini membuat 'one clean' biasa otomatis meminta password sudo dengan aman di terminal!
        tasks = [
            {
                "step": "2/4",
                "desc": "Membersihkan Cache Paket (.deb lama) via APT",
                "cmd": ["sudo", "apt-get", "clean"]
            },
            {
                "step": "3/4",
                "desc": "Menghapus Dependensi Aplikasi Tidak Terpakai (Autoremove)",
                "cmd": ["sudo", "apt-get", "autoremove", "-y"]
            },
            {
                "step": "4/4",
                "desc": "Mengoptimalkan Ukuran Log Sistem (Systemd Journal)",
                "cmd": ["sudo", "journalctl", "--vacuum-size=50M"]
            }
        ]

        for task in tasks:
            print(f"  {self.C_SUBTLE}[{task['step']}]{self.C_RESET} {task['desc']}...")
            try:
                # subprocess.run dengan sudo di dalam array cmd akan memicu prompt password bawaan Linux
                result = subprocess.run(task['cmd'], capture_output=True, text=True, check=True)
                print(f"      {self.C_FOAM}✅ Eksekusi sistem berhasil dijalankan.{self.C_RESET}")
            except subprocess.CalledProcessError as e:
                print(f"      {self.C_LOVE}❌ Gagal mengeksekusi operasi sistem: {e.stderr.strip()}{self.C_RESET}")
            except Exception as e:
                print(f"      {self.C_LOVE}❌ Terjadi eror tak terduga: {e}{self.C_RESET}")
            print("")

        print(f"{self.C_BOLD}{self.C_ROSE}🌸 [ Sukses Bersih-Bersih ] Seluruh sampah telah disapu. Sistem komputermu jadi segar kembali, sayang!{self.C_RESET}\n")

if __name__ == "__main__":
    cleaner = CleanManager()
    cleaner.execute_clean()