# Sprint 5 – Ansible Automation

## Overview

This sprint demonstrates the use of Ansible to automate server configuration and application deployment across two Ubuntu Linux servers hosted in AWS.

## Environment

* Control Node: linux1
* Managed Nodes:

  * linux1
  * linux2

Ansible connectivity was verified using:

ansible all -i inventory.ini -m ping

Both hosts successfully responded with "pong".

## Files Included

* inventory.ini
* configure.yml
* deploy.yml
* healthmon.py
* config.json
* README.md

## configure.yml

The configure.yml playbook performs the following tasks:

* Installs required packages
* Creates a monitoring user
* Sets the system timezone
* Ensures rsyslog is installed and running
* Disables root SSH login
* Restarts SSH when configuration changes occur

Run with:

ansible-playbook -i inventory.ini configure.yml

## deploy.yml

The deploy.yml playbook performs the following tasks:

* Creates the application directory
* Copies healthmon.py
* Copies config.json
* Installs required Python packages
* Creates a cron job for automated monitoring

Run with:

ansible-playbook -i inventory.ini deploy.yml

## Validation

### Ansible Connectivity

Verified connectivity to both linux1 and linux2 using the Ansible ping module.

### Idempotency Test

configure.yml:

* First execution: changes detected and applied
* Second execution: changed=0

deploy.yml:

* First execution: changes detected and applied
* Second execution: changed=0

This confirms both playbooks are idempotent.

## Git Branch

sprint5-ansible

