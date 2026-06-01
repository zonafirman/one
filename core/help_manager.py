# core/help_manager.py

class HelpManager:
    def __init__(self):
        # Kode warna ANSI ala Rosé Pine lokal
        self.C_PINE = "\033[36m"     # Teal/Pine
        self.C_ROSE = "\033[35m"     # Pink/Rose
        self.C_GOLD = "\033[33m"     # Gold/Kuning
        self.C_RESET = "\033[0m"     # Reset warna ke bawaan
        self.C_BOLD = "\033[1m"      # Teks Tebal

    def show_help(self):
        """Menampilkan panduan penggunaan perintah 'one' yang rapi dan estetik"""
        print(f"{self.C_PINE}{self.C_BOLD}=========================================================={self.C_RESET}")
        print(f" ⚡ {self.C_ROSE}{self.C_BOLD}One-CLI (one){self.C_RESET} - Universal Package Manager Wrapper")
        print(f"    {self.C_GOLD}The only package manager command you'll ever need.{self.C_RESET}")
        print(f"{self.C_PINE}=========================================================={self.C_RESET}\n")
        
        print(f"{self.C_BOLD}PENGGUNAAN:{self.C_RESET}")
        print(f"  one <perintah> [argumen]\n")
        
        print(f"{self.C_BOLD}PERINTAH YANG TERSEDIA:{self.C_RESET}")
        print(f"  {self.C_PINE}search{self.C_RESET}     : Mencari aplikasi dan files atau folder di dalam repositori dan lokal sistem.")
        print(f"   ├─ one search <nama package>         -> Mencari paket aplikasi di repositori resmi.")
        print(f"   └─ one search -f <nama>              -> Mencari file/folder di komputer")
        print(f"  {self.C_PINE}list{self.C_RESET}       : Menampilkan SEMUA aplikasi & layanan terinstal.")
        print(f"  {self.C_PINE}install{self.C_RESET}    : Menginstal aplikasi baru ke dalam sistem.")
        print(f"   ├─ one install <nama package>        -> Menginstal paket aplikasi dari repositori resmi.")
        print(f"   └─ one install -l <jalur file>       -> Menginstal file lokal (.deb)")
        print(f"  {self.C_PINE}update{self.C_RESET}     : Memperbarui daftar paket repositori sistem.")
        print(f"  {self.C_PINE}remove{self.C_RESET}     : Menghapus aplikasi atau mematikan layanan secara pintar.")
        print(f"   ├─ one remove <nama package>         -> Menghapus paket aplikasi yang terinstal.")
        print(f"   └─ one remove -d <nama>              -> Menghapus file atau folder secara permanen.")
        print(f"  {self.C_PINE}system{self.C_RESET}     : Menampilkan visualisasi performa sistem (CPU, RAM, DISK) secara real-time.")
        print(f"  {self.C_PINE}fetch{self.C_RESET}      -> Menampilkan spesifikasi sistem estetik ala Rosé Pine, sayang")
        print(f"  {self.C_PINE}extract{self.C_RESET}    : Mengekstrak berbagai format arsip (zip, tar, rar, 7z) secara otomatis.")
        print(f"  {self.C_PINE}help{self.C_RESET}       : Menampilkan menu bantuan.")
        
        print(f"\n{self.C_PINE}----------------------------------------------------------{self.C_RESET}")
        print(f"💡 {self.C_GOLD}Tips:{self.C_RESET} Gunakan ID paket di dalam tanda kurung ( ) dari hasil 'one list'")
        print(f"      untuk melakukan penghapusan via 'one remove'.")
        print(f"{self.C_PINE}=========================================================={self.C_RESET}")