import os
import sys
import subprocess
import json
from datetime import datetime
from core.base_manager import BaseManager

class BackupManager(BaseManager):
    def __init__(self):
        super().__init__()

    def execute_backup(self):
        self.info("Starting system package backup...")
        self.info("Scanning manually installed packages...")
        
        backup_data = {"APT": [], "Flatpak": [], "Snap": []}

        try:
            apt_out = subprocess.check_output(["apt-mark", "showmanual"], text=True, stderr=subprocess.DEVNULL)
            backup_data["APT"] = [p.strip() for p in apt_out.splitlines() if p.strip()]
            self.info(f"Found: {len(backup_data['APT'])} APT packages.")
        except Exception as e:
            self.warn(f"Could not back up APT packages: {e}")

        try:
            flat_out = subprocess.check_output(["flatpak", "list", "--app", "--columns=application"], text=True, stderr=subprocess.DEVNULL)
            backup_data["Flatpak"] = [p.strip() for p in flat_out.splitlines() if p.strip()]
            self.info(f"Found: {len(backup_data['Flatpak'])} Flatpak applications.")
        except Exception as e:
            self.warn(f"Could not back up Flatpak packages: {e}")

        try:
            snap_out = subprocess.check_output(["snap", "list"], text=True, stderr=subprocess.DEVNULL)
            lines = snap_out.splitlines()[1:]
            backup_data["Snap"] = [line.split()[0] for line in lines if line.strip()]
            self.info(f"Found: {len(backup_data['Snap'])} Snap applications.")
        except Exception as e:
            self.warn(f"Could not back up Snap packages: {e}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.expanduser(f"~/one_backup_{timestamp}.json")
        
        with open(filename, 'w') as f:
            json.dump(backup_data, f, indent=4)

        self.success(f"Backup complete. File saved to: {filename}")

    def execute_restore(self):
        if len(sys.argv) < 3:
            self.error("Usage: one restore <path_to_backup.json>")
            return
        file_path = sys.argv[2]
        target = os.path.abspath(file_path)
        if not os.path.exists(target):
            self.error(f"Backup file not found: '{target}'")
            return

        self.info(f"Starting system restore from: {os.path.basename(target)}")
        try:
            with open(target, 'r') as f:
                data = json.load(f)
            
            apt_pkgs = data.get("APT", [])
            flat_pkgs = data.get("Flatpak", [])
            snap_pkgs = data.get("Snap", [])

            self.info(f"To be restored: {len(apt_pkgs)} APT, {len(flat_pkgs)} Flatpak, {len(snap_pkgs)} Snap packages.")
            if input(f"{self.C_YELLOW}[WARN]{self.C_RESET} Proceed with restoration? (y/n): ").lower() != 'y':
                self.warn("Restore operation cancelled by user.")
                return

            self.info("Starting restoration process... (Sudo password may be required)")
            
            if apt_pkgs:
                self.info("Restoring APT packages...")
                subprocess.run(["sudo", "apt-get", "install", "-y"] + apt_pkgs, check=True)
            
            if flat_pkgs:
                self.info("Restoring Flatpak applications...")
                for pkg in flat_pkgs:
                    subprocess.run(["flatpak", "install", "flathub", pkg, "-y"], check=True)
            
            if snap_pkgs:
                self.info("Restoring Snap applications...")
                for pkg in snap_pkgs:
                    subprocess.run(["sudo", "snap", "install", pkg], check=True)

            self.success("System restoration completed successfully.")

        except Exception as e:
            self.error(f"Failed to read or restore from file: {e}")