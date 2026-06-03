# core/update_manager.py
import subprocess

class UpdateManager:
    def __init__(self):
        # Warna estetik ala Rosé Pine
        self.C_PINE = "\033[36m"
        self.C_RESET = "\033[0m"

    def check_and_update(self):
        """Fungsi untuk menyegarkan indeks paket repositori sistem Linux, sayang"""
        print(f"🔄 {self.C_PINE}Menyegarkan daftar paket repositori sistem (apt update)...{self.C_RESET}\n")
        try:
            # Mengeksekusi perintah apt update bawaan Linux secara langsung
            subprocess.run(["sudo", "apt", "update"], check=True)
            print(f"\n🎉 {self.C_PINE}Daftar paket berhasil diperbarui, sayang! Sistem siap menginstal aplikasi terbaru.{self.C_RESET}")
        except subprocess.CalledProcessError:
            print(f"\n❌ Gagal memperbarui daftar paket repositori.")