# core/docker_manager.py
import subprocess
from core.base_manager import BaseManager

class DockerManager(BaseManager):
    def manage(self):
        self.info("Scanning active Docker containers...")
        try:
            subprocess.run(["docker", "ps", "--format", "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"], check=True)
            self.success("Docker container list retrieved.")
        except Exception:
            self.error("Docker daemon is not running or Docker is not installed.")