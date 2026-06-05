# core/package_utils.py
class PackageUtils:
    def __init__(self):
        self.C_PINE = "\033[36m"
        self.C_GOLD = "\033[33m"
        self.C_RESET = "\033[0m"
        self.C_BOLD = "\033[1m"

        self.popular_packages = [
            "spotify", "vlc", "htop", "neovim", "tmux", "git", "curl", "wget",
            "fastfetch", "neofetch", "docker", "nodejs", "python3", "gimp",
            "steam", "firefox", "chromium", "build-essential", "zsh", "fish",
            "obs-studio", "discord", "telegram-desktop", "postman", "eza", "bat"
        ]
        
        self.software_alternatives = {
            "neofetch": ("fastfetch", "Neofetch sudah usang sejak 2024. Fastfetch jauh lebih cepat & modern."),
            "screen": ("tmux", "Screen sudah berumur. Tmux adalah multiplexer terminal modern yang sangat stabil."),
            "iptables": ("nftables", "Iptables mulai digantikan oleh nftables untuk efisiensi jaringan."),
            "ifconfig": ("iproute2", "Net-tools (ifconfig) deprecated. Gunakan utilitas bawaan 'ip a'."),
            "ls": ("eza", "Eza (pengganti exa) memberikan visualisasi struktur file berwarna dan modern."),
            "cat": ("bat", "Bat adalah kloningan 'cat' cerdas dengan syntax highlighting bawaan.")
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
            print(f"\n📢 {self.C_BOLD}[ SUGGESTION ALTERNATIF ]{self.C_RESET}")
            print(f"   Aplikasi '{package}' sudah usang atau digantikan.")
            print(f"   ℹ️  Alasan: {reason}")
            print(f"   🔄 {self.C_PINE}one mengalihkan eksekusi ke: '{replacement}'{self.C_RESET}\n")
            return replacement

        closest_match = self.find_closest_match(package)
        if closest_match and closest_match != package:
            print(f"💡 {self.C_GOLD}[one-cli] Mengoreksi salah ketik '{package}' -> '{closest_match}'...{self.C_RESET}")
            return closest_match
        return package