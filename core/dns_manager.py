import sys
import socket
from core.base_manager import BaseManager

class DnsManager(BaseManager):
    def run(self):
        if len(sys.argv) < 3:
            self.error("Usage: one dns <domain_name>")
            self.info("Example: one dns github.com")
            return
        
        domain = sys.argv[2]
        self.info(f"Resolving DNS records for: {domain}")
        
        try:
            hostname, aliases, ips = socket.gethostbyname_ex(domain)
            print(f"\n  {self.C_CYAN}Target{self.C_RESET}  : {hostname}")
            if aliases:
                print(f"  {self.C_YELLOW}Aliases{self.C_RESET} : {', '.join(aliases)}")
            
            for ip in ips:
                print(f"  {self.C_GREEN}IPv4{self.C_RESET}    : {ip}")
            self.success("DNS resolution completed.")
        except socket.gaierror:
            self.error(f"Failed to resolve '{domain}'. Domain might not exist.")
        except Exception as e:
            self.error(f"An unexpected error occurred: {e}")