#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "================================================================="
echo "  AI CLASS LOCAL DISTRIBUTION SERVER (AGES 14-16)"
echo "  Connect Students on ANY Network (Wi-Fi, Hotspot, or LAN)"
echo "================================================================="
echo

# Port 8000 matches START_SERVER_WINDOWS.bat. The Node server (server.js) is optional:
# it is used only if `npm install` has been run, otherwise Python's built-in server is used.
PORT=${PORT:-8000}

echo "[Detecting Local Network IP Addresses...]"
if command -v hostname >/dev/null 2>&1 && hostname -I >/dev/null 2>&1; then
    for ip in $(hostname -I); do
        echo "  -> http://$ip:$PORT"
    done
elif command -v ip >/dev/null 2>&1; then
    ip -4 addr show | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | while read -r ip; do
        if [ "$ip" != "127.0.0.1" ]; then
            echo "  -> http://$ip:$PORT"
        fi
    done
elif command -v ifconfig >/dev/null 2>&1; then
    ifconfig | grep "inet " | awk '{print $2}' | while read -r ip; do
        if [ "$ip" != "127.0.0.1" ]; then
            echo "  -> http://$ip:$PORT"
        fi
    done
fi

echo
echo "-----------------------------------------------------------------"
echo "CONNECTING FROM ANY NETWORK:"
echo "1. Same Wi-Fi: Students open http://YOUR-IP:$PORT"
echo "2. School Wi-Fi Blocking? Connect teacher & students to a phone Hotspot,"
echo "   or use the Cloud URL: https://ais-pre-rp4wyeuhw3rca3whcrxqjw-551148841539.europe-west2.run.app"
echo "3. Offline Teacher QR generator: http://localhost:$PORT/teacher_qr.html"
echo "-----------------------------------------------------------------"
echo

if command -v node >/dev/null 2>&1 && [ -d node_modules/express ]; then
    echo "[OK] Node.js + Express detected. Starting server on 0.0.0.0:$PORT..."
    echo "Keep this terminal open during class. Press Ctrl+C to stop."
    echo
    PORT="$PORT" node server.js
elif command -v python3 >/dev/null 2>&1; then
    echo "[OK] Python 3 detected. Starting HTTP server on 0.0.0.0:$PORT..."
    echo "Keep this terminal open during class. Press Ctrl+C to stop."
    echo
    python3 -m http.server "$PORT" --bind 0.0.0.0
elif command -v python >/dev/null 2>&1; then
    echo "[OK] Python detected. Starting HTTP server on 0.0.0.0:$PORT..."
    echo "Keep this terminal open during class. Press Ctrl+C to stop."
    echo
    python -m http.server "$PORT" --bind 0.0.0.0
else
    echo "[ERROR] Neither Node.js nor Python was found. Please install one and try again."
    exit 1
fi
