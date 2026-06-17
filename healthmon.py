#!/usr/bin/env python3

"""
Name: Patricia Kahongya
Date: June 2026
Course: SEC 444
Version: 2.0
Script: healthmon.py

Health monitoring script using configurable thresholds.
Checks disk usage, memory usage, CPU load, and service status.
Logs results to a main log file, writes alerts to an alert log,
and sends alerts to syslog when thresholds are breached.
"""

import json
import logging
import logging.handlers
import os
import shutil
import subprocess
import sys


def load_config(config_file):
    """Load configuration from a JSON file."""
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("ERROR: Config file not found. Please provide a valid config.json file.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("ERROR: Config file is not valid JSON. Please fix the config file.")
        sys.exit(1)


def setup_logging(log_file):
    """Configure logging to write to the main log file."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True
    )


def write_syslog(message):
    """Write alert messages to syslog."""
    try:
        syslog = logging.handlers.SysLogHandler(address="/dev/log")
        logger = logging.getLogger("healthmon_syslog")
        logger.setLevel(logging.WARNING)

        if not logger.handlers:
            logger.addHandler(syslog)

        logger.warning(message)
    except OSError:
        logging.warning("Unable to write to syslog")


def log_alert(alert_file, message):
    """Write alerts to alert log, syslog, and main log."""
    with open(alert_file, "a", encoding="utf-8") as file:
        file.write(message + "\n")

    write_syslog(message)
    logging.warning(message)


def check_disk(threshold, alert_file):
    """Check disk usage against configured threshold."""
    usage = shutil.disk_usage("/")
    percent = (usage.used / usage.total) * 100

    logging.info("Disk usage: %.2f%%", percent)

    status = "OK"
    if percent > threshold:
        status = "ALERT"
        log_alert(
            alert_file,
            f"ALERT: Disk usage exceeded threshold ({percent:.2f}%)"
        )

    return {
        "check": "Disk Usage",
        "value": f"{percent:.2f}%",
        "threshold": f"{threshold}%",
        "status": status,
    }


def check_memory(threshold, alert_file):
    """Check memory usage against configured threshold."""
    try:
        result = subprocess.check_output(["free"]).decode().splitlines()
        memory = result[1].split()

        total = int(memory[1])
        used = int(memory[2])
        percent = (used / total) * 100
    except (subprocess.SubprocessError, IndexError, ValueError) as error:
        logging.error("Memory check failed: %s", error)
        return {
            "check": "Memory Usage",
            "value": "Unavailable",
            "threshold": f"{threshold}%",
            "status": "ERROR",
        }

    logging.info("Memory usage: %.2f%%", percent)

    status = "OK"
    if percent > threshold:
        status = "ALERT"
        log_alert(
            alert_file,
            f"ALERT: Memory usage exceeded threshold ({percent:.2f}%)"
        )

    return {
        "check": "Memory Usage",
        "value": f"{percent:.2f}%",
        "threshold": f"{threshold}%",
        "status": status,
    }


def check_cpu(threshold, alert_file):
    """Check CPU load average against configured threshold."""
    load = os.getloadavg()[0]

    logging.info("CPU load (1 min): %.2f", load)

    status = "OK"
    if load > threshold:
        status = "ALERT"
        log_alert(
            alert_file,
            f"ALERT: CPU load exceeded threshold ({load:.2f})"
        )

    return {
        "check": "CPU Load 1 Min",
        "value": f"{load:.2f}",
        "threshold": str(threshold),
        "status": status,
    }


def check_services(services, alert_file):
    """Check whether configured services are active."""
    results = []

    for service in services:
        result = subprocess.run(
            ["systemctl", "is-active", service],
            capture_output=True,
            text=True,
            check=False
        )

        status_text = result.stdout.strip()
        logging.info("%s: %s", service, status_text)

        status = "OK"
        if status_text != "active":
            status = "ALERT"
            log_alert(
                alert_file,
                f"ALERT: Service {service} is not running"
            )

        results.append({
            "check": f"Service: {service}",
            "value": status_text,
            "threshold": "active",
            "status": status,
        })

    return results


def run_checks(config):
    """Run all health checks and return summary results."""
    logging.info("Running health checks")

    summary = []

    summary.append(check_disk(
        config["checks"]["disk_usage_percent"],
        config["alert_log"]
    ))

    summary.append(check_memory(
        config["checks"]["memory_usage_percent"],
        config["alert_log"]
    ))

    summary.append(check_cpu(
        config["checks"]["cpu_load_1min"],
        config["alert_log"]
    ))

    summary.extend(check_services(
        config["checks"]["services"],
        config["alert_log"]
    ))

    return summary


def display_summary(summary):
    """Display health check summary report to the screen."""
    print("\nHealth Monitoring Summary")
    print("-------------------------")

    for item in summary:
        print(
            f"{item['check']}: "
            f"Value={item['value']} | "
            f"Threshold={item['threshold']} | "
            f"Status={item['status']}"
        )

    print("\nSummary complete. Results were also written to the log file.")


def main():
    """Main program."""
    if len(sys.argv) not in [2, 3]:
        print("Usage: python3 healthmon.py <config.json> [--check]")
        sys.exit(1)

    config = load_config(sys.argv[1])
    setup_logging(config["log_file"])

    if len(sys.argv) == 3 and sys.argv[2] != "--check":
        print("Invalid option. Use --check")
        sys.exit(1)

    manual_check = len(sys.argv) == 3 and sys.argv[2] == "--check"

    if manual_check:
        logging.info("Running manual check with --check flag")

    summary = run_checks(config)

    if manual_check:
        display_summary(summary)


if __name__ == "__main__":
    main()
