import subprocess
import sys
import time
import socket
import requests
from pathlib import Path

def connect_openvpn(config_path, openvpn_path="openvpn"):
    """Connect to OpenVPN using the provided configuration file."""
    try:
        config_file = Path(config_path)
        if not config_file.exists():
            print(f"❌ Error: Configuration file '{config_path}' does not exist.")
            sys.exit(1)
        
        openvpn_path = Path(openvpn_path)
        if not openvpn_path.exists():
            print(f"❌ Error: OpenVPN executable '{openvpn_path}' not found.")
            sys.exit(1)

        cmd = [str(openvpn_path), '--config', str(config_file)]
        
        print(f"🔄 Connecting to OpenVPN server using config: {config_path}")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if 'Initialization Sequence Completed' in output:
                print("✅ Successfully connected to the VPN!")
                time.sleep(5)  # Ensure tunnel is fully established
                #flush_dns_cache()  # Flush DNS after connection
                check_vpn_status()
                break
            if output:
                print(output.strip())
                
        process.stdout.close()
        process.wait()
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Error connecting to OpenVPN: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def flush_dns_cache():
    """Flush the DNS cache based on the OS."""
    try:
        print("🧹 Flushing DNS cache...")
        if sys.platform == "win32":
            subprocess.run(["ipconfig", "/flushdns"], check=True)
        elif sys.platform == "linux":
            subprocess.run(["sudo", "systemd-resolve", "--flush-caches"], check=True)
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["sudo", "killall", "-HUP", "mDNSResponder"], check=True)
        print("✅ DNS cache flushed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error flushing DNS: {e}")

def get_vpn_ip():
    """Get the local VPN-assigned IP."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # Detect correct adapter
    vpn_ip = s.getsockname()[0]
    s.close()
    return vpn_ip

def get_public_ip():
    """Check the current public IPv4 address through VPN connection."""
    try:
        print("\n🌍 Checking public IP address through VPN...")
        services = ["https://api64.ipify.org", "https://ifconfig.me", "https://icanhazip.com"]
        for service in services:
            try:
                result = requests.get(service, timeout=5).text.strip()
                print(f"Public IP from {service}: {result}")
                return result
            except requests.RequestException as e:
                print(f"⚠️ Error checking IP with {service}: {e}")
        return "⚠️ Failed to check public IP."
    except Exception as e:
        return f"⚠️ Error retrieving public IP: {e}"
    
def get_public_ip_location(ip):
    """Get the geographical location of the public IP address."""
    try:
        print(f"\n🌐 Getting location for IP: {ip}")
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            location = f"{data.get('city')}, {data.get('region')}, {data.get('country_name')}"
            print(f"📍 Location: {location}")
            return location
        else:
            print(f"⚠️ Failed to get location for IP: {ip}")
            return "Unknown location"
    except requests.RequestException as e:
        print(f"⚠️ Error retrieving IP location: {e}")
        return "Error retrieving location"


def check_vpn_status():
    """Verify if traffic is correctly routed through OpenVPN."""
    vpn_ip = get_vpn_ip()
    public_ip = get_public_ip()

    print(f"🛜 VPN Local IP: {vpn_ip}")
    print(f"🌍 Public IP (should match VPN IP): {public_ip}")

    if public_ip == "OpenVpnAs Ip Address":
        print("🎉 Successfully routed traffic through OpenVPN!")
        # Example usage
        location = get_public_ip_location(public_ip)
        print(f"🌍 Public IP Location: {location}")
    else:
        print("⚠️ WARNING: Traffic is NOT going through the VPN.")

        

if __name__ == "__main__":
    # Provide the path to your .ovpn configuration file
    config_path = "Sample.ovpn"
    
    # Specify the path to the OpenVPN executable
    openvpn_path = "path to openvpn.exe"

    # Connect to OpenVPN and verify routing
    connect_openvpn(config_path, openvpn_path)
    
