# sprint_scripts
# Sprint 4 - Health Monitoring Script

## Author

Patricia Kahongya

## Course

SEC 444

## Description

healthmon.py is a Python health monitoring script that checks:

* Disk usage
* Memory usage
* CPU 1-minute load average
* Service status (ssh and cron)

Thresholds are configured through config.json.

The script logs results to a log file and writes alerts to a separate alert log and syslog when thresholds are exceeded.

## Files

### healthmon.py

Main health monitoring script.

### config.json

Configuration file containing:

* Disk threshold
* Memory threshold
* CPU threshold
* Services to monitor
* Log file locations

## Usage

Run health checks:

```bash
python3 healthmon.py config.json
```

Run manual check:

```bash
python3 healthmon.py config.json --check
```

## Logging

Main log:

```text
/home/patriciakahongya36/healthmon.log
```

Alert log:

```text
/home/patriciakahongya36/alerts.log
```

## Cron Schedule

Configured to run every 5 minutes:

```bash
*/5 * * * * /usr/bin/python3 /home/patriciakahongya36/sprint_scripts/healthmon.py /home/patriciakahongya36/sprint_scripts/config.json
```

