param([int]$Port = 8000)

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootFull = [System.IO.Path]::GetFullPath($Root)
$RootPrefix = $RootFull.TrimEnd('\') + '\'

$Listener = New-Object System.Net.HttpListener
$Listener.Prefixes.Add("http://+:$Port/")

try {
    $Listener.Start()
} catch {
    Write-Host ""
    Write-Host "Could not start the PowerShell server." -ForegroundColor Red
    if ($_.Exception.Message -match "denied") {
        Write-Host "Reason: Windows blocked binding to the network on port $Port (Access is denied)." -ForegroundColor Yellow
        Write-Host "This backup server needs Administrator rights to accept connections from"
        Write-Host "other devices. Close this window and run START_SERVER_WINDOWS.bat again -"
        Write-Host "it will request Administrator rights automatically (a Windows permission prompt)."
    } elseif ($_.Exception.Message -match "conflict|already") {
        Write-Host "Reason: port $Port is already in use by another program." -ForegroundColor Yellow
        Write-Host "Close the other program, or run this script with a different port, e.g.:"
        Write-Host "  powershell -File server.ps1 -Port 8001"
    } else {
        Write-Host $_.Exception.Message
    }
    Write-Host ""
    Read-Host "Press Enter to close"
    exit 1
}

Write-Host ""
Write-Host "AI CLASS LOCAL SERVER (PowerShell)" -ForegroundColor Cyan
Write-Host "Serving folder: $RootFull"
Write-Host "Port: $Port"
Write-Host ""
Write-Host "Students open: http://YOUR-IP:$Port"
Write-Host "Press Ctrl+C to stop."
Write-Host ""

$Mime = @{
    ".html"="text/html; charset=utf-8"
    ".htm" ="text/html; charset=utf-8"
    ".txt" ="text/plain; charset=utf-8"
    ".zip" ="application/zip"
    ".png" ="image/png"
    ".jpg" ="image/jpeg"
    ".jpeg"="image/jpeg"
    ".css" ="text/css; charset=utf-8"
    ".js"  ="application/javascript; charset=utf-8"
    ".ico" ="image/x-icon"
    ".json"="application/json; charset=utf-8"
    ".xlsx"="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
}

while ($Listener.IsListening) {
    try {
        $Context = $Listener.GetContext()
    } catch {
        break
    }

    try {
        $Request = $Context.Request
        $Response = $Context.Response

        if ($Request.HttpMethod -ne 'GET' -and $Request.HttpMethod -ne 'HEAD') {
            $Response.StatusCode = 405
            continue
        }

        $RequestPath = [Uri]::UnescapeDataString($Request.Url.AbsolutePath.TrimStart('/'))
        if ([string]::IsNullOrWhiteSpace($RequestPath)) { $RequestPath = "index.html" }

        $FullPath = $null
        $IsSafe = $false
        try {
            $FullPath = [System.IO.Path]::GetFullPath((Join-Path $RootFull $RequestPath))
            $IsSafe = $FullPath.Equals($RootFull, [StringComparison]::OrdinalIgnoreCase) -or
                      $FullPath.StartsWith($RootPrefix, [StringComparison]::OrdinalIgnoreCase)
        } catch {
            $IsSafe = $false
        }

        if (-not $IsSafe) {
            $Response.StatusCode = 403
            continue
        }

        if (Test-Path -LiteralPath $FullPath -PathType Leaf) {
            try {
                $Bytes = [System.IO.File]::ReadAllBytes($FullPath)
                $Ext = [System.IO.Path]::GetExtension($FullPath).ToLowerInvariant()
                if ($Mime.ContainsKey($Ext)) { $Response.ContentType = $Mime[$Ext] }
                else { $Response.ContentType = "application/octet-stream" }
                $Response.ContentLength64 = $Bytes.Length
                if ($Request.HttpMethod -eq 'GET') {
                    $Response.OutputStream.Write($Bytes, 0, $Bytes.Length)
                }
            } catch {
                $Response.StatusCode = 500
            }
        } else {
            $Response.StatusCode = 404
        }
    } catch {
        try { $Context.Response.StatusCode = 400 } catch {}
    } finally {
        try { $Context.Response.OutputStream.Close() } catch {}
    }
}
