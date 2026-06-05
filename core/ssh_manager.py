import os
import sys
import subprocess
from core.base_manager import BaseManager

class SshManager(BaseManager):
    def run(self):
        if len(sys.argv) > 2 and sys.argv[2] == "generate":
            self.generate_key()
        else:
            self.list_keys()

    def list_keys(self):
        self.info("Scanning for SSH keys in ~/.ssh...")
        ssh_dir = os.path.expanduser("~/.ssh")
        if not os.path.exists(ssh_dir):
            self.warn("No .ssh directory found. You don't have any SSH keys yet.")
            return
        
        keys = [f for f in os.listdir(ssh_dir) if f.endswith(".pub")]
        if not keys:
            self.warn("No public SSH keys found in ~/.ssh.")
        else:
            for k in keys:
                print(f"  {self.C_GREEN}🔑 {k}{self.C_RESET}")
        self.info("Use 'one ssh generate' to create a new secure Ed25519 keypair.")

    def generate_key(self):
        self.info("Generating a new Ed25519 SSH Keypair...")
        try:
            subprocess.run(["ssh-keygen", "-t", "ed25519"], check=True)
            self.success("SSH Keypair generated successfully.")
        except subprocess.CalledProcessError:
            self.error("SSH Key generation cancelled or failed.")