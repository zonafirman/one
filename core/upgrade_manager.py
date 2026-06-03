# core/upgrade_manager.py
import os
import subprocess

class UpgradeManager:
    def __init__(self):
        # Warna estetik ala Rosé Pine
        self.C_PINE = "\033[36m"
        self.C_GOLD = "\033[33m"
        self.C_RESET = "\033[0m"

    def pull_latest_code(self):
        """Menarik pembaruan kode terbaru dari Git repositori secara otomatis"""
        print(f"🔄 {self.C_PINE}Memeriksa pembaruan core sistem One-CLI...{self.C_RESET}")
        
        # Lokasi instalasi universal proyek utama
        repo_dir = os.path.expanduser("~/rli-cli")
        
        # Pastikan folder tersebut terhubung ke Git
        if not os.path.exists(os.path.join(repo_dir, ".git")):
            print(f"❌ {repo_dir} bukan merupakan repositori Git, sayang.")
            print(f"💡 Solusi: Pastikan proyek ini dikloning via 'git clone' agar bisa di-upgrade otomatis.")
            return

        try:
            # Berpindah ke folder utama di latar belakang
            os.chdir(repo_dir)
            
            # Ambil informasi berkas terbaru dari GitHub/GitLab kamu
            subprocess.run(["git", "fetch"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Cek apakah kode di lokal tertinggal dari server
            status_check = subprocess.run(
                ["git", "status", "-sb"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            if "behind" in status_check.stdout:
                print(f"✨ {self.C_GOLD}Pembaruan fitur baru ditemukan!{self.C_RESET}")
                print("📥 Sedang mengunduh dan menyelaraskan modul baru...")
                
                # Eksekusi penarikan file kode baru
                pull_result = subprocess.run(["git", "pull"], capture_output=True, text=True, check=True)
                print(pull_result.stdout)
                
                print(f"🎉 {self.C_GOLD}One-CLI berhasil di-upgrade ke versi terbaru, sayang!{self.C_RESET}")
                print(f"💡 Semua fitur baru siap digunakan langsung.")
            else:
                print(f"✅ One-CLI sudah berada di versi paling mutakhir, sayang! Tidak ada perubahan.")
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Gagal melakukan upgrade otomatis. Pastikan koneksi internet aman atau tidak ada konflik kode lokal.")