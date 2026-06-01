# core/package_manager.py
import subprocess
import os
import sys
import glob

# Mengimpor modul internal core
from core.help_manager import HelpManager
from core.package_utils import PackageUtils
from core.system_manager import SystemManager
from core.extract_manager import ExtractManager
from core.file_manager import FileManager
from core.update_manager import UpdateManager

class PackageManager:
    def __init__(self):
        self.system_apps_path = "/usr/share/applications/*.desktop"
        self.user_apps_path = os.path.expanduser("~/.local/share/applications/*.desktop")
        
        # Inisialisasi helper dan utils
        self.helper = HelpManager()
        self.utils = PackageUtils()
        self.system_monitor = SystemManager()
        self.extractor = ExtractManager()
        self.file_handler = FileManager()
        self.update_manager = UpdateManager()
        
        # Kode warna khusus untuk tampilan lokal
        self.C_PINE = "\033[36m"
        self.C_GOLD = "\033[33m"
        self.C_RESET = "\033[0m"
        self.C_BOLD = "\033[1m"

    def get_all_installed_apps(self):
        """Mendeteksi semua aplikasi GUI/Interaktif berbasis file .desktop"""
        apps = {}
        desktop_files = glob.glob(self.system_apps_path) + glob.glob(self.user_apps_path)
        
        for file_path in desktop_files:
            try:
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read()
                    name, exec_path, app_type = None, None, "Manual/External"
                    
                    if "X-Flatpak" in content:
                        app_type = "Flatpak"
                    elif "snap/" in content or "/snap/bin" in content:
                        app_type = "Snap Store"
                    elif "/usr/bin/" in content or "/usr/games/" in content:
                        app_type = "APT (Native Debian/Ubuntu)"
                    
                    for line in content.splitlines():
                        if line.startswith("Name="):
                            name = line.split("=", 1)[1].strip()
                        elif line.startswith("Exec="):
                            exec_path = line.split("=", 1)[1].strip().split()[0]
                        if name and exec_path:
                            break
                    
                    if name:
                        pkg_id = os.path.basename(file_path).replace(".desktop", "")
                        apps[pkg_id] = {
                            "name": name,
                            "type": app_type,
                            "exec": exec_path,
                            "desktop_file": file_path
                        }
            except Exception:
                continue
        return apps

    def get_systemd_services(self):
        """Mendeteksi layanan/daemons latar belakang yang aktif di sistem"""
        services = []
        try:
            # Memanggil systemctl untuk list semua service tipe @service yang loaded
            result = subprocess.run(
                ["systemctl", "list-units", "--type=service", "--state=active", "--no-legend"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 1:
                    service_name = parts[0]
                    # Bersihkan ekstensi '.service' agar tampilannya cantik
                    service_id = service_name.replace(".service", "")
                    
                    # Ambil deskripsi singkat layanannya jika ada
                    description = " ".join(parts[4:]) if len(parts) > 4 else "Layanan latar belakang"
                    services.append(f"🛠️  {service_id} {self.C_GOLD}({description}){self.C_RESET}")
        except Exception:
            # Fallback jika dijalankan di lingkungan WSL lama yang tidak pakai systemd
            if os.path.exists("/etc/init.d"):
                for path in glob.glob("/etc/init.d/*"):
                    service_id = os.path.basename(path)
                    if service_id not in ["README", "skeleton"]:
                        services.append(f"🛠️  {service_id} {self.C_GOLD}(SysVinit Service){self.C_RESET}")
        return services

    def smart_list(self):
        print(f"{self.C_PINE}============== ALL APPS & SERVICES DETECTED BY ONE =============={self.C_RESET}\n")
        
        # 1. Tampilkan Aplikasi Visual (GUI / Interactive)
        all_apps = self.get_all_installed_apps()
        categorized = {"APT (Native Debian/Ubuntu)": [], "Snap Store": [], "Flatpak": [], "Manual/External": []}
        
        for pkg_id, info in all_apps.items():
            categorized[info["type"]].append(f"📌 {info['name']} {self.C_GOLD}({pkg_id}){self.C_RESET}")
            
        for app_type, app_list in categorized.items():
            if app_list:
                icon = "📦" if "APT" in app_type else "🛍️" if "Snap" in app_type else "🚀" if "Flatpak" in app_type else "⭐"
                print(f"{icon} {self.C_BOLD}{app_type}{self.C_RESET}:")
                sorted_list = sorted(app_list)
                for i, app in enumerate(sorted_list):
                    if i == len(sorted_list) - 1:
                        print(f"  └─ {app}")
                    else:
                        print(f"  ├─ {app}")
                print()

        # 2. Tampilkan Layanan Latar Belakang (Services/Daemons)
        services_list = self.get_systemd_services()
        if services_list:
            print(f"⚙️  {self.C_BOLD}System Services & Daemons (Latar Belakang){self.C_RESET}:")
            sorted_services = sorted(services_list)
            for i, svc in enumerate(sorted_services):
                if i == len(sorted_services) - 1:
                    print(f"  └─ {svc}")
                else:
                    print(f"  ├─ {svc}")
            print()
                
        print(f"{self.C_PINE}=================================================================={self.C_RESET}")

    def smart_remove(self, package_id: str):
        """Menghapus aplikasi atau menghentikan service secara fleksibel"""
        fixed_package_id = self.utils.fix_typo_or_alias(package_id)
        all_apps = self.get_all_installed_apps()
        
        # Cek apakah yang mau dihapus/dimatikan adalah sebuah SERVICE sistem
        # Kita cek apakah service tersebut ada di daftar running systemd
        try:
            check_svc = subprocess.run(["systemctl", "is-active", f"{fixed_package_id}.service"], stdout=subprocess.PIPE, text=True)
            if check_svc.returncode == 0:
                print(f"⚙️  Mendeteksi '{fixed_package_id}' sebagai layanan sistem yang aktif.")
                confirm = input(f"❓ Apakah kamu ingin menonaktifkan & mematikan service ini, sayang? (y/n): ").lower()
                if confirm == 'y':
                    print(f"🔥 Mematikan dan menonaktifkan service: {fixed_package_id}...")
                    subprocess.run(["sudo", "systemctl", "stop", f"{fixed_package_id}.service"])
                    subprocess.run(["sudo", "systemctl", "disable", f"{fixed_package_id}.service"])
                    print(f"🎉 Service '{fixed_package_id}' berhasil dimatikan total, sayang!")
                return
        except Exception:
            pass

        # Jika bukan service, jalankan logika penghapusan aplikasi biasa seperti kemarin
        if fixed_package_id not in all_apps:
            print(f"❌ Aplikasi atau Service '{fixed_package_id}' tidak ditemukan di sistem, sayang.")
            return
            
        app_info = all_apps[fixed_package_id]
        app_type = app_info["type"]
        print(f"🔥 Memulai proses penghapusan untuk: {self.C_BOLD}{app_info['name']}{self.C_RESET} [{app_type}]...")
        
        if app_type == "APT (Native Debian/Ubuntu)":
            subprocess.run(["sudo", "apt-get", "purge", "-y", fixed_package_id])
            subprocess.run(["sudo", "apt-get", "autoremove", "-y"])
        elif app_type == "Snap Store":
            subprocess.run(["sudo", "snap", "remove", fixed_package_id])
        elif app_type == "Flatpak":
            subprocess.run(["flatpak", "uninstall", "-y", fixed_package_id])
        else:
            print("⚙️  Mendeteksi instalasi manual. Menghapus pintasan sistem...")
            if os.path.exists(app_info["desktop_file"]):
                os.remove(app_info["desktop_file"])
                print("✅ File pintasan .desktop berhasil dihapus.")
            
            exec_cmd = app_info["exec"]
            if os.path.exists(exec_cmd) and not exec_cmd.startswith(("/usr", "/bin", "/sbin")):
                app_dir = os.path.dirname(exec_cmd)
                print(f"🧹 Membersihkan folder sisa aplikasi di: {app_dir}")
                subprocess.run(["rm", "-rf", app_dir])
                print("✅ Folder aplikasi berhasil dibersihkan.")
                
        print(f"🎉 Aplikasi '{app_info['name']}' sukses dihapus total, sayang!")

if __name__ == '__main__':
    manager = PackageManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "list":
            manager.smart_list()
            
        elif command == "remove" and len(sys.argv) > 2:
            arg2 = sys.argv[2]

            # Memanggil fungsi dari file_manager.py jika memakai argumen -d
            if arg2 == "-d" and len(sys.argv) > 3:
                target_berkas = sys.argv[3]
                manager.file_handler.delete_item(target_berkas)

            elif arg2 == "-d" and len(sys.argv) <= 3:
                print(f"❌ Argumen -d membutuhkan nama file atau folder yang ingin dihapus, sayang.")
                print(f"💡 Contoh: one remove -d dokumen.pdf")

            else:
                # Jika tidak pakai -d, hapus paket aplikasi internet seperti biasa
                print(f"🗑️  Memproses penghapusan paket/layanan untuk: '{arg2}'...")
                manager.smart_remove(arg2)
            
        elif command == "search" and len(sys.argv) > 2:
            # Mengambil argumen setelah kata 'search'
            arg2 = sys.argv[2]
            
            # FITUR BARU: Jika user memasukkan argumen -f untuk mencari file/folder, sayang
            if arg2 == "-f" and len(sys.argv) > 3:
                target_search = sys.argv[3]
                print(f"📂 {manager.C_PINE}Mencari file atau folder bernama: '{target_search}'...{manager.C_RESET}\n")
                
                # Kita jalankan perintah 'find' dari direktori home user (~/) agar aman dan cepat
                # -iname membuat pencarian bersifat Case-Insensitive (tidak peduli huruf besar/kecil)
                # 2>/dev/null digunakan untuk menyembunyikan pesan error "Permission Denied" yang mengganggu
                try:
                    home_dir = os.path.expanduser("~")
                    result = subprocess.run(
                        f"find {home_dir} -iname '*{target_search}*' 2>/dev/null",
                        shell=True, stdout=subprocess.PIPE, text=True
                    )
                    
                    if result.stdout.strip():
                        # Tampilkan hasil pencarian berkas dengan estetik
                        lines = result.stdout.splitlines()
                        print(f"✨ Berhasil menemukan {len(lines)} lokasi:")
                        for line in lines:
                            # Jika yang ditemukan adalah folder, beri warna gold, jika file biasa beri warna default
                            if os.path.isdir(line):
                                print(f"  📁 {manager.C_GOLD}{line}{manager.C_RESET}")
                            else:
                                print(f"  📄 {line}")
                    else:
                        print(f"❌ File atau folder '{target_search}' tidak ditemukan di direktori home kamu, sayang.")
                except Exception as e:
                    print(f"❌ Terjadi kesalahan saat mencari: {e}")
                    
            elif arg2 == "-f" and len(sys.argv) <= 3:
                print(f"❌ Argumen -f membutuhkan nama file atau folder yang dicari, sayang.")
                print(f"💡 Contoh: one search -f dokumen.txt")
                
            else:
                # Jika tidak pakai -f, maka dia mencari paket aplikasi biasa seperti kemarin
                fixed_name = manager.utils.fix_typo_or_alias(arg2)
                print(f"🔍 Mencari paket aplikasi untuk: '{fixed_name}'...")
                subprocess.run(["apt-cache", "search", fixed_name])
            
        elif command == "install" and len(sys.argv) > 2:
            arg2 = sys.argv[2]
            
            # SINKRONISASI: Menggunakan argumen -l untuk instalasi file LOKAL .deb, sayang!
            if arg2 == "-l" and len(sys.argv) > 3:
                file_path = sys.argv[3]
                
                # Pastikan file tersebut beneran ada di komputer kamu
                if os.path.exists(file_path):
                    print(f"📦 {manager.C_PINE}Mendeteksi perintah instalasi file lokal...{manager.C_RESET}")
                    print(f"🚀 Memasang file lokal: '{os.path.basename(file_path)}'...")
                    
                    # Ambil path absolut agar apt-get tidak bingung mencari lokasinya
                    abs_path = os.path.abspath(file_path)
                    result = subprocess.run(["sudo", "apt-get", "install", "-y", abs_path])
                    
                    if result.returncode == 0:
                        print(f"\n🎉 File '{os.path.basename(file_path)}' sukses terpasang di sistem kamu, sayang!")
                    else:
                        print(f"\n❌ Gagal menginstal file lokal. Periksa kembali dependensi sistem kamu, sayang.")
                else:
                    print(f"❌ File '{file_path}' tidak ditemukan di lokasi tersebut, sayang.")
                    print(f"💡 Contoh: one install -l ./aplikasi.deb")
                    
            elif arg2 == "-l" and len(sys.argv) <= 3:
                print(f"❌ Argumen -l membutuhkan jalur file (.deb) lokal yang ingin diinstal, sayang.")
                print(f"💡 Contoh: one install -l ./discord.deb")
                
            else:
                # Jika tidak pakai argumen -l, pasang aplikasi dari repositori internet seperti biasa
                fixed_name = manager.utils.fix_typo_or_alias(arg2)
                print(f"🚀 Memulai instalasi paket dari repositori untuk: '{fixed_name}'...")
                subprocess.run(["sudo", "apt-get", "install", "-y", fixed_name])

        elif command == "update":
            manager.update_manager.check_and_update()

        elif command == "extract" and len(sys.argv) > 2:
            archive_file = sys.argv[2]
            manager.extractor.extract(archive_file)

        elif command == "extract" and len(sys.argv) <= 2:
            print("❌ Perintah 'extract' membutuhkan argumen nama file arsip, sayang.")
            print("💡 Contoh: one extract berkas.zip")
            
        elif command in ["help", "-h", "--help"]:
            manager.helper.show_help()

        elif command == "system":
            print("🚀 Membuka Dashboard Sistem...")
            manager.system_monitor.start()
            
        else:
            # Jika argumen yang dimasukkan salah atau kurang (misal ketik 'one install' tanpa nama aplikasi)
            if command in ["install", "search", "remove"] and len(sys.argv) <= 2:
                print(f"❌ Perintah '{command}' membutuhkan nama aplikasi, sayang.")
                print(f"💡 Contoh: one {command} nama-aplikasi")
            else:
                print(f"❌ Perintah '{command}' tidak dikenal.")
                manager.helper.show_help()

        
    else:
        # Jika cuma ketik 'one' tanpa argumen sama sekali
        manager.helper.show_help()