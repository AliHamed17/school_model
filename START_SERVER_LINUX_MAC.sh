#!/usr/bin/env bash
cd "$(dirname "$0")"
echo
echo "AI CLASS LOCAL SERVER"
echo "Students should open: http://YOUR-IP:8000"
echo "Keep this terminal open. Ctrl+C stops the server."
echo

if command -v python3 >/dev/null 2>&1; then
    python3 -m http.server 8000 --bind 0.0.0.0
elif command -v python >/dev/null 2>&1; then
    python -m http.server 8000 --bind 0.0.0.0
else
    echo "ERROR: Python was not found. Install Python 3 and try again."
    exit 1
fi
