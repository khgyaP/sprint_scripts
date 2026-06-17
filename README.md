# Sprint 3 – netrecon.py

## Author

Patricia Kahongya

## Course

SEC 444

## Description

netrecon.py is a Python network reconnaissance script. It scans a target IP address for open ports using python-nmap and also queries a public geolocation API to collect location and ISP information.

The script combines scan results and geolocation data into one CSV output file and displays a summary report to the screen.

## Features

- Scans a target IP address for open ports
- Records port number, protocol, service name, and state
- Queries ip-api.com for geolocation data
- Collects country, region, city, and ISP
- Writes results to a CSV file
- Displays a screen summary
- Handles bad input and API failures gracefully

## Requirements

Install required system package:

```bash
sudo apt update
sudo apt install nmap -y
