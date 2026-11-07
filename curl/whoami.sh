#!/usr/bin/env bash
# Prints the exit IP twice with rotation, then twice with one sticky session.
set -euo pipefail

host="${LUDAX_HOST:-gw.ludaxproxy.com}:${LUDAX_PORT:-7777}"
url="https://api.ludaxproxy.com/whoami"

echo "Rotating:"
for _ in 1 2; do
  curl -sS -x "http://$host" -U "$LUDAX_USERNAME:$LUDAX_PASSWORD" "$url"; echo
done

echo "Sticky:"
token="demo$RANDOM"
for _ in 1 2; do
  curl -sS -x "http://$host" -U "$LUDAX_USERNAME:$LUDAX_PASSWORD-session-$token-time-10" "$url"; echo
done
