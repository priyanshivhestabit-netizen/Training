# Day 1 – System Reverse Engineering + Node & Terminal

## Objective
The goal of this task was to understand how a **Linux system exposes low-level information** and how it can be inspected using **Node.js core modules**, **terminal commands**, and **shell configuration**—without using any external libraries or frameworks.


## What I built
I created a small **system inspection toolkit** consisting of:

- A **Node.js script (`sysinfo.js`)** that retrieves system and network information
- **Shell aliases** to improve terminal productivity
- A **Node.js metrics logger (`symmetrics.js`)** that captures runtime CPU and resource usage
- A **JSON log file** to store system metrics in a structured format

## What I learned

### 1- System Information via Node.js
Learned how to extract system-level data using Node.js core modules:
- Used the `os` module to retrieve the **hostname**
- Used `child_process.execSync()` to execute Linux commands from Node.js
- Parsed command output to display meaningful system details

System data collected includes:
- Hostname
- Available disk space
- Open network ports
- Default network gateway
- Logged-in users count


### 2- Linux Networking & System Commands
Worked with core Linux utilities to inspect the system:
- `df -h` for disk usage
- `ss -tuln` for open TCP/UDP ports
- `ip route` and `route -n` to find the default gateway
- `who | wc -l` to count active user sessions


### 3- Shell Aliases 
Created reusable shell aliases in `.bashrc` to speed up common workflows:
- `gs` → quick git status checks
- `files` → detailed file listings
- `ports` → inspect listening ports instantly


### 4- Node.js Runtime Metrics
Used:
- `process.cpuUsage()`
- `process.resourceUsage()`

Captured metrics include:
- CPU time (user & system)
- Memory usage
- Page faults
- Context switches
- File system operations

These metrics were stored in a structured JSON file for later analysis.


## Files Used
- `sysinfo.js` – Collects and prints system and network information
- `symmetrics.js` – Logs Node.js runtime metrics
- `logs/day1-symmetrics.json` – Stored CPU and resource usage data
- `.bashrc` – Shell aliases configuration


## Output
A functional **system inspection and monitoring setup** built using Linux commands and Node.js core APIs. The scripts successfully retrieve live system data and store runtime metrics in a structured format, forming a strong foundation for advanced system diagnostics and automation in later stages.
