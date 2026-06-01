# core/extract_manager.py
import os
import subprocess

class ExtractManager:
    def __init__(self):
        # Kode warna khusus lokal
        self.C_PINE = "\033[36m"
        self.C_GOLD = "\033[33m"
        self.C_RESET = "\033[0m"
        self.C_BOLD = "\033[1m"

    def _ensure_tool_installed(self, command_check: str, package_name: str):
        """Memastikan tool extractor terinstall, jika tidak ada otomatis diinstall, sayang"""
        check = subprocess.run(f"command -v {command_check}", shell=True, stdout=subprocess.PIPE)
        if check.returncode != 0:
            print(f"📦 Tool '{command_check}' belum terpasang. {self.C_PINE}one otomatis memasangnya untukmu...{self.C_RESET}")
            subprocess.run(["sudo", "apt-get", "install", "-y", package_name])

    def extract(self, file_path: str):
        """Mendeteksi jenis arsip secara dinamis dan mengekstraknya"""
        if not os.path.exists(file_path):
            print(f"❌ File '{file_path}' tidak ditemukan, sayang.")
            return

        file_name = os.path.basename(file_path)
        lower_path = file_path.lower()

        print(f"📦 {self.C_PINE}Mengekstrak arsip: '{file_name}'...{self.C_RESET}")

        try:
            # 1. Format .zip
            if lower_path.endswith(".zip"):
                self._ensure_tool_installed("unzip", "unzip")
                subprocess.run(["unzip", file_path])

            # 2. Format .tar.gz atau .tgz
            elif lower_path.endswith(".tar.gz") or lower_path.endswith(".tgz"):
                subprocess.run(["tar", "-xzvf", file_path])

            # 3. Format .tar.bz2 atau .tbz2
            elif lower_path.endswith(".tar.bz2") or lower_path.endswith(".tbz2"):
                subprocess.run(["tar", "-xjvf", file_path])

            # 4. Format .tar
            elif lower_path.endswith(".tar"):
                subprocess.run(["tar", "-xvf", file_path])

            # 5. Format .rar
            elif lower_path.endswith(".rar"):
                self._ensure_tool_installed("unrar", "unrar-free")
                subprocess.run(["unrar", "x", file_path])

            # 6. Format .7z
            elif lower_path.endswith(".7z"):
                self._ensure_tool_installed("7z", "p7zip-full")
                subprocess.run(["7z", "x", file_path])

            # 7. Format .gz (Single file compression)
            elif lower_path.endswith(".gz") and not lower_path.endswith(".tar.gz"):
                subprocess.run(["gunzip", "-k", file_path])

            else:
                print(f"❌ Format arsip untuk '{file_name}' tidak didukung atau belum terdaftar, sayang.")
                return

            print(f"\n🎉 {self.C_BOLD}File '{file_name}' sukses diekstrak total, sayang!{self.C_RESET}")

        except Exception as e:
            print(f"❌ Terjadi kesalahan saat mengekstrak: {e}")