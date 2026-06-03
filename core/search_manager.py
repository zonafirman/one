# core/search_manager.py
import subprocess
import shutil

class SearchManager:
    def __init__(self):
        # 🌸 Palet Warna Rosé Pine Asli
        self.C_ROSE    = "\033[38;2;235;188;186m"
        self.C_PINE    = "\033[38;2;49;116;143m"
        self.C_GOLD    = "\033[38;2;246;193;119m"
        self.C_IRIS    = "\033[38;2;196;167;231m"
        self.C_LOVE    = "\033[38;2;235;111;145m"
        self.C_FOAM    = "\033[38;2;156;207;216m"
        self.C_SUBTLE  = "\033[38;2;144;140;170m"
        self.C_RESET   = "\033[0m"
        self.C_BOLD    = "\033[1m"

    def _truncate(self, text, max_len):
        """Memotong teks jika melebihi batas agar tidak meluber ke baris baru"""
        return text[:max_len-3] + "..." if len(text) > max_len else text

    def _search_apt(self, query):
        """Mencari paket aplikasi di repositori APT Linux asli"""
        results = []
        try:
            out = subprocess.check_output(["apt-cache", "search", query], text=True, stderr=subprocess.DEVNULL)
            for line in out.strip().split("\n")[:6]:
                if " - " in line:
                    pkg_name, desc = line.split(" - ", 1)
                    results.append({
                        "name": self._truncate(pkg_name.strip(), 35), 
                        "desc": self._truncate(desc.strip(), 55)
                    })
        except:
            pass
        return results

    def _search_flatpak(self, query):
        """Mencari paket aplikasi di katalog Flathub / Flatpak dengan parsing presisi"""
        results = []
        if not shutil.which("flatpak"):
            return results
        try:
            # Menggunakan opsi --columns=application,description agar output teratur dan tidak terbalik
            out = subprocess.check_output(
                ["flatpak", "search", "--columns=application,description", query], 
                text=True, stderr=subprocess.DEVNULL
            )
            lines = out.strip().split("\n")
            for line in lines:
                if not line.strip():
                    continue
                # Flatpak search menggunakan pembatas Tab (\t)
                parts = [p.strip() for p in line.split("\t") if p.strip()]
                if len(parts) >= 2 and parts[0] != "Application":
                    results.append({
                        "name": self._truncate(parts[0], 35), 
                        "desc": self._truncate(parts[1], 55)
                    })
                if len(results) >= 6:
                    break
        except:
            pass
        return results

    def _search_snap(self, query):
        """Mencari paket aplikasi di katalog resmi Snapcraft (Snapd)"""
        results = []
        if not shutil.which("snap"):
            return results
        try:
            out = subprocess.check_output(["snap", "find", query], text=True, stderr=subprocess.DEVNULL)
            lines = out.strip().split("\n")
            for line in lines:
                if line.startswith("Name") or not line.strip():
                    continue
                # Split berdasarkan spasi ganda untuk memisahkan kolom snap find
                parts = [p.strip() for p in line.split("  ") if p.strip()]
                if len(parts) >= 2:
                    results.append({
                        "name": self._truncate(parts[0], 35), 
                        "desc": self._truncate(parts[-1], 55)
                    })
                if len(results) >= 6:
                    break
        except:
            pass
        return results

    def unified_search(self, query):
        """Menggabungkan hasil pencarian 3 repo dengan layout lurus, rapi, dan sejajar"""
        if not query:
            print(f"  {self.C_LOVE}❌ Nama paket tidak boleh kosong, sayang!{self.C_RESET}")
            return

        print(f"\n{self.C_BOLD}{self.C_IRIS}🔍 --- One-CLI Unified Package Search ---{self.C_RESET}")
        print(f"{self.C_SUBTLE}Kata Kunci: '{query}'{self.C_RESET}\n")

        # Batas lebar kolom nama (padding otomatis agar karakter pembatas │ lurus vertikal)
        col_width = 35

        # 1. Jalankan dan tampilkan hasil pencarian APT
        print(f"  {self.C_SUBTLE}[1/3] Menyisir Repositori Lokal (APT)...{self.C_RESET}")
        apt_pkgs = self._search_apt(query)
        if apt_pkgs:
            for pkg in apt_pkgs:
                padded_name = f"{pkg['name']}".ljust(col_width)
                print(f"      📦 {self.C_GOLD}{padded_name}{self.C_RESET} │ {pkg['desc']}")
        else:
            print(f"      {self.C_SUBTLE}(Tidak ada paket APT yang cocok){self.C_RESET}")
        print("")

        # 2. Jalankan dan tampilkan hasil pencarian Flatpak
        print(f"  {self.C_SUBTLE}[2/3] Menyisir Katalog Global (Flatpak)...{self.C_RESET}")
        flat_pkgs = self._search_flatpak(query)
        if flat_pkgs:
            for pkg in flat_pkgs:
                padded_name = f"{pkg['name']}".ljust(col_width)
                print(f"      🚀 {self.C_FOAM}{padded_name}{self.C_RESET} │ {pkg['desc']}")
        else:
            print(f"      {self.C_SUBTLE}(Tidak ada paket Flatpak yang cocok atau Flatpak belum aktif){self.C_RESET}")
        print("")

        # 3. Jalankan dan tampilkan hasil pencarian Snap
        print(f"  {self.C_SUBTLE}[3/3] Menyisir Katalog Canonical (Snap)...{self.C_RESET}")
        snap_pkgs = self._search_snap(query)
        if snap_pkgs:
            for pkg in snap_pkgs:
                padded_name = f"{pkg['name']}".ljust(col_width)
                print(f"      ⚡ {self.C_ROSE}{padded_name}{self.C_RESET} │ {pkg['desc']}")
        else:
            print(f"      {self.C_SUBTLE}(Tidak ada paket Snap yang cocok atau Snapcraft bermasalah){self.C_RESET}")

        print(f"\n{self.C_BOLD}{self.C_IRIS}🌸 Pencarian selesai di 3 Repo! Gunakan 'one info <nama_paket>' untuk melihat detail paket.{self.C_RESET}\n")

if __name__ == "__main__":
    s = SearchManager()
    s.unified_search("vlc")