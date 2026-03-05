# Linux Inside Docker Container

## Base Image
node:20-alpine

## Working Directory
/app

## Running Process
node app.js

## Observations

- Container runs as root user
- Node process visible in ps
- Minimal Linux OS (Alpine)
- Disk usage minimal