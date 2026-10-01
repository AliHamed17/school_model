@echo off
title AI Class Local Server
cd /d "%~dp0"

where curl.exe >nul 2>&1
if %errorlevel%==0 (
    curl.exe -s -o NUL -m 1 "http://127.0.0.1:8000/"
) else (
    powershell -NoProfile -Command "try { Invoke-WebRequest 'http://127.0.0.1:8000/' -UseBasicParsing -TimeoutSec 1 | Out-Null; exit 0 } catch { exit 1 }"
)
if %errorlevel%==0 (
    echo.
    echo A server is already running on port 8000 - opening it instead of
    echo starting a second one. If this is not what you expected, close
    echo whichever other window is running the server first.
    echo.
    start "" "http://127.0.0.1:8000"
    pause
    exit /b
)

where py >nul 2>&1
if %errorlevel%==0 set PYCMD=py
if not defined PYCMD (
    where python >nul 2>&1
    if %errorlevel%==0 set PYCMD=python
)

if defined PYCMD goto :run_python

rem No Python found - use the built-in PowerShell server instead.
rem That one needs Administrator rights, so get them automatically if needed.
net session >nul 2>&1
if %errorlevel%==0 goto :run_powershell_elevated

echo.
echo =========================================
echo   AI CLASS LOCAL SERVER
echo =========================================
echo.
echo Python was not found, so this will use the backup method instead.
echo That needs Administrator rights on Windows - a permission prompt
echo will appear next. Click "Yes" to continue.
echo.
pause
powershell -NoProfile -Command "try { Start-Process -FilePath '%~f0' -Verb RunAs -ErrorAction Stop } catch { exit 1 }"
if %errorlevel% neq 0 (
    echo.
    echo Administrator rights were not granted, so the backup method can't run.
    echo Easiest fix: install Python from the Microsoft Store - it does not
    echo need Administrator rights - then run this file again.
    echo.
    pause
)
exit /b

:run_python
call :banner
start "" "http://127.0.0.1:8000"
%PYCMD% -m http.server 8000 --bind 0.0.0.0
goto :eof

:run_powershell_elevated
call :banner
start "" "http://127.0.0.1:8000"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0server.ps1" -Port 8000
pause
goto :eof

:banner
echo.
echo =========================================
echo   AI CLASS LOCAL SERVER
echo =========================================
echo.
echo Recommended IPv4 address(es) for students (best guess):
powershell -NoProfile -Command "$c = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*' -and $_.InterfaceAlias -notmatch 'Loopback|vEthernet|WSL|Virtual|Hyper-V|VPN|Tailscale|ZeroTier|Docker|Bluetooth' } | Sort-Object -Property @{Expression={$_.InterfaceAlias -match 'Wi-?Fi|Wireless'};Descending=$true}; if ($c) { $c | ForEach-Object { $n = ($_.InterfaceAlias -replace [char]0x200E,'') -replace [char]0x200F,''; '   {0,-28} {1}' -f $n, $_.IPAddress } } else { '   (none detected automatically - use the full list below)' }"
echo.
echo Full network details (for reference / troubleshooting):
ipconfig | findstr /i "IPv4"
echo.
echo This computer's own copy of the page is opening in your browser now.
echo Give STUDENTS the "Recommended" address above instead, like:
echo   http://YOUR-IP:8000
echo.
echo If Windows Firewall asks, click: Allow access on PRIVATE networks
echo.
echo Keep this window OPEN during the class. Press Ctrl+C to stop the server.
echo.
exit /b
