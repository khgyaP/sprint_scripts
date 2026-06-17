#!/usr/bin/env python3

"""
Name: Patricia Kahongya
Date: June 2026
Course: SEC 444
Version: 2.0
Script: netrecon.py

Description:
This script scans a target IP address for open ports using python-nmap.
It also queries a public geolocation API to collect country, region, city,
and ISP information about the target. Results are displayed to the screen
and written to a CSV file.
"""

import csv
import sys

import nmap
import requests


def validate_arguments():
    """Validate command-line arguments."""
    if len(sys.argv) != 3:
        print("Usage: python3 netrecon.py <target_ip> <output.csv>")
        sys.exit(1)

    return sys.argv[1], sys.argv[2]


def get_geolocation(target_ip):
    """Query a public geolocation API for target IP information."""
    url = f"http://ip-api.com/json/{target_ip}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "fail":
            return {
                "country": "Unavailable",
                "region": "Unavailable",
                "city": "Unavailable",
                "isp": "Unavailable",
            }

        return {
            "country": data.get("country", "Unavailable"),
            "region": data.get("regionName", "Unavailable"),
            "city": data.get("city", "Unavailable"),
            "isp": data.get("isp", "Unavailable"),
        }

    except requests.RequestException:
        return {
            "country": "Unavailable",
            "region": "Unavailable",
            "city": "Unavailable",
            "isp": "Unavailable",
        }


def scan_target(target_ip):
    """Scan the target IP address using Nmap and return open port data."""
    scanner = nmap.PortScanner()

    try:
        scanner.scan(target_ip, arguments="-Pn")
    except nmap.PortScannerError as error:
        print(f"Nmap scan error: {error}")
        sys.exit(1)
    except Exception as error:
        print(f"Unexpected scan error: {error}")
        sys.exit(1)

    results = []

    for host in scanner.all_hosts():
        for protocol in scanner[host].all_protocols():
            ports = scanner[host][protocol].keys()

            for port in ports:
                port_info = scanner[host][protocol][port]
                state = port_info.get("state", "unknown")
                service = port_info.get("name", "unknown")

                if state == "open":
                    results.append({
                        "host": host,
                        "protocol": protocol,
                        "port": port,
                        "service": service,
                        "state": state,
                    })

    return results


def write_csv(output_file, scan_results, geo_data):
    """Write scan and geolocation results to a CSV file."""
    try:
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "Host",
                "Protocol",
                "Port",
                "Service",
                "State",
                "Country",
                "Region",
                "City",
                "ISP",
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for result in scan_results:
                writer.writerow({
                    "Host": result["host"],
                    "Protocol": result["protocol"],
                    "Port": result["port"],
                    "Service": result["service"],
                    "State": result["state"],
                    "Country": geo_data["country"],
                    "Region": geo_data["region"],
                    "City": geo_data["city"],
                    "ISP": geo_data["isp"],
                })

    except OSError as error:
        print(f"Error writing CSV file: {error}")
        sys.exit(1)


def display_summary(target_ip, scan_results, geo_data, output_file):
    """Display a summary report to the screen."""
    print("\nNetwork Reconnaissance Summary")
    print("------------------------------")
    print(f"Target IP: {target_ip}")
    print(f"Country: {geo_data['country']}")
    print(f"Region: {geo_data['region']}")
    print(f"City: {geo_data['city']}")
    print(f"ISP: {geo_data['isp']}")
    print(f"Open Ports Found: {len(scan_results)}")

    if scan_results:
        print("\nOpen Port Details:")
        for result in scan_results:
            print(
                f"Port {result['port']}/{result['protocol']} "
                f"- {result['service']} - {result['state']}"
            )
    else:
        print("\nNo open ports found.")

    print(f"\nResults written to: {output_file}")


def main():
    """Main program function."""
    target_ip, output_file = validate_arguments()
    geo_data = get_geolocation(target_ip)
    scan_results = scan_target(target_ip)
    write_csv(output_file, scan_results, geo_data)
    display_summary(target_ip, scan_results, geo_data, output_file)


if __name__ == "__main__":
    main()
