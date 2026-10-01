# AI Class Local Server

A self-contained local web server that lets a teacher's Windows laptop act as the
file-distribution hub for a 90-minute middle-school AI lesson built around
[Google Teachable Machine](https://teachablemachine.withgoogle.com/). Students connect
over the classroom Wi-Fi/LAN, download the phase they're told to use, and train an
image classifier — with **no camera**, **no external image search**, and **no dataset
downloads from the internet**. Only the AI training tool itself needs real internet
access; the lesson files travel entirely over the local network.

This repository holds the finished, tested package: the student-facing pages, the
lesson ZIPs, and the two Windows server implementations behind them.

The core lesson is phases 1–7, scheduled minute-by-minute across 90 minutes. An
optional **Phase 8 — Expert Challenge** bonus is included for early finishers or a
follow-up session: 8 procedurally-generated images (matching the exact visual style
of the training set), each built to test one specific way an image classifier can be
fooled — color-only shortcuts, orientation, scale, clutter, and contrast — rather than
just "harder to see." See `TEACHER_NOTES.txt` inside the Phase 8 ZIP for the framing.

## The problem this solves

The lesson needed every student in a room to grab the same curated set of training
and test images, phase by phase, without:

- requiring a camera (privacy/safety),
- letting students search the open web for images (unpredictable, off-task), or
- depending on school IT to host anything.

The solution: the teacher's own laptop serves the files locally. Nothing leaves the
building, nothing needs installing, and the only non-local dependency is the
Teachable Machine site itself (and, optionally, Quick, Draw! for the Phase 1 warm-up).

## How it works

```
Teacher laptop (this repo, unzipped)                    Student browser
┌─────────────────────────────────┐                      ┌────────────┐
│ START_SERVER_WINDOWS.bat         │   same Wi-Fi/LAN     │  Chrome /  │
│  -> py -m http.server --bind     │◄────────────────────►│  Edge etc. │
│     0.0.0.0 8000                 │  http://TEACHER-IP   │            │
│  (falls back automatically to    │  :8000                │ 1. open    │
│   server.ps1 if Python is        │                      │ 2. click   │
│   missing)                       │                      │    a phase │
│                                   │                      │ 3. extract │
│ Root = this folder               │                      │    the ZIP │
│  ├─ index.html / index-ar.html   │                      │ 4. upload  │
│  ├─ teacher_qr.html              │                      │    to      │
│  └─ downloads/*.zip              │                      │  Teachable │
└─────────────────────────────────┘                      │  Machine   │
                                                            └────────────┘
```

The socket binds to `0.0.0.0:8000`, so it answers on `127.0.0.1`, the Wi-Fi IP, and
any other local interface through the same listening socket. Every request is
resolved to a canonical filesystem path and checked against the server root before
anything is read from disk — `..`, absolute paths, and encoded traversal tricks are
all rejected rather than served. Only `GET`/`HEAD` are handled: there is no upload
endpoint and no way to browse or modify anything else on the laptop.

## What's in the repository

| Path | Purpose |
|---|---|
| `START_SERVER_WINDOWS.bat` | The only file a teacher needs to run. Detects Python, starts the server, opens the page automatically, and detects/avoids starting a duplicate server if one is already running. Falls back to the PowerShell server below if Python isn't installed. |
| `server.ps1` | A from-scratch HTTP file server (`System.Net.HttpListener`) used only when Python is unavailable. Needs Administrator rights once (self-elevates via UAC) because Windows restricts non-loopback `HttpListener` binding to admins — Python's raw sockets don't have this restriction, which is why Python is the preferred path. |
| `index.html` / `index-ar.html` | The student download page, in English and Arabic (full RTL layout), each linking to the other. |
| `teacher_qr.html` | An optional, offline, teacher-only page that generates a QR code for whatever address the server is actually running on, so students can scan instead of typing. |
| `downloads/` | The lesson ZIPs: a MASTER bundle, an already-expanded "Expanded" bundle, one ZIP per core phase (1–7), and an optional bonus Phase 8. |
| `README_FIRST.txt` | The plain-language operational guide for the teacher: quick start, troubleshooting, firewall notes, network scenarios. |
| `START_SERVER_LINUX_MAC.sh` | Equivalent launcher for Linux/macOS, included for completeness. |

## Notable engineering decisions

A few things in here exist because an earlier, simpler version of them didn't hold up
under real testing:

- **Path-traversal fix.** The original boundary check compared paths with a plain
  string `StartsWith`, which would also match an unrelated sibling folder whose name
  happened to share the same prefix (e.g. `AI_Class_Local_Server_OLD`). Fixed by
  comparing against the root plus a trailing separator.
- **Crash hardening.** A single malformed request (an embedded `%00`, or a
  drive-letter-looking path segment like `/C:/Windows/win.ini`) threw an unhandled
  exception that escaped the server's request loop and killed the entire process —
  silently ending class for everyone. The whole per-request body is now wrapped so a
  bad request gets a 400/403/404, never a dead server.
- **No "download as folder" option.** This was built once, using the File System
  Access API, and then removed. That API is only available in a secure context
  (HTTPS or literally `localhost`), never on a plain `http://192.168.x.x` address —
  which is exactly how every student reaches this server. The only thing it could
  actually offer over plain HTTP was downloading every image individually, which
  tested worse than a ZIP. ZIP + Windows' built-in "Extract All" remains the only
  reliable one-click-to-one-folder path here.
- **Automatic duplicate-server detection.** Re-running the launcher while a server is
  already up just reopens the existing page instead of starting a second process —
  added after repeated manual test runs left multiple stale browser tabs pointing at
  servers that had since been closed, which produced confusing "can't connect"
  failures on an otherwise-working file.
- **IPv4 auto-detection.** `ipconfig` alone isn't enough on a machine with Hyper-V,
  VPN, or WSL virtual adapters present — a teacher could easily copy a virtual
  switch's address instead of the real Wi-Fi one. The launcher filters out loopback,
  link-local, and known-virtual adapter names, then lists real candidates with the
  Wi-Fi adapter prioritized first.

## Security model

- Serves only files inside this folder; nothing else on the laptop is reachable.
- Read-only: `GET`/`HEAD` only, no upload endpoint, no directory write access.
- No personal files belong in this folder — it is network-exposed by design while the
  server is running.
- Intended for a trusted classroom LAN/Wi-Fi, not a public network. Not intended to be
  exposed to the public internet (no port forwarding, no tunneling by default).

## Running it

See [`README_FIRST.txt`](README_FIRST.txt) for the full step-by-step teacher guide.
Short version: unzip, double-click `START_SERVER_WINDOWS.bat`, read the address it
shows you, give that address to students.
