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

## This week: the four phases (the main page)

The main page (`index.html`, `index-ar.html`, `index-he.html`) now shows **exactly four phases**. The earlier 14-phase lesson is kept, unchanged and not linked from the main page, as `all-phases.html` / `all-phases-ar.html` / `all-phases-he.html`.

| Phase | Time | What it is | Files |
|---|---|---|---|
| **1 — Boss Pictures** | ~60 min | Teachable Machine with much harder pictures. 120 training pictures (Apple, Banana, Orange) in which each fruit mostly sits on its own table (a hidden shortcut); a **Boss test** (12 pictures chosen where Teachable-Machine-style models struggle), a **Nightmare** set (blur, dark, tiny, cropped, sketch, mixed fruit), **Trap** pictures (tomato, lemon, peach, pumpkin, ball, corn, pepper) and a **Fix Pack** (every fruit on every table) for Round 2, plus an optional 4th class **Other**. Guide + captioned video in English, Arabic and Hebrew. | `boss/`, `downloads/Phase1_Boss_Pictures_STUDENT.zip`, `…FIX_PACK.zip`, `…TEACHER_KEY.zip` |
| **2 — Excel Data Lab** | ~45 min | The same Excel lab as last week (formulas, accuracy, five charts), now applied to the Boss results. Boss starter/example workbooks (the example holds real Teachable Machine numbers). | `excel/`, `downloads/Phase2_Excel_Data_Lab.zip` |
| **3 — Excel Brain** | ~60 min | A tiny AI built only from Excel formulas: 5×5-pixel pictures, 25 weights, logistic regression trained one picture at a time (192 learning steps), learning-rate experiment, weight "brain scan", test sheet, draw pad. Goal: 90% on the test. Guide + captioned video in three languages. | `brain/`, `downloads/Phase3_Excel_Brain.zip` |
| **4 — Detective Map** | ~35 min | The simulation of how an AI predicts (the former Phase 12): k-nearest-neighbours on a map of clues, with a challenge. | `sim/`, `downloads/Phase4_Detective_Map.zip` |

`downloads/Four_Phases_ALL.zip` bundles the four phase ZIPs, the teacher key and start-here notes.

**How hard are the Boss pictures, really?** We measured instead of guessing. (a) Teachable-Machine-style models (a MobileNet image model with a small trained head) on three MobileNet versions, 3 seeds each: pictures like the training set 99%, Boss test 62% in Round 1 → 95% in Round 2, Nightmare 33% → 49%, and the models were over 80% sure about 84% of the traps. (b) The real Teachable Machine website, driven in headless Chrome: Boss test 7/12 in Round 1 → 10/12 in Round 2, 4th class Other: 11 of 12 traps called Other. Results vary from run to run. The Boss test pictures were *mined*: hundreds of candidate pictures were scored and the ones a person finds obvious but the models get wrong were kept, so the numbers are not an accident of the generator.

**Excel Brain verification.** The workbook was opened in real Excel; the learning engine's weights match an independent Python simulation to 1e-6 in all three languages, and the student path (type five formulas, fill down) reproduces them. With the 4 hint pictures the test accuracy is 100% (learning rate 0.5 or 1), 90% (0.05, 0.1, 2) or 80% (5).

## Previous lesson: curriculum overview (Phases 0–13, now in `all-phases.html`)

The core lesson is phases 1–7, scheduled minute-by-minute across 90 minutes. Phase 0 is an
easy game to start with, and phases 8–13 are optional extensions.

| Phase | Time | Focus | What students get |
|---|---|---|---|
| **0** | Easy start, ~10 min | Human vs Robot (game) | A browser game: teach a tiny colour-based "robot" with 9 pictures, race it on 12 new ones, then try to trick it. Works offline in English, Arabic and Hebrew and exports the scores as a CSV for Excel. |
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
| **11** | Creative, ~35 min | Doodle Lab | Students invent their own categories, draw the training examples, teach an in-browser AI (nearest neighbour on 16×16 pixel grids), try to fool it, log accuracy to a CSV for Excel, and swap drawings with a friend to see bias. Offline, English/Arabic/Hebrew. |
| **12** | Concept simulation, ~35 min (best after Phase 3) | Detective Map | Answers *how does an AI predict?* Pictures become clue numbers, training pictures land as dots on a map, a new picture lands among them and its k nearest neighbours vote. Students pick the clues, switch on the AI's decision map, compare clue pairs and see why tricky pictures fool it. Real fruit pictures plus generated cats and dogs (drawn from their clue numbers, with two deliberately useless clues). Offline, English/Arabic/Hebrew. |
| **13** | XL challenge, 45–60 min | Inbox Defender | A challenge with no pictures: text. Students train a word-counting AI (naive Bayes) to stop scam messages in their own language (English, Arabic or Hebrew), see which words it treats as clues, beat 'sneaky scammers' (misspellings, dots between letters, polite scams, scary-sounding real messages) and patch the AI, tune how strict the guard is with a live 2×2 table, earn badges and export a CSV for Excel. Comes with a 3-minute captioned video of the real game and a step-by-step guide. |

