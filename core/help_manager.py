from core.base_manager import BaseManager
class HelpManager(BaseManager):
    def show_help(self):
        print(f"\n{self.C_CYAN}{self.C_BOLD}=== 🚀 One-CLI Enterprise Edition ==={self.C_RESET}")
        print("Usage: one <command> [arguments]\n")
        
        categories = {
            "📦 Package Management": {
                "search": "Cari paket lintas repo (APT, Flatpak, Snap) atau file (-f).",
                "info": "Lihat detail meta-data aplikasi.",
                "install": "Pasang paket dari repo atau file .deb (-l).",
                "remove": "Hapus paket, file (-d), atau service.",
                "list": "Tampilkan aplikasi visual & systemd service aktif.",
                "update": "Sinkronisasi indeks APT.",
            },
            "🖥️  System & Diagnostics": {
                "system": "Dashboard TUI monitor CPU, RAM, IO.",
                "doctor": "Diagnosa hardware, disk, dan memory.",
                "clean": "Pembersihan cache APT/System (--all).",
                "fetch": "Sistem info minimalis.",
                "disk": "Analisis partisi disk dan temukan folder terbesar.",
            },
            "🌐 Network & Security": {
                "ports": "Monitor active listening TCP/UDP ports.",
                "security": "Jalankan audit keamanan sistem (UFW, Ports, SSH).",
                "ip": "Tampilkan IP lokal, publik, dan detail ISP.",
                "ping": "Uji latensi jaringan.",
                "speedtest": "Uji throughput bandwidth.",
                "dns": "Lakukan resolusi DNS/IP untuk sebuah domain.",
                "ssh": "Manajemen kunci SSH (generate & list).",
            },
            "🛠️  Utilities": {
                "extract": "Ekstraksi arsip (.zip, .tar, .rar, .7z).",
                "tree": "Tampilkan struktur direktori dalam format pohon.",
                "cron": "Tampilkan jadwal tugas otomatis (Cron Jobs).",
                "env": "Tampilkan atau cari environment variables sistem.",
                "users": "Audit pengguna sistem dan sesi login aktif.",
                "kill": "Matikan proses berdasarkan nama atau nomor Port.",
                "history": "Tampilkan riwayat perintah one-cli (--clear untuk hapus).",
                "docker": "Manajemen container Docker lokal.",
                "logs": "Audit system journal (error/warning).",
                "service": "Manajemen systemd service (start/stop/status).",
            },
            "💾 Backup & Restore": {
                "backup": "Ekspor profil aplikasi sistem ke JSON.",
                "restore": "Pulihkan sistem dari file JSON.",
            },
            "⚙️  CLI Management": {
                "upgrade": "Tarik versi kode One-CLI terbaru dari Git.",
                "version": "Tampilkan versi One-CLI yang sedang berjalan.",
                "help": "Tampilkan panduan ini.",
            }
        }
        
        for category, cmds in categories.items():
            print(f"{self.C_YELLOW}{self.C_BOLD}{category}{self.C_RESET}")
            for k, v in cmds.items():
                print(f"  {self.C_CYAN}{k:<10}{self.C_RESET} : {v}")
            print("")
