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
    ".mp4" ="video/mp4"
    ".csv" ="text/csv; charset=utf-8"
    ".svg" ="image/svg+xml"
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
                $Ext = [System.IO.Path]::GetExtension($FullPath).ToLowerInvariant()
                if ($Mime.ContainsKey($Ext)) { $Response.ContentType = $Mime[$Ext] }
                else { $Response.ContentType = "application/octet-stream" }
                $Response.AddHeader('Accept-Ranges', 'bytes')

                # HTTP Range support (browsers need it to jump around inside a video)
                $Len = (Get-Item -LiteralPath $FullPath).Length
                $Start = [int64]0
                $End = $Len - 1
                $Partial = $false
                $RangeHeader = $Request.Headers['Range']
                if ($RangeHeader -and ($RangeHeader.Trim() -match '^bytes=(\d*)-(\d*)$') -and ($Matches[1] -ne '' -or $Matches[2] -ne '')) {
                    if ($Matches[1] -ne '') {
                        $Start = [int64]$Matches[1]
                        if ($Matches[2] -ne '') { $End = [Math]::Min([int64]$Matches[2], $Len - 1) }
                    } else {
                        $Start = [Math]::Max([int64]0, $Len - [int64]$Matches[2])
                    }
                    if ($Start -ge $Len -or $Start -gt $End) {
                        $Response.StatusCode = 416
                        $Response.AddHeader('Content-Range', "bytes */$Len")
                        continue
                    }
                    $Partial = $true
                }
                $Count = $End - $Start + 1
                if ($Partial) {
                    $Response.StatusCode = 206
                    $Response.AddHeader('Content-Range', "bytes $Start-$End/$Len")
                }
                $Response.ContentLength64 = $Count
                if ($Request.HttpMethod -eq 'GET') {
                    $FS = [System.IO.File]::Open($FullPath, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
                    try {
                        [void]$FS.Seek($Start, [System.IO.SeekOrigin]::Begin)
                        $Buf = New-Object byte[] 65536
                        $Left = $Count
                        while ($Left -gt 0) {
                            $N = $FS.Read($Buf, 0, [int][Math]::Min([int64]$Buf.Length, $Left))
                            if ($N -le 0) { break }
                            $Response.OutputStream.Write($Buf, 0, $N)
                            $Left -= $N
                        }
                    } finally { $FS.Dispose() }
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
