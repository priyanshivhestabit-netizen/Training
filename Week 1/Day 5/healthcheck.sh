#!/bin/bash

SERVER="192.0.2.1"
LOG_FILE="logs/health.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

while true
do
  TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

  if ! ping -c 1 $SERVER > /dev/null 2>&1
  then
    echo "[$TIMESTAMP] Server unreachable" >> $LOG_FILE
  fi

  sleep 10
done
