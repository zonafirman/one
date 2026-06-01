# core/file_manager.py
import os
import shutil
import subprocess

class FileManager:
    def __init__(self):
        self.C_PINE = "\033[36m"
        self.C_RESET = "\033[0m"

    def delete_item(self, raw_path: str):
        """Fungsi universal untuk menghapus file atau folder secara aman & kebal permission, sayang"""
        target_path = os.path.abspath(raw_path)
        target_name = os.path.basename(target_path)
        
        if not os.path.exists(target_path):
            print(f"❌ '{target_name}' tidak ditemukan di lokasi tersebut, sayang.")
            return

        # KONDISI 1: JIKA TARGET ADALAH FOLDER
        if os.path.isdir(target_path):
            print(f"🗑️  {self.C_PINE}Mendeteksi perintah hapus folder...{self.C_RESET}")
            print(f"⚠️  Menghapus folder: '{target_name}' beserta seluruh isinya...")
            try:
                shutil.rmtree(target_path)
                print(f"\n🎉 Folder '{target_name}' berhasil dihapus total, sayang!")
            except PermissionError:
                # TRICK: Jika hak akses ditolak, otomatis pakai mode super user di latar belakang!
                print(f"🔒 {self.C_PINE}Hak akses terbatas detected. Mencoba menghapus dengan akses sudo...{self.C_RESET}")
                result = subprocess.run(["sudo", "rm", "-rf", target_path])
                if result.returncode == 0:
                    print(f"\n🎉 Folder '{target_name}' sukses dihapus menggunakan akses sudo, sayang!")
                else:
                    print(f"\n❌ Gagal menghapus folder bahkan dengan akses sudo.")
            except Exception as e:
                print(f"\n❌ Gagal menghapus folder: {e}")
                
        # KONDISI 2: JIKA TARGET ADALAH FILE BIASA
        else:
            print(f"🗑️  {self.C_PINE}Mendeteksi perintah hapus file...{self.C_RESET}")
            print(f"⚠️  Menghapus file: '{target_name}'...")
            try:
                os.remove(target_path)
                print(f"\n🎉 File '{target_name}' berhasil dihapus dari sistem, sayang!")
            except PermissionError:
                # TRICK: Otomatis pakai mode super user untuk file bandel
                print(f"🔒 {self.C_PINE}Hak akses terbatas detected. Mencoba menghapus dengan akses sudo...{self.C_RESET}")
                result = subprocess.run(["sudo", "rm", "-f", target_path])
                if result.returncode == 0:
                    print(f"\n🎉 File '{target_name}' sukses didepak menggunakan akses sudo, sayang!")
                else:
                    print(f"\n❌ Gagal menghapus file bahkan dengan akses sudo.")
            except Exception as e:
                print(f"\n❌ Gagal menghapus file: {e}")