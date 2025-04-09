import ipaddress
import subprocess
import multiprocessing

def ping_host(ip):
    try:
        subprocess.run(
            ["ping", "-n", "1", "-w", "1", str(ip)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return ip, True
    except subprocess.CalledProcessError:
        return ip, False

def main(subnet):
    ip_network = ipaddress.IPv4Network(subnet, strict=False)
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() * 2)
    results = pool.map(ping_host, ip_network.hosts())
    return results

if __name__ == "__main__":
    subnet = input("Enter subnet (example: 192.168.1.1/24): ")
    scan_results = main(subnet)
    for ip, is_up in scan_results:
        print(f"{ip} is {'ONLINE' if is_up else 'OFFLINE'}")
