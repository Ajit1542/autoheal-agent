#!/bin/bash

# Check disk space and alert if usage exceeds threshold
THRESHOLD=80
USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$USAGE" -gt "$THRESHOLD" ]; then
    echo "ALERT: Disk usage is at ${USAGE}%"
else
    echo "OK: Disk usage is at ${USAGE}%"
fi

