import subprocess
import json
import urllib.request
from core.base_manager import BaseManager

class IpManager(BaseManager):
    def run(self):
        self.info("Fetching network interface information...")
        
        try:
            local_ip = subprocess.check_output(["hostname", "-I"], text=True).strip().split()[0]
            print(f"  {self.C_CYAN}Local IP{self.C_RESET}    : {local_ip}")
        except Exception:
            self.warn("Could not determine Local IP.")

        self.info("Fetching public IP and Geo-location...")
        try:
            req = urllib.request.Request("https://ipinfo.io/json", headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                print(f"  {self.C_GREEN}Public IP{self.C_RESET}   : {data.get('ip', 'N/A')}")
                print(f"  {self.C_YELLOW}ISP{self.C_RESET}         : {data.get('org', 'N/A')}")
                print(f"  {self.C_YELLOW}Location{self.C_RESET}    : {data.get('city', '')}, {data.get('region', '')}, {data.get('country', '')}")
                print(f"  {self.C_YELLOW}Timezone{self.C_RESET}    : {data.get('timezone', 'N/A')}")
            self.success("Network identity retrieved successfully.")
        except Exception as e:
            self.error(f"Could not fetch public IP information. Check your internet connection.")