@echo off
setlocal enabledelayedexpansion
title AI Class Local Server
color 0b

echo =================================================================
echo   AI CLASS LOCAL DISTRIBUTION SERVER (AGES 14-16)
echo   Connect Students on ANY Network (Wi-Fi, Hotspot, or LAN)
echo =================================================================
echo.

cd /d "%~dp0"

echo [Detecting Network IP Addresses on this machine...]
ipconfig | findstr /i "IPv4"
echo.
echo -----------------------------------------------------------------
echo CONNECTING FROM ANY NETWORK:
echo 1. Local Wi-Fi: Give students one of the IP addresses above on port 3000
echo    Example: http://192.168.1.25:3000
echo.
echo 2. School Wi-Fi Isolation (AP Isolation) Workaround:
echo    If student devices cannot reach your laptop, connect teacher and
echo    student devices to a phone Personal Hotspot, or use the Cloud URL:
echo    https://ais-pre-rp4wyeuhw3rca3whcrxqjw-551148841539.europe-west2.run.app
echo.
echo 3. Teacher QR code: http://localhost:3000/teacher_qr.html
echo -----------------------------------------------------------------
echo.

:: Check for Node.js first
where node >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] Node.js detected. Starting production server on 0.0.0.0:3000...
    echo Keep this window open during class. Press Ctrl+C to stop.
    echo.
    node server.js
    goto :eof
)

:: Fallback to Python 3
where py >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] Python detected. Starting HTTP server on 0.0.0.0:3000...
    echo Keep this window open during class. Press Ctrl+C to stop.
    echo.
    py -m http.server 3000 --bind 0.0.0.0
    goto :eof
)

where python >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] Python detected. Starting HTTP server on 0.0.0.0:3000...
    echo Keep this window open during class. Press Ctrl+C to stop.
    echo.
    python -m http.server 3000 --bind 0.0.0.0
    goto :eof
)

echo [ERROR] Neither Node.js nor Python was found on this system.
echo Please install Node.js (https://nodejs.org) or Python (from Microsoft Store)
echo and run this file again.
pause
