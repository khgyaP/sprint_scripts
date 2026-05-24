import nmap
import requests
import csv
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 netrecon.py <target_ip> <output.csv>")
        sys.exit(1)

    target = sys.argv[1]
    output_file = sys.argv[2]

    scanner = nmap.PortScanner()
    scanner.scan(target, arguments='-Pn')

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Host', 'Protocol', 'Port', 'State'])

        for host in scanner.all_hosts():
            for protocol in scanner[host].all_protocols():
                ports = scanner[host][protocol].keys()

                for port in ports:
                    state = scanner[host][protocol][port]['state']
                    writer.writerow([host, protocol, port, state])

    print(f"Scan results saved to {output_file}")

if __name__ == "__main__":
    main()
