#!/bin/bash

SERVER="8.8.8.8"
LOG_FILE="logs/health.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

ping -c 1 $SERVER > /dev/null 2>&1

if [ $? -ne 0 ]; then
  echo "[$TIMESTAMP] Server unreachable" >> $LOG_FILE
else
  echo "[$TIMESTAMP] Server is healthy" >> $LOG_FILE
fi
