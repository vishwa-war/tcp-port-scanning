# TCP Port Scanner

A multithreaded TCP port scanner written in Python that performs port discovery, banner grabbing, hostname resolution, and basic operating system fingerprinting using TTL analysis.

## Overview

This project is a lightweight network reconnaissance tool designed to scan TCP ports on a target host. It supports scanning a single port or performing a full-range aggressive scan across all TCP ports (1–65535).

The scanner uses concurrent execution to improve scanning performance and attempts to identify running services through banner grabbing. Additionally, it performs a simple operating system estimation by analyzing the TTL value returned from an ICMP ping response.

## Features

* TCP port scanning
* Single-port scanning mode
* Aggressive scan mode (ports 1–65535)
* Multithreaded scanning using `ThreadPoolExecutor`
* Banner grabbing for service identification
* Hostname-to-IP resolution
* Basic OS fingerprinting using TTL values
* Socket timeout handling
* Concurrent execution for faster results

## Technologies Used

* Python 3
* Socket Programming
* Threading
* Concurrent Futures (`ThreadPoolExecutor`)
* Subprocess
* Regular Expressions (`re`)

## Project Structure

```text
tcp-port-scanner/
│
├── scanner.py
├── README.md
```

## How It Works

### 1. Target Resolution

The program accepts either:

* Domain Name (example.com)
* IPv4 Address (192.168.1.1)

The hostname is resolved into an IP address using:

```python
socket.gethostbyname()
```

### 2. OS Detection

Before scanning begins, the script sends a ping request to the target and extracts the TTL value.

Typical TTL values:

| TTL Range | Likely Operating System |
| --------- | ----------------------- |
| 65 - 127  | Windows                 |
| 1 - 64    | Linux/Unix              |

Example:

```text
The Running Operating System is Likely Windows
```

### 3. Port Scanning

The scanner creates a TCP socket and attempts to connect to the specified port using:

```python
socket.connect_ex()
```

Return values:

* `0` → Port Open
* Non-zero → Port Closed

### 4. Banner Grabbing

When an open port is detected, the scanner attempts to receive service information:

```python
sock.recv(1024)
```

Example output:

```text
port 80 is open and the version is Apache/2.4.58
```

### 5. Aggressive Scanning

If the user enters:

```text
1
```

as the port number, the scanner launches an aggressive scan across all TCP ports:

```text
1 - 65535
```

using a pool of 100 worker threads.

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/tcp-port-scanner.git
cd tcp-port-scanner
```

### Verify Python Installation

```bash
python --version
```

Python 3.8+ is recommended.

## Usage

Run the script:

```bash
python scanner.py
```

### Example: Single Port Scan

```text
Enter Target URL or IP address: scanme.nmap.org
Enter Port Number or 1 for aggressive scan: 80
```

Output:

```text
The Running Operating System is Likely Linux
port 80 is open
```

### Example: Aggressive Scan

```text
Enter Target URL or IP address: scanme.nmap.org
Enter Port Number or 1 for aggressive scan: 1
```

Output:

```text
port 22 is open
port 80 is open
port 443 is open
```

## Code Components

### `scann()`

Responsible for:

* Single port scanning
* Launching aggressive scans
* Banner grabbing
* Reporting port status

### `scanall()`

Used by worker threads during aggressive scans to:

* Scan individual ports
* Detect open ports
* Perform banner grabbing

### Main Thread

Handles:

* User input
* Hostname resolution
* TTL analysis
* Thread creation and synchronization

## Performance Considerations

The scanner uses:

```python
ThreadPoolExecutor(max_workers=100)
```

to perform concurrent scans, significantly reducing the time required for full-range port scanning.

Factors affecting performance:

* Network latency
* Firewall rules
* Target responsiveness
* Socket timeout configuration

## Limitations

* Supports TCP scanning only.
* OS detection is based solely on TTL estimation and may be inaccurate.
* Banner grabbing depends on the target service sending data.
* Designed primarily for IPv4 environments.
* Closed ports are printed individually during single-port scans, which may create verbose output.

## Possible Improvements

Future enhancements may include:

* UDP port scanning
* Service fingerprinting database
* CIDR/range scanning
* Export results to CSV or JSON
* Colored terminal output
* Improved OS fingerprinting
* Scan progress indicators
* Custom thread pool sizing
* Logging support
* Cross-platform ping handling

## Security Notice

This tool is intended for:

* Educational purposes
* Security research
* Network administration
* Authorized penetration testing

Only scan systems and networks that you own or have explicit permission to assess. Unauthorized scanning may violate local laws, organizational policies, or service agreements.

## License

This project is released under the MIT License.

```text
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge,
to any person obtaining a copy of this software
and associated documentation files...
```

## Author

Developed using Python networking concepts, multithreading, and socket programming for educational and cybersecurity learning purposes.
