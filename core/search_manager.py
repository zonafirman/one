import subprocess
import sys
import shutil
import concurrent.futures
from core.base_manager import BaseManager

class SearchManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.C_SUBTLE = "\033[90m"

    def _truncate(self, text, max_len):
        return text[:max_len-3] + "..." if len(text) > max_len else text

    def _search_apt(self, query):
        results = []
        try:
            out = subprocess.check_output(["apt-cache", "search", query], text=True, stderr=subprocess.DEVNULL)
            for line in out.strip().split("\n")[:6]:
                if " - " in line:
                    pkg_name, desc = line.split(" - ", 1)
                    results.append({"name": self._truncate(pkg_name.strip(), 35), "desc": self._truncate(desc.strip(), 55)})
        except (subprocess.CalledProcessError, FileNotFoundError): pass
        return results

    def _search_flatpak(self, query):
        results = []
        try:
            out = subprocess.check_output(["flatpak", "search", "--columns=application,description", query], text=True, stderr=subprocess.DEVNULL)
            for line in out.strip().split("\n"):
                parts = [p.strip() for p in line.split("\t") if p.strip()]
                if len(parts) >= 2 and parts[0] != "Application":
                    results.append({"name": self._truncate(parts[0], 35), "desc": self._truncate(parts[1], 55)})
                if len(results) >= 6: break
        except (subprocess.CalledProcessError, FileNotFoundError): pass
        return results

    def _search_snap(self, query):
        results = []
        try:
            out = subprocess.check_output(["snap", "find", query], text=True, stderr=subprocess.DEVNULL)
            for line in out.strip().split("\n"):
                if line.startswith("Name") or not line.strip(): continue
                parts = [p.strip() for p in line.split("  ") if p.strip()]
                if len(parts) >= 2 and not parts[0].startswith(" "):
                    results.append({"name": self._truncate(parts[0], 35), "desc": self._truncate(parts[-1], 55)})
                if len(results) >= 6: break
        except (subprocess.CalledProcessError, FileNotFoundError): pass
        return results

    def _print_results(self, title, items, icon, color, col_width, empty_msg):
        print(f"\n  {self.C_BOLD}{color}{title}{self.C_RESET}")
        if items:
            for pkg in items:
                print(f"      {icon} {color}{pkg['name'].ljust(col_width)}{self.C_RESET} │ {pkg['desc']}")
        else:
            print(f"      {self.C_SUBTLE}({empty_msg}){self.C_RESET}")

    def run(self):
        query = " ".join(sys.argv[2:])
        if not query:
            self.error("Usage: one search <query>")
            return
        self.info(f"Searching for '{query}' across multiple repositories (parallel)...")
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            f_apt = executor.submit(self._search_apt, query)
            f_flat = executor.submit(self._search_flatpak, query)
            f_snap = executor.submit(self._search_snap, query)
            
            apt_pkgs = f_apt.result()
            flat_pkgs = f_flat.result()
            snap_pkgs = f_snap.result()

        cw = 35
        self._print_results("[ APT Results ]", apt_pkgs, "📦", self.C_YELLOW, cw, "No matching packages found.")
        self._print_results("[ Flatpak Results ]", flat_pkgs, "🚀", self.C_GREEN, cw, "No matching packages found.")
        self._print_results("[ Snap Results ]", snap_pkgs, "⚡", self.C_RED, cw, "No matching packages found.")
        self.success("\nSearch complete. Use 'one info <package_name>' for details.")