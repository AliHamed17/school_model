AI CLASS LOCAL DOWNLOAD SERVER
================================

QUICK START (just do this)
---------------------------
1. Unzip this whole folder anywhere (don't put it inside another zip or a
   OneDrive-synced "personal documents" folder).
2. Double-click:
      START_SERVER_WINDOWS.bat
   Give it a few seconds - your browser opens automatically showing the
   download page once it's ready. (If Windows Firewall asks, click "Allow"
   for private networks.) If you run this file again while it's already
   running, it just reopens the page instead of starting a second server -
   so don't worry about double-clicking it more than once.
3. Look at the black window for a line like:
      Wi-Fi     10.0.0.25
   Tell students to open that address in their browser, e.g.:
      http://10.0.0.25:8000
4. Keep the black window open during class. Close it (or press Ctrl+C) when
   you're done.

That's the whole thing. Everything below is only for when something looks
wrong or you want more detail.

---------------------------------------------------------------------------

WHAT STUDENTS DO
-----------------
1. Open the address you give them.
2. Click the button for the phase you name (e.g. "Phase 2").
3. Right-click the downloaded ZIP -> Extract All.
4. Go to https://teachablemachine.withgoogle.com/ and upload the extracted
   files (no camera needed).

ARABIC VERSION
--------------
The student page also exists fully in Arabic:
   http://YOUR-IP:8000/index-ar.html
Each page has a language link at the top ("English" / "العربية").

IF THE BROWSER DOESN'T OPEN BY ITSELF
---------------------------------------
Just open it yourself - type the address shown in the black window into any
browser. Everything still works the same.

IF "START_SERVER_WINDOWS.bat" SAYS PYTHON WASN'T FOUND
---------------------------------------------------------
It automatically switches to a backup method built into this same file -
you don't need to run anything else. That backup needs Administrator
rights, so Windows will ask for permission once; click "Yes". If you can't
grant that (a locked-down school laptop with no admin account), install
Python from the Microsoft Store instead - it needs no admin rights - then
run START_SERVER_WINDOWS.bat again.

TEST BEFORE CLASS
------------------
1. Start the server (step 2 above).
2. Confirm the page that auto-opened loads correctly.
3. On one OTHER device connected to the same Wi-Fi, open the address from
   step 3 above and download one ZIP.
4. If that fails, see the troubleshooting below.

TROUBLESHOOTING
-----------------
- Page doesn't load right after starting: wait a second and refresh - the
  server takes a moment to start.
- A download fails and the browser says "check internet connection": this
  almost always means the black server window got closed (on purpose or by
  accident) and nothing is listening anymore, usually after running the
  .bat file more than once and closing one of the windows. Fix: close any
  leftover browser tabs, double-click START_SERVER_WINDOWS.bat once, and
  use the NEW tab it opens - don't reuse an old tab from an earlier run.
- A second device can't connect: confirm it's on the SAME Wi-Fi/network as
  this laptop, and that you gave it the "Recommended" address, not
  127.0.0.1 or an address starting with 169.254.
- Still can't connect on the same Wi-Fi: many school/guest Wi-Fi networks
  block device-to-device traffic ("client isolation" / "AP isolation").
  Fix: use a dedicated classroom router or hotspot instead.
- Different networks entirely (e.g. teacher on 192.168.1.x, student on
  10.20.x.x): private network addresses can't reach across different
  networks. Put everyone on the same Wi-Fi/hotspot.
- Port 8000 already in use: close any other program using it, or run
  "powershell -File server.ps1 -Port 8001" instead.

NOTE ON INTERNET ACCESS
------------------------
This server itself only needs your LOCAL network - no internet required to
download the phase ZIPs. The lesson activity itself still needs real
internet access for https://teachablemachine.withgoogle.com/ (required) and
optionally https://quickdraw.withgoogle.com/ (Phase 1 warm-up only).

WHY THERE IS ONLY A ZIP OPTION (NOT A "FOLDER" DOWNLOAD)
----------------------------------------------------------
Browsers only allow "pick a folder and save files straight into it" on
HTTPS or on literally "localhost" - never on a plain http:// address like
http://10.0.0.25:8000, which is exactly how students reach this server. The
only alternative would be downloading every picture one by one, which is
worse. ZIP + Windows' built-in "Extract All" (one right-click) is the
simplest reliable way to get "one click, one folder" here.

OPTIONAL: QR CODE FOR STUDENTS
-------------------------------
Once the server is running, open this on YOUR laptop only:
   http://YOUR-IP:8000/teacher_qr.html
It generates a QR code for the address you're actually using, so students
can scan instead of typing. Fully offline, not linked from the student page.

SECURITY
--------
This server only serves files inside this folder (read-only, no upload).
Don't put personal files in this folder. Stop the server after class.
Prefer a trusted classroom network over public Wi-Fi.

FILES
-----
index.html                  Student download page (English)
index-ar.html                Student download page (Arabic, right-to-left)
teacher_qr.html             Optional teacher-only QR code generator
downloads/                  All phase ZIPs
START_SERVER_WINDOWS.bat    Double-click this (Windows) - handles everything
server.ps1                  Backup server used automatically if Python is missing
START_SERVER_LINUX_MAC.sh   Linux/macOS
