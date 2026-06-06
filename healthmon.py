#!/usr/bin/env python3

"""
Name: Patricia Kahongya
Date: June 2026
Course: SEC 444
Script: healthmon.py

Health monitoring script using configurable thresholds.
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
    with open(config_file, "r", encoding="utf-8") as file:
        return json.load(file)


def setup_logging(log_file):
    """Configure logging to write to the main log file."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def write_syslog(message):
    """Write alert messages to syslog."""
    try:
        syslog = logging.handlers.SysLogHandler(address="/dev/log")
        logger = logging.getLogger("healthmon_syslog")
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

    logging.info(f"Disk usage: {percent:.2f}%")

    if percent > threshold:
        log_alert(
            alert_file,
            f"ALERT: Disk usage exceeded threshold ({percent:.2f}%)"
        )


def check_memory(threshold, alert_file):
    """Check memory usage against configured threshold."""
    result = subprocess.check_output(["free"]).decode().splitlines()
    memory = result[1].split()

    total = int(memory[1])
    used = int(memory[2])
    percent = (used / total) * 100

    logging.info(f"Memory usage: {percent:.2f}%")

    if percent > threshold:
        log_alert(
            alert_file,
            f"ALERT: Memory usage exceeded threshold ({percent:.2f}%)"
        )


def check_cpu(threshold, alert_file):
    """Check CPU load average against configured threshold."""
    load = os.getloadavg()[0]

    logging.info(f"CPU load (1 min): {load:.2f}")

    if load > threshold:
        log_alert(
            alert_file,
            f"ALERT: CPU load exceeded threshold ({load:.2f})"
        )


def check_services(services, alert_file):
    """Check whether configured services are active."""
    for service in services:
        result = subprocess.run(
            ["systemctl", "is-active", service],
            capture_output=True,
            text=True,
            check=False
        )

        status = result.stdout.strip()
        logging.info(f"{service}: {status}")

        if status != "active":
            log_alert(
                alert_file,
                f"ALERT: Service {service} is not running"
            )


def run_checks(config):
    """Run all health checks."""
    logging.info("Running health check summary")

    check_disk(
        config["checks"]["disk_usage_percent"],
        config["alert_log"]
    )

    check_memory(
        config["checks"]["memory_usage_percent"],
        config["alert_log"]
    )

    check_cpu(
        config["checks"]["cpu_load_1min"],
        config["alert_log"]
    )

    check_services(
        config["checks"]["services"],
        config["alert_log"]
    )


def main():
    """Main program."""

    if len(sys.argv) not in [2, 3]:
        logging.error("Usage: python3 healthmon.py <config.json> [--check]")
        sys.exit(1)

    config = load_config(sys.argv[1])
    setup_logging(config["log_file"])

    if len(sys.argv) == 3 and sys.argv[2] != "--check":
        logging.error("Invalid option. Use --check")
        sys.exit(1)

    if len(sys.argv) == 3 and sys.argv[2] == "--check":
        logging.info("Running manual check with --check flag")

    run_checks(config)


if __name__ == "__main__":
    main()
