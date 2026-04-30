# sprint_scripts
set up from AWS Linux box
Cybersecurity automation scripts 
# Sprint 2 - sysinfo.py

## Description
This script collects system information from a Linux machine and outputs the data in screen, CSV, or JSON format.

## Usage

```bash
python3 sysinfo.py screen
python3 sysinfo.py csv
python3 sysinfo.py json
```

## Output
- screen → prints information to terminal
- csv → creates sysinfo.csv
- json → creates sysinfo.json

## Information Collected
- Hostname
- OS information
- CPU cores
- Memory usage
- Disk usage
- IP address
- MAC address
- Uptime
- Logged-in users

## Platform
Developed and tested on a Linux AWS EC2 instance.