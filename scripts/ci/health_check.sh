#!/usr/bin/env bash
# Simple health check helper: poll a URL until it returns 2xx or timeout
set -euo pipefail

URL=${1:-}
TIMEOUT=${2:-60}

if [ -z "$URL" ]; then
  echo "Usage: $0 <url> [timeout_seconds]"
  exit 2
fi

echo "Health check: $URL (timeout ${TIMEOUT}s)"
SECS=0
while [ $SECS -lt $TIMEOUT ]; do
  if curl -sSf --max-time 5 "$URL" >/dev/null 2>&1; then
    echo "Healthy: $URL"
    exit 0
  fi
  sleep 2
  SECS=$((SECS+2))
done

echo "Health check timed out for $URL"
exit 1
