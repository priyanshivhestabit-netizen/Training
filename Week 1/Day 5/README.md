# Day 5 – Automation & Mini-CI Pipeline

## Objective
The goal of this task was to understand and implement **basic automation, scripting, and CI-style validation** using Bash, Git hooks, packaging, and cron scheduling.

This simulates a **mini CI pipeline** without using external tools like GitHub Actions.


## What I Built

### 1- Health Monitoring Script (`healthcheck.sh`)

A Bash script that:
- Pings a server every **10 seconds**
- Logs failures to `logs/health.log`
- Runs continuously until stopped

This demonstrates:
- Infinite loops
- Exit status handling
- Logging
- Process control


### 2- Pre-Commit Validation (Husky)

A Git pre-commit hook that ensures:

- `.env` file does NOT exist in Git
- JavaScript files are properly formatted
- Log files are ignored

This simulates:
- Basic CI validation rules
- Preventing sensitive file commits


### 3- Packaging System

Created a versioned bundle:

```
bundle-<timestamp>.zip
```

The bundle includes:
- `src/`
- `logs/`
- `docs/`

This demonstrates:
- Build artifact creation
- Timestamp-based versioning
- Structured packaging

---

### 4- Checksum Verification

Generated a SHA1 checksum file:

```
checksums.sha1
```

This ensures:
- File integrity validation
- Artifact verification after transfer


### 5- Cron Job Scheduling

Configured a cron job to run:

```
healthcheck.sh
```

Every 5 minutes.

This demonstrates:
- Task automation
- Background scheduling
- System-level process management



## Deliverables

- `healthcheck.sh`
- Husky pre-commit hook (failed & passed screenshots)
- `bundle-*.zip`
- `checksums.sha1`
- Screenshot of scheduled cron job


