AI CLASS LOCAL DOWNLOAD SERVER & COMPUTER VISION LAB (AGES 14-16)
====================================================================

QUICK START (just do this)
---------------------------
1. Unzip this whole folder anywhere on your teacher laptop.
2. Run the server:
   - On Windows: Double-click START_SERVER_WINDOWS.bat
   - On Mac/Linux: Run ./START_SERVER_LINUX_MAC.sh
   - Or with Node.js: npm run dev
3. Look at your computer's local Wi-Fi or LAN IP address, e.g. 10.0.0.25 or 192.168.1.15.
   Tell students to open that address on port 3000 in their browser, e.g.:
      http://10.0.0.25:3000
4. Keep the server window open during class. Close it when class ends.

---------------------------------------------------------------------------

WHAT STUDENTS DO
-----------------
1. Open the address you give them (e.g. http://10.0.0.25:3000).
2. Download the phase you instruct them to work on (e.g., Phase 2).
3. Right-click the downloaded ZIP -> Extract All.
4. Go to https://teachablemachine.withgoogle.com/ and upload the extracted
   images into the Standard Image Model (no camera required).
5. Use the in-browser Red Team Diagnostic Simulator to explore how CNNs evaluate
   features before running the advanced challenges.

ADVANCED CHALLENGES:
- Phase 8: Expert Bonus (8 tricky images exploring shortcut learning).
- Phase 9: Hardcore Adversarial Gauntlet (12 adversarial attacks, out-of-distribution
  tennis balls and basketballs, texture swaps, and architectural defense design).

ARABIC VERSION
--------------
The student hub is available in English and Arabic (full RTL layout):
   http://YOUR-IP:3000/index-ar.html
Click "العربية" or "English" in the top bar to switch languages instantly.

OFFLINE TEACHER QR CODE
-----------------------
Once the server is running, open this on your laptop:
   http://localhost:3000/teacher_qr.html
It displays a scannable QR code for students to join without typing the IP address manually.

NETWORK RESILIENCE
------------------
All lesson files, web pages, interactive simulators, and images are 100% self-contained
and served locally. No internet connection is needed for downloading files or rendering
the classroom hub. Internet is only required for the Google Teachable Machine website.
