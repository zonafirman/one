import sys, os, subprocess, time, argparse, importlib
from core.help_manager import HelpManager
from core.base_manager import BaseManager

class PackageManager(BaseManager):
    def __init__(self):
        super().__init__()
        # Registry: mapping commands to (module_name, class_name, method_name)
        # This provides a professional, scalable router avoiding massive if-else chains.
        self.COMMAND_REGISTRY = {
            "help": ("help_manager", "HelpManager", "show_help"),
            "update": ("update_manager", "UpdateManager", "run"),
            "upgrade": ("upgrade_manager", "UpgradeManager", "run"),
            "clean": ("clean_manager", "CleanManager", "run"),
            "ping": ("ping_manager", "PingManager", "run"),
            "docker": ("docker_manager", "DockerManager", "manage"),
            "logs": ("log_manager", "LogManager", "audit"),
            "system": ("system_manager", "SystemManager", "start"),
            "backup": ("backup_manager", "BackupManager", "execute_backup"),
            "restore": ("backup_manager", "BackupManager", "execute_restore"),
            "doctor": ("doctor_manager", "DoctorManager", "run"),
            "extract": ("extract_manager", "ExtractManager", "run"),
            "fetch": ("fetch_manager", "FetchManager", "run"),
            "file": ("file_manager", "FileManager", "run"),
            "info": ("info_manager", "InfoManager", "run"),
            "install": ("install_manager", "InstallManager", "run"),
            "ip": ("ip_manager", "IpManager", "run"),
            "kill": ("kill_manager", "KillManager", "run"),
            "ports": ("network_manager", "NetworkManager", "show_listening_ports"),
            "search": ("search_manager", "SearchManager", "run"),
            "security": ("security_manager", "SecurityManager", "run"),
            "service": ("service_manager", "ServiceManager", "run"),
            "speedtest": ("speed_manager", "SpeedManager", "run"),
            "history": ("history_manager", "HistoryManager", "run"),
            "tree": ("tree_manager", "TreeManager", "run"),
        }

    def setup_parser(self):
        parser = argparse.ArgumentParser(
            description="One CLI - Professional Enterprise System & Package Manager",
            usage="one <command> [options]",
            add_help=False
        )
        parser.add_argument("command", nargs="?", help="Command to execute")
        return parser

    def dispatch(self, cmd):
        """Dynamically load and execute the appropriate manager."""
        if cmd not in self.COMMAND_REGISTRY:
            self.error(f"Unknown command: '{cmd}'.")
            self.info("Use 'one help' to view all available commands.")
            return False
            
        module_name, class_name, method_name = self.COMMAND_REGISTRY[cmd]
        
        try:
            # Dynamically import the required module
            module = importlib.import_module(f"core.{module_name}")
            manager_class = getattr(module, class_name)
            manager_instance = manager_class()
            
            # Retrieve the appropriate method to run
            method = getattr(manager_instance, method_name)
            method()
            return True
            
        except ImportError:
            # Graceful fallback for commands without a fully implemented module
            self._fallback_inline(cmd)
            return True
        except AttributeError as e:
            self.error(f"Implementation error in '{module_name}': {e}")
            return False
        except Exception as e:
            self.error(f"Execution failed for command '{cmd}': {e}")
            return False

    def _fallback_inline(self, cmd):
        """Fallback inline implementations for essential commands."""
        if cmd == "update": 
            self.info("Running system update...")
            self._run_sys(["sudo", "apt", "update"])
        elif cmd == "clean":
            self.info("Running system cleanup...")
            self._run_sys(["sudo", "apt-get", "clean"])
            self._run_sys(["sudo", "apt-get", "autoremove", "-y"])
            self.success("System cache cleaned successfully.")
        elif cmd == "ping": 
            self.info("Pinging Cloudflare DNS to check connectivity...")
            self._run_sys(["ping", "-c", "4", "1.1.1.1"])
        elif cmd == "upgrade":
            self.info("Upgrading ONE CLI from repository...")
            os.chdir(os.path.expanduser("~/one"))
            self._run_sys(["git", "pull"])
            self.success("Upgrade complete.")
        else:
            self.warn(f"Command '{cmd}' is registered but its module is not implemented yet.")

    def _log_command(self, command, arguments):
        """Logs the executed command to a history file."""
        if command in ['help', 'history']:
            return
        
        history_file = os.path.expanduser("~/.one_history")
        full_command = f"one {command} {' '.join(arguments)}"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(history_file, "a") as f:
                f.write(f"{timestamp} | {full_command}\n")
        except Exception:
            # Fail silently, logging is not a critical path.
            pass

    def run(self):
        parser = self.setup_parser()
        args, unknown = parser.parse_known_args()
        
        if not args.command:
            HelpManager().show_help()
            sys.exit(0)
            
        cmd = args.command.lower()
        self._log_command(cmd, unknown)
        start_time = time.time()
        
        try:
            self.dispatch(cmd)
        except KeyboardInterrupt:
            print()
            self.warn("Operation cancelled by user (SIGINT).")
            sys.exit(130)
        except subprocess.CalledProcessError as e:
            self.error(f"Process terminated with exit code {e.returncode}.")
            sys.exit(e.returncode)
        except Exception as e:
            self.error(f"An unexpected error occurred: {e}")
            sys.exit(1)
        finally:
            elapsed = time.time() - start_time
            if cmd != "help":
                # Optional professional execution metric
                # self.info(f"Execution time: {elapsed:.2f}s")
                pass

    def _run_sys(self, args):
        """Execute system commands safely with standard interactive behavior."""
        subprocess.run(args, check=True)

if __name__ == '__main__':
    PackageManager().run()