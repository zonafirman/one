# core/doctor_manager.py
import os
import shutil
import getpass
import subprocess

class DoctorManager:
    def __init__(self):
        # 📂 Target sistem utama
        self.target_root = "/"
        
        # 📂 Daftar berkas wajib pembentuk jantung One-CLI
        self.required_files = [
            "package_manager.py", "package_utils.py", "help_manager.py", 
            "file_manager.py", "extract_manager.py", "system_manager.py", 
            "update_manager.py", "upgrade_manager.py", "fetch_manager.py",
            "doctor_manager.py"
        ]
        
        # 🌸 Palet Warna Rosé Pine Asli
        self.C_ROSE    = "\033[38;2;235;188;186m"
        self.C_PINE    = "\033[38;2;49;116;143m"
        self.C_GOLD    = "\033[38;2;246;193;119m"
        self.C_IRIS    = "\033[38;2;196;167;231m"
        self.C_LOVE    = "\033[38;2;235;111;145m" # Indikator kritis/eror
        self.C_FOAM    = "\033[38;2;156;207;216m" # Indikator sukses/aman
        self.C_SUBTLE  = "\033[38;2;144;140;170m"
        self.C_RESET   = "\033[0m"
        self.C_BOLD    = "\033[1m"

    def check_privileges(self):
        """[1/6] Memeriksa status tingkat hak akses pengguna"""
        print(f"  {self.C_SUBTLE}[1/6]{self.C_RESET} Memeriksa Otoritas Hak Akses...")
        if os.geteuid() == 0:
            print(f"      {self.C_GOLD}⚠️  Sudo Mode Aktif. Hati-hati dalam mengeksekusi perintah sistem.{self.C_RESET}")
        else:
            print(f"      {self.C_FOAM}✅ User Standar ({getpass.getuser()}). Aman untuk operasi berkas.{self.C_RESET}")

    def check_disk_space(self):
        """[2/6] Memeriksa kapasitas ruang penyimpanan asli dan memperbaiki bug variabel"""
        print(f"  {self.C_SUBTLE}[2/6]{self.C_RESET} Menganalisis Partisi Penyimpanan ({self.target_root})...")
        try:
            total, used, free = shutil.disk_usage(self.target_root)
            total_gb = total / (2**30)
            used_gb = used / (2**30)
            free_gb = free / (2**30)
            percent_used = int((used / total) * 100)
            
            print(f"      {self.C_SUBTLE}› Detail Alokasi: Total: {total_gb:.1f} GB | Terpakai: {used_gb:.1f} GB ({percent_used}%)")
            print(f"      {self.C_SUBTLE}› Sisa Ruang    : {free_gb:.1f} GB Tersedia{self.C_RESET}")
            
            if free_gb < 5:
                print(f"      {self.C_LOVE}❌ KRITIS: Ruang disk sekarat! Segera lakukan pembersihan.{self.C_RESET}")
            elif free_gb < 15:
                print(f"      {self.C_GOLD}⚠️  PERINGATAN: Sisa penyimpanan mulai menipis.{self.C_RESET}")
            else:
                print(f"      {self.C_FOAM}✅ AMAN: Partisi penyimpanan sangat lega.{self.C_RESET}")
        except Exception as e:
            print(f"      {self.C_LOVE}❌ Gagal membaca disk: {e}{self.C_RESET}")

    def check_cpu_and_thermal(self):
        """[3/6] Menghitung Load Average sistem secara riil dan temperatur core"""
        print(f"  {self.C_SUBTLE}[3/6]{self.C_RESET} Memantau Beban Kerja CPU & Thermal...")
        try:
            load1, load5, load15 = os.getloadavg()
            print(f"      {self.C_SUBTLE}› Load Average  : {load1:.2f} (1m) | {load5:.2f} (5m) | {load15:.2f} (15m){self.C_RESET}")
            
            temp_found = False
            for path in ["/sys/class/thermal/thermal_zone0/temp", "/sys/class/hwmon/hwmon0/temp1_input"]:
                if os.path.exists(path):
                    with open(path, "r") as f:
                        temp = int(f.read().strip()) / 1000
                        print(f"      {self.C_SUBTLE}› Suhu CPU Core : {temp:.1f}°C{self.C_RESET}")
                        if temp > 80:
                            print(f"          {self.C_LOVE}🔥 Overheat! CPU terlalu panas, kurangi proses berat.{self.C_RESET}")
                        temp_found = True
                        break
            if not temp_found:
                print(f"      {self.C_SUBTLE}› Suhu CPU Core : N/A (WSL / Lingkungan Virtual){self.C_RESET}")
        except:
            print(f"      {self.C_GOLD}⚠️  Gagal memindai beberapa parameter thermal CPU.{self.C_RESET}")

    def check_ram_and_swap(self):
        """[4/6] Menganalisis keseimbangan memori fisik (RAM) dan memori virtual (Swap)"""
        print(f"  {self.C_SUBTLE}[4/6]{self.C_RESET} Menghitung Utilisasi RAM & Swap Memory...")
        try:
            with open("/proc/meminfo", "r") as f:
                mem = {line.split(":")[0].strip(): int(line.split(":")[1].split()[0]) for line in f.readlines()}
                
            total_ram = mem.get("MemTotal", 0)
            avail_ram = mem.get("MemAvailable", 0)
            used_ram = total_ram - avail_ram
            ram_pct = int((used_ram / total_ram) * 100) if total_ram else 0
            
            total_swap = mem.get("SwapTotal", 0)
            free_swap = mem.get("SwapFree", 0)
            used_swap = total_swap - free_swap
            swap_pct = int((used_swap / total_swap) * 100) if total_swap else 0

            print(f"      {self.C_SUBTLE}› Fisik (RAM)   : {used_ram//1024} MB / {total_ram//1024} MB ({ram_pct}%)")
            print(f"      {self.C_SUBTLE}› Virtual (Swap): {used_swap//1024} MB / {total_swap//1024} MB ({swap_pct}%){self.C_RESET}")
            
            if swap_pct > 50:
                print(f"      {self.C_GOLD}⚠️  Peringatan: Sistem terlalu bergantung pada Swap, indikasi RAM sesak.{self.C_RESET}")
            else:
                print(f"      {self.C_FOAM}✅ AMAN: Alokasi memori fisik dan virtual seimbang.{self.C_RESET}")
        except:
            print(f"      {self.C_LOVE}❌ Gagal membaca tabel /proc/meminfo.{self.C_RESET}")

    def check_graphics_and_drivers(self):
        """[5/6] Analisis GPU, Driver Proprietary NVIDIA, dan Akselerasi Grafis Linux asli"""
        print(f"  {self.C_SUBTLE}[5/6]{self.C_RESET} Menganalisis Perangkat Grafis & Akselerasi Driver...")
        try:
            gpu_out = subprocess.check_output("lspci | grep -E 'VGA|3D'", shell=True, text=True, stderr=subprocess.DEVNULL)
            # Potong teks hardware GPU agar pas di terminal
            clean_gpu = gpu_out.strip().split(": ")[-1] if ": " in gpu_out else gpu_out.strip()
            print(f"      {self.C_SUBTLE}› Hardware GPU   : {clean_gpu}{self.C_RESET}")
            
            if "nvidia" in gpu_out.lower() or "geforce" in gpu_out.lower():
                if os.path.exists("/proc/driver/nvidia/version"):
                    with open("/proc/driver/nvidia/version", "r") as f:
                        version_info = f.readline().strip().split("  ")[0]
                    print(f"      {self.C_FOAM}✅ Driver NVIDIA Resmi Aktif ({version_info}){self.C_RESET}")
                else:
                    print(f"      {self.C_GOLD}⚠️  Peringatan: GPU NVIDIA aktif, tapi menggunakan driver open-source generik (Nouveau).{self.C_RESET}")
                    print(f"         {self.C_SUBTLE}💡 Solusi: Disarankan pasang driver proprietary agar performa grafis maksimal.{self.C_RESET}")
            
            if shutil.which("glxinfo"):
                glx_out = subprocess.check_output("glxinfo | grep 'OpenGL version string'", shell=True, text=True, stderr=subprocess.DEVNULL)
                print(f"      {self.C_SUBTLE}› Akselerasi API : {glx_out.strip()}{self.C_RESET}")
            else:
                print(f"      {self.C_SUBTLE}› Akselerasi API : OpenGL/Vulkan Aktif (Instal 'mesa-utils' untuk detail info){self.C_RESET}")
        except:
            print(f"      {self.C_GOLD}⚠️  Informasi subsistem grafis terbatas di lingkungan ini.{self.C_RESET}")

    def check_pro_dependencies_and_integrity(self):
        """[6/6] Memeriksa broken packages tingkat sistem, kompiler, serta integritas berkas internal One-CLI"""
        print(f"  {self.C_SUBTLE}[6/6]{self.C_RESET} Memverifikasi Integritas Pustaka & Berkas Pro...")
        
        # 1. Cek Kompiler Inti untuk Development
        pro_tools = {"gcc": "Kompiler C", "make": "Otomatisasi Berkas", "pip3": "Manajer Paket Python"}
        missing_tools = [tool for tool in pro_tools if not shutil.which(tool)]
        
        if missing_tools:
            print(f"      {self.C_GOLD}⚠️  Kakas pengembangan belum lengkap: {', '.join(missing_tools)}{self.C_RESET}")
        else:
            print(f"      {self.C_FOAM}✅ Kompiler & lingkungan Python siap pakai.{self.C_RESET}")
            
        # 2. Cek Broken Packages di APT
        try:
            check_broken = subprocess.run(["apt-get", "check"], capture_output=True, text=True)
            if check_broken.returncode != 0:
                print(f"      {self.C_LOVE}❌ TERDETEKSI BROKEN PACKAGES: Ada pustaka sistem yang patah!{self.C_RESET}")
                print(f"         {self.C_SUBTLE}💡 Solusi: Jalankan perintah 'sudo apt-get install -f' untuk memperbaikinya.{self.C_RESET}")
            else:
                print(f"      {self.C_FOAM}✅ Struktur dependensi repositori APT sehat.{self.C_RESET}")
        except:
            pass

        # 3. Cek Berkas Proyek Internal One-CLI
        core_dir = os.path.dirname(os.path.abspath(__file__))
        missing_files = [f for f in self.required_files if not os.path.exists(os.path.join(core_dir, f))]
                
        if missing_files:
            print(f"      {self.C_LOVE}❌ EROR INTEGRITAS: Komponen inti One-CLI hilang: {', '.join(missing_files)}{self.C_RESET}")
        else:
            print(f"      {self.C_FOAM}✅ Sempurna: Seluruh komponen internal One-CLI utuh dan presisi.{self.C_RESET}")

    def run_diagnose(self):
        """Menjalankan runtutan fungsi diagnosis utama"""
        print(f"\n{self.C_BOLD}{self.C_IRIS}🩺 --- One-CLI Advanced System Doctor Diagnostic ---{self.C_RESET}\n")
        
        self.check_privileges()
        print("")
        self.check_disk_space()
        print("")
        self.check_cpu_and_thermal()
        print("")
        self.check_ram_and_swap()
        print("")
        self.check_graphics_and_drivers()
        print("")
        self.check_pro_dependencies_and_integrity()
        
        print(f"\n{self.C_BOLD}{self.C_ROSE}🌸 [ Analisis Selesai ] Rekam medis sistem komputermu sekarang sangat akurat, sayang!{self.C_RESET}\n")

if __name__ == "__main__":
    doc = DoctorManager()
    doc.run_diagnose()