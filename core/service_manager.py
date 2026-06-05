import subprocess
import sys
from core.base_manager import BaseManager

class ServiceManager(BaseManager):
    def run(self):
        if len(sys.argv) < 3:
            self.error("Usage: one service <status|start|stop|restart> <service_name>")
            return
        
        action = sys.argv[2]
        if action not in ["status", "start", "stop", "restart"]:
            self.error("Invalid action. Use status, start, stop, or restart.")
            return

        if len(sys.argv) < 4:
            self.error("Please specify a service name.")
            return

        service = sys.argv[3]
        self.info(f"Executing '{action}' on service '{service}'...")
        try:
            cmd = ["sudo", "systemctl", action, service]
            if action == "status":
                subprocess.run(cmd, check=False)
            else:
                subprocess.run(cmd, check=True)
                self.success(f"Service '{service}' successfully {action}ed.")
        except subprocess.CalledProcessError:
            self.error(f"Failed to {action} service '{service}'.")