#!/usr/bin/python3
# Parse an auth.log file and extract failed SSH login attempts
# Blue-20260413: Initial version

import csv
import os
import re
import sys

EXPECTED_ARG_COUNT = 3
CSV_HEADERS = ["timestamp", "source_ip", "username"]

FAILED_LOGIN_PATTERN = re.compile(
    r'^(?P<timestamp>[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}).*?'
    r'Failed password for (?:invalid user )?(?P<username>\S+) '
    r'from (?P<source_ip>\d{1,3}(?:\.\d{1,3}){3}) port \d+ ssh2$'
)


def print_usage():
    """Display correct script usage."""
    print("Usage: python3 logparser.py <logfile> <output.csv>")


def validate_arguments(arguments):
    """Validate command-line arguments."""
    if len(arguments) != EXPECTED_ARG_COUNT:
        print("Error: Wrong number of arguments.")
        print_usage()
        sys.exit(1)

    input_file = arguments[1]
    output_file = arguments[2]

    if not os.path.isfile(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    return input_file, output_file


def parse_failed_logins(log_file):
    """Parse failed SSH login attempts from auth log."""
    failed_attempts = []

    with open(log_file, "r", encoding="utf-8") as file_handle:
        for line in file_handle:
            match = FAILED_LOGIN_PATTERN.search(line.strip())

            if match:
                failed_attempts.append({
                    "timestamp": match.group("timestamp"),
                    "source_ip": match.group("source_ip"),
                    "username": match.group("username")
                })

    return failed_attempts


def write_csv(output_file, rows):
    """Write failed login attempts to CSV."""
    with open(output_file, "w", newline="", encoding="utf-8") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def print_results(rows):
    """Print parsed results to screen."""
    for row in rows:
        print(
            f"{row['timestamp']} | "
            f"{row['source_ip']} | "
            f"{row['username']}"
        )


def main():
    """Main script execution flow."""
    input_file, output_file = validate_arguments(sys.argv)
    failed_attempts = parse_failed_logins(input_file)

    print_results(failed_attempts)
    write_csv(output_file, failed_attempts)


if __name__ == '__main__':
    main()
