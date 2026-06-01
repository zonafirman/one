# core/package_utils.py
from difflib import SequenceMatcher

class PackageUtils:
    def __init__(self):
        # Warna Rosé Pine Lokal
        self.C_PINE = "\033[36m"     # Teal/Pine
        self.C_GOLD = "\033[33m"     # Gold/Kuning
        self.C_RESET = "\033[0m"     # Reset
        self.C_BOLD = "\033[1m"      # Tebal

        # Kamus Aplikasi Populer untuk Fuzzy Matching Offline
        self.popular_packages = [
            "spotify", "vlc", "htop", "neovim", "tmux", "git", "curl", "wget",
            "fastfetch", "neofetch", "docker", "nodejs", "python3", "gimp",
            "steam", "firefox", "chromium", "build-essential", "zsh", "fish"
        ]
        
        # KAMUS ALTERNATIF
        self.software_alternatives = {
            "neofetch": ("fastfetch", "Neofetch sudah tidak dikembangkan lagi sejak 2024. Fastfetch jauh lebih cepat dan modern."),
            "screen": ("tmux", "Screen sudah usang. Tmux adalah terminal multiplexer modern yang lebih stabil."),
            "iptables": ("nftables", "Iptables mulai digantikan oleh nftables untuk manajemen firewall yang lebih efisien."),
            "ntp": ("chrony", "Chrony adalah implementasi NTP default baru yang lebih cepat menyinkronkan waktu."),
            "ifconfig": ("iproute2", "Tools net-tools (ifconfig) sudah deprecated. Gunakan perintah 'ip a' bawaan iproute2.")
        }

    def levenshtein_distance(self, s1: str, s2: str) -> int:
        if len(s1) > len(s2): s1, s2 = s2, s1
        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            distances__ = [i2+1]
            for i1, c1 in enumerate(s1):
                if c1 == c2: distances__.append(distances[i1])
                else: distances__.append(1 + min((distances[i1], distances[i1 + 1], distances__[-1])))
            distances = distances__
        return distances[-1]

    def find_closest_match(self, typo_word: str) -> str:
        best_match = None
        min_distance = 999
        for pkg in self.popular_packages:
            dist = self.levenshtein_distance(typo_word, pkg)
            if dist <= 2 and dist < min_distance:
                min_distance = dist
                best_match = pkg
        return best_match

    def fix_typo_or_alias(self, package: str) -> str:
        package = package.lower().strip()
        
        if package in self.software_alternatives:
            replacement, reason = self.software_alternatives[package]
            print(f"\n📢 {self.C_BOLD}[📢 NOTIFIKASI ALTERNATIF]{self.C_RESET}")
            print(f"   Aplikasi '{package}' saat ini sudah tidak tersedia atau usang.")
            print(f"   ℹ️  Alasan: {reason}")
            print(f"   🔄 {self.C_PINE}one otomatis mengalihkan perintah ke alternatif terbaik: '{replacement}'{self.C_RESET}\n")
            return replacement

        closest_match = self.find_closest_match(package)
        if closest_match and closest_match != package:
            print(f"💡 {self.C_GOLD}[one-cli] Maksud kamu mungkin '{closest_match}'? (Membetulkan typo '{package}'){self.C_RESET}")
            return closest_match
            
        return package