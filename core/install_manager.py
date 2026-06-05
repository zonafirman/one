# core/install_manager.py
import subprocess
import shutil

class InstallManager:
    def __init__(self):
        self.C_ROSE    = "\033[35m"
        self.C_PINE    = "\033[36m"
        self.C_GOLD    = "\033[33m"
        self.C_IRIS    = "\033[34m"
        self.C_LOVE    = "\033[31m"
        self.C_FOAM    = "\033[32m"
        self.C_SUBTLE  = "\033[90m"
        self.C_RESET   = "\033[0m"
        self.C_BOLD    = "\033[1m"

    def _get_smart_suggestions(self, query):
        suggestions = []
        if shutil.which("flatpak"):
            try:
                out = subprocess.check_output(["flatpak", "search", "--columns=application", query], text=True, stderr=subprocess.DEVNULL)
                for line in out.strip().split("\n"):
                    if line.strip() and "." in line and line.strip() != "Application":
                        suggestions.append({"type": "Flatpak", "id": line.strip()})
                    if len(suggestions) >= 2: break
            except: pass
        if shutil.which("snap") and len(suggestions) < 5:
            try:
                out = subprocess.check_output(["snap", "find", query], text=True, stderr=subprocess.DEVNULL)
                for line in out.strip().split("\n"):
                    if line.startswith("Name") or not line.strip(): continue
                    parts = [p.strip() for p in line.split("  ") if p.strip()]
                    if parts and not any(s["id"] == parts[0] for s in suggestions):
                        suggestions.append({"type": "Snap", "id": parts[0]})
                    if len(suggestions) >= 4: break
            except: pass
        try:
            out = subprocess.check_output(["apt-cache", "pkgnames", query], text=True, stderr=subprocess.DEVNULL)
            for line in out.strip().split("\n"):
                if line.strip() and len(suggestions) < 5:
                    if not any(s["id"] == line.strip() for s in suggestions):
                        suggestions.append({"type": "APT", "id": line.strip()})
        except: pass
        return suggestions[:5]

    def smart_install(self, pkg_name):
        if not pkg_name:
            print(f"  {self.C_LOVE}❌ Nama paket tidak boleh kosong.{self.C_RESET}")
            return
        if "." in pkg_name and shutil.which("flatpak"):
            subprocess.run(["flatpak", "install", "flathub", pkg_name, "-y"])
            return

        print(f"\n{self.C_BOLD}{self.C_IRIS}📦 --- One-CLI Interactive Smart Installer ---{self.C_RESET}\n")
        choices = self._get_smart_suggestions(pkg_name)
        if not choices:
            print(f"  {self.C_LOVE}❌ Paket '{pkg_name}' tidak ditemukan di repositori mana pun.{self.C_RESET}\n")
            return

        print(f"  {self.C_BOLD}{self.C_SUBTLE}[ Silakan Pilih Paket Aplikasi Terdekat ]{self.C_RESET}")
        for idx, item in enumerate(choices, start=1):
            c = self.C_GOLD if item['type']=="APT" else (self.C_FOAM if item['type']=="Flatpak" else self.C_ROSE)
            print(f"      {c}{idx}. {item['id']:<40} [{item['type']}]{self.C_RESET}")
        print("")
        
        try:
            inp = input(f"  {self.C_BOLD}{self.C_IRIS}❓ Pilih nomor aplikasi (1-{len(choices)} atau 'c' untuk batal): {self.C_RESET}").strip()
            if inp.lower() == 'c': return
            idx = int(inp) - 1
            if 0 <= idx < len(choices):
                t = choices[idx]
                if t['type'] == "APT": subprocess.run(["sudo", "apt-get", "install", "-y", t['id']])
                elif t['type'] == "Flatpak": subprocess.run(["flatpak", "install", "flathub", t['id'], "-y"])
                elif t['type'] == "Snap": subprocess.run(["sudo", "snap", "install", t['id']])
                print(f"\n  {self.C_FOAM}✅ Proses instalasi selesai.{self.C_RESET}\n")
            else: print(f"\n  {self.C_LOVE}❌ Pilihan tidak valid.{self.C_RESET}")
        except: print(f"\n  {self.C_LOVE}❌ Masukan tidak valid, harap gunakan angka.{self.C_RESET}")