import sys
from scapy.all import ICMP, IP, sr1
from netaddr import IPNetwork

def ping_sweep(network_with_netmask):
    live_hosts = []
    total_hosts = 0
    scanned_hosts = 0

    # Use IPNetwork directly without manually concatenating network and netmask
    ip_network = IPNetwork(network_with_netmask)
    
    # Count total hosts first (not strictly necessary but gives good feedback)
    total_hosts = len(list(ip_network.iter_hosts()))
    
    for host in ip_network.iter_hosts():
        scanned_hosts += 1
        print(f"Scanning: {scanned_hosts}/{total_hosts}", end="\r")

        # Send an ICMP packet and set a timeout for 1 second
        response = sr1(IP(dst=str(host))/ICMP(), timeout=1, verbose=0)

        if response is not None:
            live_hosts.append(str(host))
            print(f"Host {host} is online.")

    return live_hosts

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ping_sweep.py <network_with_netmask>")
        sys.exit(1)

    # Network with netmask in CIDR format (e.g., 192.168.1.0/24)
    network_with_netmask = sys.argv[1]

    live_hosts = ping_sweep(network_with_netmask)
    print("\nCompleted")
    print(f"Live hosts: {live_hosts}")
