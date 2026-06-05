from core.base_manager import BaseManager
class HelpManager(BaseManager):
    def show_help(self):
        print(f"{self.C_CYAN}{self.C_BOLD}=== One-CLI Enterprise Edition ==={self.C_RESET}")
        print("Usage: one <command> [arguments]\n")
        cmds = {
            "search": "Cari paket lintas repo (APT, Flatpak, Snap) atau file (-f).",
            "info": "Lihat detail meta-data aplikasi.",
            "install": "Pasang paket dari repo atau file .deb (-l).",
            "remove": "Hapus paket, file (-d), atau service.",
            "list": "Tampilkan aplikasi visual & systemd service aktif.",
            "extract": "Ekstraksi arsip (.zip, .tar, .rar, .7z).",
            "system": "Dashboard TUI monitor CPU, RAM, IO.",
            "docker": "Manajemen container Docker lokal.",
            "logs": "Audit system journal (error/warning).",
            "ports": "Monitor active listening TCP/UDP ports.",
            "backup": "Ekspor profil aplikasi sistem ke JSON.",
            "restore": "Pulihkan sistem dari file JSON.",
            "doctor": "Diagnosa hardware, disk, dan memory.",
            "clean": "Pembersihan cache APT/System (--all).",
            "ping": "Uji latensi jaringan.",
            "speedtest": "Uji throughput bandwidth.",
            "update": "Sinkronisasi indeks APT.",
            "fetch": "Sistem info minimalis.",
            "upgrade": "Tarik versi kode One-CLI terbaru dari Git.",
            "security": "Jalankan audit keamanan sistem (UFW, Ports, SSH).",
            "service": "Manajemen systemd service (start/stop/status).",
            "ip": "Tampilkan IP lokal, publik, dan detail ISP.",
            "kill": "Matikan proses berdasarkan nama atau nomor Port.",
            "history": "Tampilkan riwayat perintah one-cli (--clear untuk hapus).",
            "tree": "Tampilkan struktur direktori dalam format pohon.",
            "disk": "Analisis partisi disk dan temukan folder terbesar.",
            "ssh": "Manajemen kunci SSH (generate & list).",
            "cron": "Tampilkan jadwal tugas otomatis (Cron Jobs).",
            "users": "Audit pengguna sistem dan sesi login aktif.",
            "env": "Tampilkan atau cari environment variables sistem.",
            "dns": "Lakukan resolusi DNS/IP untuk sebuah domain."
        }
        for k, v in cmds.items():
            print(f"  {self.C_CYAN}{k:<10}{self.C_RESET} : {v}")
