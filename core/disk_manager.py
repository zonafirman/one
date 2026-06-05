import subprocess
from core.base_manager import BaseManager

class DiskManager(BaseManager):
    def run(self):
        self.info("Analyzing Disk Partitions...")
        try:
            # Menampilkan penggunaan disk dengan format rapi, mengabaikan tmpfs
            subprocess.run(["df", "-h", "-x", "tmpfs", "-x", "devtmpfs"], check=True)
        except subprocess.CalledProcessError:
            self.error("Failed to retrieve disk partitions.")

        print(f"\n{self.C_BOLD}{self.C_CYAN}[ Top 10 Largest Directories in /var ]{self.C_RESET}")
        self.info("Scanning for space hogs (Root privileges might be required for accurate results)...")
        try:
            # Mencari 10 folder terbesar di /var (tempat log/cache biasanya membengkak)
            cmd = "sudo du -Sh /var 2>/dev/null | sort -rh | head -n 10"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.stdout:
                print(res.stdout.strip())
        except Exception as e:
            self.warn(f"Could not calculate directory sizes: {e}")