**Phase 10 — Excel Data Lab.** Students type the percentages Teachable Machine gave them
into a spreadsheet, calculate accuracy and confidence with formulas (`IF`, `INDEX/MATCH`,
`AVERAGEIF` …) and draw five charts: pie, column, line, **XY scatter** and **XYZ bubble**.
It comes with an illustrated step-by-step guide in **English, Arabic and Hebrew**
(right-to-left pages), a starter `.xlsx` and a finished answer-key `.xlsx` per language,
a printable results sheet, and teacher notes. Everything in it was checked against real
Microsoft Excel, not just written from memory (see "How Phase 10 was verified" below).
Each guide opens with a **4-minute captioned video** (one per language) that walks through
every step, with chapter buttons and a "watch this part" link on every section.

**Phase 0 — Human vs Robot.** The "robot" is a real, very small machine-learning model:
from the labels the student gives it, it remembers one average colour per fruit and
classifies a new picture by the nearest colour. Because it only sees colour, it is fooled
by the orange-coloured and green apples while a person is not, which is the lesson: a model
learns from the examples it is given, and a model that only sees colour is not enough. With
correct labels it gets 9 of 12 on the quiz and 1 of 4 on the trick round; if it is taught
wrong names on purpose it gets 2 of 12.

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
| `index.html` / `index-ar.html` / `index-he.html` | The student hub (English, Arabic RTL, Hebrew RTL): exactly four phase cards, the student connection link and the teacher QR panel. |
| `boss/` | Phase 1: `guide-en/ar/he.html`, `START_HERE.html`, `img/` (contact sheets + real Teachable Machine screenshots), `video/` (three ~13 MB captioned videos built from the real Teachable Machine screenshots and real results). |
| `brain/` | Phase 3: `guide-en/ar/he.html`, `files/` (starter and example workbooks), `img/` (real exports of every step), `video/` (three ~17 MB captioned videos). |
| `all-phases*.html` | The previous 14-phase hubs, kept as an archive and not linked from the main page. |
| `inbox/` | Phase 13 Inbox Defender: `index.html` (the game), `guide-en/ar/he.html` (student guides with the video), `video/` (three ~12 MB captioned videos of the real game, posters, chapter times). Zipped without the videos as `downloads/Phase_13_Inbox_Defender_XL.zip`. |
| `sim/` | Phase 12 Detective Map: `index.html` (one page) plus `img/` (119 pictures); zipped with teacher notes as `downloads/Phase_12_Detective_Map_HOW_AI_PREDICTS.zip`. |
| `lab/` | Phase 11 Doodle Lab: one self-contained page (`index.html`), also zipped with teacher notes as `downloads/Phase_11_Doodle_Lab_CREATIVE.zip`. |
| `game/` | Phase 0 game: `index.html` (one self-contained page, English/Arabic/Hebrew) and `img/` (25 pictures). Also zipped, with notes, as `downloads/Phase_00_Easy_Game_Human_vs_Robot.zip` so it can be played from a file. |
| `excel/` | Phase 10 as web pages: `guide-en/ar/he.html` (click a formula to copy it), `START_HERE.html` language chooser, `img/` (illustrations + real Excel charts), `files/` (starter and example workbooks), `video/` (the three tutorial videos, posters and chapter times). The guides and files are zipped into `downloads/Phase_10_Excel_Data_Lab_FOLLOWUP.zip`; the videos are too large for that ZIP, so the ZIP's guides point to the class server instead. |
| `teacher_qr.html` | An optional, offline, teacher-only page that generates a QR code for whatever address the server is actually running on, so students can scan instead of typing. |
| `downloads/` | The lesson ZIPs: a MASTER bundle, an already-expanded "Expanded" bundle, one ZIP per phase (0–13). |
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

## About the tutorial videos

The three videos (`excel/video/excel-lab-en|ar|he.mp4`, 1280×720, about 4 minutes, about
20 MB each) are **animated walkthroughs, not screen recordings**, and they have **no
voice-over** (no Arabic or Hebrew voice was available on the build machine, so every step is
explained with large on-screen captions instead). They show a simulated Excel window with a
moving cursor, typed formulas, zoom, menus and the Insert-chart dropdown; the numbers and
formulas are exactly the ones in the example workbooks, and the five charts that pop up are
the real charts exported from Excel. Because it is a simulation, the same video can show
English, Arabic (right-to-left) and Hebrew (right-to-left) menus consistently. They were
generated by rendering an HTML animation frame by frame in headless Chrome and encoding it
as H.264 with Windows' built-in media encoder; the source is not part of the student
package. The wording of the Arabic and Hebrew captions follows the written guide and is
worth a native-speaker skim. If you later record a voice-over, the chapter times used by the
guides are in `excel/video/chapters-*.json`.

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
