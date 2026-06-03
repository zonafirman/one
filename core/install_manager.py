# core/install_manager.py
import subprocess
import shutil

class InstallManager:
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

    def _get_smart_suggestions(self, query):
        """Mencari rekomendasi paket yang paling mendekati dari APT, Flatpak, dan Snap (Maksimal 5)"""
        suggestions = []

        # 1. Cari di Flatpak terlebih dahulu (Biasanya versi paling update & diinginkan)
        if shutil.which("flatpak"):
            try:
                out = subprocess.check_output(["flatpak", "search", "--columns=application", query], text=True, stderr=subprocess.DEVNULL)
                for line in out.strip().split("\n"):
                    line = line.strip()
                    if line and line != "Application" and "." in line:
                        suggestions.append({"type": "Flatpak", "id": line})
                    if len(suggestions) >= 2:  # Ambil maksimal 2 dari Flatpak agar adil bagi repo lain
                        break
            except:
                pass

        # 2. Cari di Snap
        if shutil.which("snap") and len(suggestions) < 5:
            try:
                out = subprocess.check_output(["snap", "find", query], text=True, stderr=subprocess.DEVNULL)
                for line in out.strip().split("\n"):
                    if line.startswith("Name") or not line.strip():
                        continue
                    parts = [p.strip() for p in line.split("  ") if p.strip()]
                    if parts:
                        if not any(s["id"] == parts[0] for s in suggestions):
                            suggestions.append({"type": "Snap", "id": parts[0]})
                    if len(suggestions) >= 4:  # Batasi total sementara agar space tersisa untuk APT
                        break
            except:
                pass

        # 3. Cari di APT sebagai alternatif pelengkap nama yang mirip
        try:
            out = subprocess.check_output(["apt-cache", "pkgnames", query], text=True, stderr=subprocess.DEVNULL)
            for line in out.strip().split("\n"):
                if line.strip() and len(suggestions) < 5:
                    if not any(s["id"] == line.strip() for s in suggestions):
                        suggestions.append({"type": "APT", "id": line.strip()})
        except:
            pass

        return suggestions[:5]

    def smart_install(self, pkg_name):
        """Mengeksekusi instalasi dengan jaminan menu interaktif 5 pilihan terdekat lintar repo"""
        if not pkg_name:
            print(f"  {self.C_LOVE}❌ Nama paket tidak boleh kosong, sayang!{self.C_RESET}")
            return

        print(f"\n{self.C_BOLD}{self.C_IRIS}📦 --- One-CLI Interactive Smart Installer ---{self.C_RESET}\n")

        # JALUR INSTAN: Hanya jika user mengetik App-ID Flatpak secara lengkap (mengandung titik)
        if "." in pkg_name and shutil.which("flatpak"):
            self._install_flatpak(pkg_name)
            return

        # JALUR INTERAKTIF: Cari dan tampilkan menu pilihan rekomendasi (Mencegah eror kandidat kosong)
        print(f"  {self.C_SUBTLE}Memisir rekomendasi alternatif terbaik untuk '{pkg_name}'...{self.C_RESET}\n")
        choices = self._get_smart_suggestions(pkg_name)

        if not choices:
            print(f"  {self.C_LOVE}❌ Maaf sayang, tidak ada paket yang mirip sama sekali di Flatpak, Snap, maupun APT.{self.C_RESET}\n")
            return

        # Tampilkan Menu 5 Pilihan Tereliminasi Cantik
        print(f"  {self.C_BOLD}{self.C_SUBTLE}[ Silakan Pilih Paket Aplikasi Terdekat ]{self.C_RESET}")
        for index, item in enumerate(choices, start=1):
            repo_badge = f"[{item['type']}]"
            if item['type'] == "APT":
                print(f"      {self.C_GOLD}{index}. {item['id']:<40} {self.C_RESET}{self.C_GOLD}{repo_badge}{self.C_RESET}")
            elif item['type'] == "Flatpak":
                print(f"      {self.C_FOAM}{index}. {item['id']:<40} {self.C_RESET}{self.C_FOAM}{repo_badge}{self.C_RESET}")
            else:
                print(f"      {self.C_ROSE}{index}. {item['id']:<40} {self.C_RESET}{self.C_ROSE}{repo_badge}{self.C_RESET}")

        print("")
        try:
            user_input = input(f"  {self.C_BOLD}{self.C_IRIS}❓ Pilih nomor aplikasi yang ingin dipasang, sayang? (1-{len(choices)} atau 'c' untuk batal): {self.C_RESET}").strip()
            
            if user_input.lower() == 'c':
                print(f"\n  {self.C_SUBTLE}🌸 Instalasi dibatalkan.{self.C_RESET}\n")
                return

            choice_idx = int(user_input) - 1
            if 0 <= choice_idx < len(choices):
                target = choices[choice_idx]
                print(f"\n  {self.C_SUBTLE}Memproses pilihan ke-{user_input}: Memasang {target['id']} via {target['type']}...{self.C_RESET}\n")
                
                if target['type'] == "APT":
                    self._install_apt(target['id'])
                elif target['type'] == "Flatpak":
                    self._install_flatpak(target['id'])
                elif target['type'] == "Snap":
                    self._install_snap(target['id'])
            else:
                print(f"\n  {self.C_LOVE}❌ Pilihan nomor tidak valid, sayang!{self.C_RESET}\n")
        except ValueError:
            print(f"\n  {self.C_LOVE}❌ Input harus berupa angka pilihan, sayang!{self.C_RESET}\n")

    def _install_apt(self, pkg_name):
        try:
            print(f"  {self.C_GOLD}⚡ Mengeksekusi: sudo apt-get install -y {pkg_name}{self.C_RESET}\n")
            subprocess.run(["sudo", "apt-get", "install", "-y", pkg_name], check=True)
            print(f"\n  {self.C_FOAM}✅ Selesai! Paket '{pkg_name}' (APT) sukses terpasang, sayang.{self.C_RESET}\n")
        except subprocess.CalledProcessError:
            print(f"  {self.C_LOVE}❌ Proses instalasi APT gagal atau dibatalkan.{self.C_RESET}")

    def _install_flatpak(self, app_id):
        print(f"  {self.C_PINE}⚡ Mengeksekusi: flatpak install flathub {app_id} -y{self.C_RESET}\n")
        try:
            subprocess.run(["flatpak", "install", "flathub", app_id, "-y"], check=True)
            print(f"\n  {self.C_FOAM}✅ Selesai! Aplikasi Flatpak '{app_id}' sukses terpasang, sayang.{self.C_RESET}\n")
        except subprocess.CalledProcessError:
            print(f"  {self.C_LOVE}❌ Gagal memasang Flatpak. Pastikan runtime Flathub berjalan normal.{self.C_RESET}")

    def _install_snap(self, pkg_name):
        print(f"  {self.C_ROSE}⚡ Mengeksekusi: sudo snap install {pkg_name}{self.C_RESET}\n")
        try:
            subprocess.run(["sudo", "snap", "install", pkg_name], check=True)
            print(f"\n  {self.C_FOAM}✅ Selesai! Aplikasi Snap '{pkg_name}' sukses terpasang, sayang.{self.C_RESET}\n")
        except subprocess.CalledProcessError:
            print(f"  {self.C_LOVE}❌ Gagal memasang paket lewat Snapcraft.{self.C_RESET}")