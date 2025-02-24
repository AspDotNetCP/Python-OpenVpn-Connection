# Python-OpenVpn-Connection
Simple Python Script to connect to DigitalOcean Droplets OpenVPNAS
# OpenVPN Client Script

This script allows you to connect to an OpenVPN server using a specified configuration file and verify the VPN connection by checking the public IP address and its geographical location.

## Prerequisites

- Python 3.x
- OpenVPN installed on your system
- Required Python packages: `requests`

## Installation

1. Clone the repository or download the script files.
2. Install the required Python package:
    ```sh
    pip install requests
    ```

## Usage

1. Provide the path to your `.ovpn` configuration file and the OpenVPN executable in the script:
    ```python
    config_path = "C:\\path\\to\\your\\config.ovpn"
    openvpn_path = "C:\\path\\to\\openvpn.exe"
    ```

2. Run the script:
    ```sh
    python main.py
    ```

## Functions

### `connect_openvpn(config_path, openvpn_path="openvpn")`
Connects to the OpenVPN server using the provided configuration file.

### `flush_dns_cache()`
Flushes the DNS cache based on the operating system.

### `get_vpn_ip()`
Gets the local VPN-assigned IP address.

### `get_public_ip()`
Checks the current public IPv4 address through the VPN connection.

### `get_public_ip_location(ip)`
Gets the geographical location of the public IP address.

### `check_vpn_status()`
Verifies if traffic is correctly routed through OpenVPN.

## License

This project is licensed under the MIT License.
