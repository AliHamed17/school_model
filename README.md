# AI Class Local Server & Computer Vision Lab

A self-contained local web server and educational distribution hub for high school AI and Computer Vision students (ages 14–16) built around [Google Teachable Machine](https://teachablemachine.withgoogle.com/). Students connect over classroom Wi-Fi or local LAN, download phase packages, and train, test, audit, and defend image classification models — with **no camera required**, **no external image search**, and **zero internet data downloads needed for lesson files**.

The repository includes student-facing web hubs (English and Arabic RTL), all lesson ZIPs, an in-browser Red Team Diagnostic Simulator, and cross-platform server implementations (Node.js Express, Windows BAT, Linux/macOS Shell, and Python fallback).

---

## Curriculum Overview (Phases 1–9)

The curriculum progresses from foundational transfer learning to advanced machine learning safety and adversarial auditing:

| Phase | Duration | Focus & Topic | Description |
|---|---|---|---|
| **Phase 1** | 0–15 min | Warm-up & Neural Doodles | Quick, Draw! interactive pattern recognition intro. |
| **Phase 2** | 15–47 min | Baseline Training | 90 curated fruit images (Apple, Banana, Orange) uploaded to Teachable Machine. |
| **Phase 3** | 47–57 min | Easy Test & Metrics | 24 unseen test images to calculate baseline test accuracy. |
| **Phase 4** | 57–67 min | Break the AI | 30 stress-test images (occlusions, sliced fruit, lighting variations) + failure report. |
| **Phase 5** | 67–75 min | Improve & Retrain | Targeted data additions to address Phase 4 errors + validation set. |
| **Phase 6** | 75–87 min | Ambiguous Challenge | Multi-fruit and hybrid fruit images to analyze conflicting feature activations. |
| **Phase 7** | 87–90 min | Exit Ticket & Reflection | Student reflection prompts and teacher answer key. |
| **Phase 8** | Bonus | Expert Challenge | 8 tricky images testing shortcut learning (color shortcuts, scale, inverted angles). |
| **Phase 9** | **Hardcore** | **Adversarial Gauntlet & OOD Audit** | **NEW: 12 mathematical attack vectors for ages 14–16: Out-of-Distribution hallucinations (tennis ball, basketball, traffic light), texture swaps (apple shape + banana skin), adversarial patch stickers, high-frequency checkerboard noise, and designing a defensive 4th rejection class.** |

---

## Interactive Red Team Simulator (In-Browser)

The web hub (`index.html` and `index-ar.html`) includes a live interactive diagnostic bench where students can explore:
1. **The Softmax Overconfidence Trap:** Why neural networks with normalized softmax outputs hallucinate 90%+ confidence on non-fruit objects (e.g. tennis balls or basketballs) because they lack an "Unknown" rejection class.
2. **Texture vs. Shape Bias:** Testing whether CNN kernels prioritize high-frequency surface textures over holistic object geometry.
3. **Defensive Engineering:** Testing a Confidence Threshold Guard (rejecting predictions <75%) and training a 4th Negative Class ("Other / Background") to safely capture adversarial and OOD inputs.

---

## Running on Any Network (Local Wi-Fi, LAN, or Cloud)

### Option A: Node.js (Recommended)
```bash
npm install
npm run dev
# Server listens on http://0.0.0.0:3000
```

### Option B: Windows Quick Start
Double-click `START_SERVER_WINDOWS.bat`. It automatically detects Node.js or Python, starts the server on port 3000, and binds to `0.0.0.0` so all student devices on the classroom Wi-Fi can connect.

### Option C: Linux / macOS Quick Start
```bash
./START_SERVER_LINUX_MAC.sh
```

### Student Access
Tell students to open:
```text
http://YOUR-COMPUTER-IP:3000
```
Or have them scan the offline QR code generated at:
```text
http://localhost:3000/teacher_qr.html
```

---

## Network & Offline Reliability

- **100% Self-Contained:** All CSS, JavaScript, SVGs, and fonts are inlined or served locally. Zero external CDN dependencies, guaranteeing that pages load reliably on locked-down school networks or offline classroom routers.
- **Bilingual Support:** Full English (`index.html`) and Arabic (`index-ar.html` with full RTL layout) interfaces.
- **Safety First:** Read-only server; serves only files in the project folder with strict path normalization.
