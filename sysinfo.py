#!/usr/bin/env python3

"""
sysinfo.py

Collects system information from a Linux machine and outputs it
to screen, CSV, or JSON format.
"""

import csv
import json
import os
import platform
import socket
import subprocess
import sys
from datetime import datetime


def run_command(command):
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode == 0:
            return result.stdout.strip()

        return "Unavailable"

    except Exception:
        return "Unavailable"


def get_ip_address():
    """Get IP address."""
    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.error:
        return "Unavailable"


def get_system_info():
    """Collect system information."""

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hostname": platform.node(),
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "cpu_cores": os.cpu_count(),
        "memory": run_command(["free", "-h"]),
        "disk_usage": run_command(["df", "-h", "/"]),
        "ip_address": get_ip_address(),
        "mac_address": run_command(
            ["cat", "/sys/class/net/eth0/address"]
        ),
        "uptime": run_command(["uptime", "-p"]),
        "logged_in_users": run_command(["who"]),
    }


def output_screen(data):
    """Print info to screen."""

    for key, value in data.items():
        print(f"{key}: {value}")


def output_csv(data):
    """Write info to CSV."""

    with open("sysinfo.csv", "w", newline="",
              encoding="utf-8") as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow(["Field", "Value"])

        for key, value in data.items():
            writer.writerow([key, value])

    print("Data written to sysinfo.csv")


def output_json(data):
    """Write info to JSON."""

    with open("sysinfo.json", "w",
              encoding="utf-8") as jsonfile:

        json.dump(data, jsonfile, indent=4)

    print("Data written to sysinfo.json")


def main():
    """Main program."""

    if len(sys.argv) != 2:
        print("Usage: python3 sysinfo.py <screen|csv|json>")
        sys.exit(1)

    output_format = sys.argv[1].lower()

    data = get_system_info()

    if output_format == "screen":
        output_screen(data)

    elif output_format == "csv":
        output_csv(data)

    elif output_format == "json":
        output_json(data)

    else:
        print("Invalid option.")
        print("Use: screen, csv, or json")
        sys.exit(1)


if __name__ == "__main__":
    main()