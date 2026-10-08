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

## Curriculum overview (Phases 1–10)

The core lesson is phases 1–7, scheduled minute-by-minute across 90 minutes. Phases 8–10
are optional extensions.

| Phase | Time | Focus | What students get |
|---|---|---|---|
| **1** | 0–15 min | Warm-up | Quick, Draw! pattern-recognition intro. |
| **2** | 15–47 min | Baseline training | 90 curated fruit images (Apple, Banana, Orange) for Teachable Machine. |
| **3** | 47–57 min | Easy test | 24 unseen test images and a results sheet that records all three percentages per image. |
| **4** | 57–67 min | Break the AI | 30 stress-test images (occlusion, slicing, lighting) and a failure report. |
| **5** | 67–75 min | Improve & retrain | Targeted extra data plus a separate validation set. |
| **6** | 75–87 min | Ambiguous challenge | Mixed and hybrid fruit images. |
| **7** | 87–90 min | Exit ticket | Reflection questions and a teacher answer key. |
| **8** | Bonus | Expert challenge | 8 images, each built to test one way a classifier can be fooled (colour shortcut, orientation, scale, clutter, contrast). |
| **9** | Bonus (advanced) | Adversarial Gauntlet | 12 attack images — out-of-distribution objects (tennis ball, basketball, traffic light), texture swaps, adversarial-patch stickers, checkerboard noise — then design a defensive 4th "Other" class. |
| **10** | Follow-up, ~45 min | Excel Data Lab | Turn the Phase 3 numbers into formulas and five charts in Excel, with an illustrated guide in English, Arabic and Hebrew. |

**Phase 10 — Excel Data Lab.** Students type the percentages Teachable Machine gave them
into a spreadsheet, calculate accuracy and confidence with formulas (`IF`, `INDEX/MATCH`,
`AVERAGEIF` …) and draw five charts: pie, column, line, **XY scatter** and **XYZ bubble**.
It comes with an illustrated step-by-step guide in **English, Arabic and Hebrew**
(right-to-left pages), a starter `.xlsx` and a finished answer-key `.xlsx` per language,
a printable results sheet, and teacher notes. Everything in it was checked against real
Microsoft Excel, not just written from memory (see "How Phase 10 was verified" below).

The English and Arabic student pages also include an in-browser **Red Team simulator**
for Phase 9: it shows why a softmax classifier with no "unknown" class answers with high
confidence on a tennis ball, how texture can beat shape, and what a confidence-threshold
guard or a 4th rejection class changes.

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
| `index.html` / `index-ar.html` | The student hub in English and Arabic (RTL), with the phase cards, filter tabs and the Red Team simulator. |
| `index-he.html` | The student download page in Hebrew (RTL). It uses a simpler layout and does not include the Red Team simulator. |
| `excel/` | Phase 10 as web pages: `guide-en/ar/he.html` (click a formula to copy it), `START_HERE.html` language chooser, `img/` (illustrations + real Excel charts), `files/` (starter and example workbooks). The same folder is zipped into `downloads/Phase_10_Excel_Data_Lab_FOLLOWUP.zip`. |
| `teacher_qr.html` | An optional, offline, teacher-only page that generates a QR code for whatever address the server is actually running on, so students can scan instead of typing. |
| `downloads/` | The lesson ZIPs: a MASTER bundle, an already-expanded "Expanded" bundle, one ZIP per phase (1–10). |
| `preview/` | Preview pictures for Phases 8 and 9, used by the student hub's inspect dialogs and the simulator. |
| `server.js`, `package.json`, `api/`, `vercel.json`, `.vercelignore`, `.env.example`, `metadata.json` | Optional Node.js/Express server and the settings for the online copy on Vercel. Not needed for the Windows launcher; see "Running it". |
| `scripts/` | Generators for the Phase 9 attack images and ZIP. |
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

## How Phase 10 was verified

Spreadsheet instructions are easy to get subtly wrong, so the Excel material was tested
against real Excel rather than assumed:

- Each answer-key workbook was opened in Excel and its formulas produced the documented
  numbers (12 images, 10 correct, 2 wrong, 83.3% accuracy, average confidence 82.7, lowest
  47; per fruit 100% / 75% / 75%) in all three languages, including the right-to-left Arabic
  and Hebrew sheets.
- Every chart in the guide is a picture exported by Excel itself from those workbooks. The
  first export exposed overlapping titles, heavy black gridlines and stray legend keys from
  the library defaults — fixed before use.
- The guide's click-by-click steps were replayed in Excel by selecting exactly the ranges
  the guide names and inserting each chart type. This caught a real error: selecting
  `C1:E13` for the bubble chart makes Excel treat the header row as a data point, so the
  guide says to select `C2:E13` (no header) for that one chart.
- The "Ctrl-select" and "Sort" challenges were checked the same way.
- The screen illustrations (ribbon, formula bar, numbered callouts) are simplified drawings
  rendered with headless Chrome so Arabic and Hebrew text shapes and flows right-to-left
  correctly; the guide labels them as illustrations. Arabic/Hebrew menu names follow
  Microsoft's terminology as closely as possible, but were not checked against an
  Arabic-language Excel — worth a native-speaker skim.

## Security model

- Serves only files inside this folder; nothing else on the laptop is reachable.
- Read-only: `GET`/`HEAD` only, no upload endpoint, no directory write access.
- No personal files belong in this folder — it is network-exposed by design while the
  server is running.
- Intended for a trusted classroom LAN/Wi-Fi, not a public network. Not intended to be
  exposed to the public internet (no port forwarding, no tunneling by default).

## Running it

See [`README_FIRST.txt`](README_FIRST.txt) for the full step-by-step teacher guide.

- **Windows (recommended):** unzip, double-click `START_SERVER_WINDOWS.bat`, read the
  address it shows you (`http://YOUR-IP:8000`), give that address to students. It uses
  Python if present and otherwise the built-in PowerShell server — nothing to install.
- **Linux / macOS:** `./START_SERVER_LINUX_MAC.sh` (port 8000; uses Node only if
  `npm install` has already been run, otherwise Python).
- **Node.js (optional):** `npm install` once, then `npm start` — serves on port 3000.
  `START_SERVER_WINDOWS.bat` deliberately does not start it automatically: on a computer
  that has Node.js but where `npm install` was never run, `node server.js` stops with
  `Cannot find package 'express'`.
- **Online copy:** the repository is deployed on Vercel (`vercel.json`, `api/`), which is
  useful when classroom Wi-Fi blocks device-to-device traffic. The site works from any
  network, but students then download over the internet instead of from the laptop.

The server's address changes with the network (home, school, hotspot). The Windows
launcher re-detects it every time it starts, and the student pages use relative links,
so they work on whatever address students open.
