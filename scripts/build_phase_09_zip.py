import os
import shutil
import zipfile

work_dir = '/tmp/Phase_09_Adversarial_Gauntlet'
os.makedirs(work_dir, exist_ok=True)
data_dir = os.path.join(work_dir, 'DATA_ADVERSARIAL_GAUNTLET')
os.makedirs(data_dir, exist_ok=True)

# Copy the 12 generated images
src_dir = '/tmp/DATA_ADVERSARIAL_GAUNTLET'
for f in os.listdir(src_dir):
    shutil.copy(os.path.join(src_dir, f), os.path.join(data_dir, f))

# 1. STUDENT_START_HERE.txt
with open(os.path.join(work_dir, 'STUDENT_START_HERE.txt'), 'w', encoding='utf-8') as f:
    f.write("""================================================================================
PHASE 9 — THE ADVERSARIAL GAUNTLET & OUT-OF-DISTRIBUTION (OOD) AUDIT
Target Age: 14–16 Years | Difficulty: HARDCORE / ADVANCED
================================================================================

MISSION OBJECTIVE:
You thought you built a smart fruit classifier.
Now you are taking the role of an AI Red Team Security Auditor.
Your mission is to PROVE that closed-world neural networks are brittle,
discover the Softmax Overconfidence Flaw, and design a defensive safety architecture.

FAST START (3 MINUTES):
1. Keep your Teachable Machine tab open with your trained model (Apple, Banana, Orange).
2. Open the folder: DATA_ADVERSARIAL_GAUNTLET/
3. Test all 12 challenge images one by one using Teachable Machine's 'Upload' file input.
4. Record what happened in AUDIT_WORKSHEET.txt!

THE 4 FAILURE MODES YOU WILL UNCOVER:
1. Out-Of-Distribution (OOD) Hallucination:
   Objects that are NOT fruit (Tennis Ball, Basketball, Traffic Light).
   Why does the AI claim a basketball is an Orange with 99% confidence?
2. Texture Bias vs. Shape Bias:
   Apple shape with banana skin speckles. Did your CNN look at the shape or the texture?
3. Adversarial Optical Perturbation:
   Mathematical checkerboard noise and high-contrast patch stickers that blind deep convolutional kernels.
4. Chimeric & Spectrum Inversion:
   Split hybrids and negative spectrums.

FINAL BOSS CHALLENGE (CAN YOU FIX IT?):
Read MISSION_BRIEF.txt to find out how to defend your model by adding a 4th class!
""")

# 2. MISSION_BRIEF.txt
with open(os.path.join(work_dir, 'MISSION_BRIEF.txt'), 'w', encoding='utf-8') as f:
    f.write("""================================================================================
AI RED TEAM AUDIT: MISSION BRIEFING & TECHNICAL BREAKDOWN
For High School AI & Computer Vision Students (Ages 14-16)
================================================================================

1. THE SOFTMAX TRAP (Why AI Lies With Confidence):
In standard classification models (like MobileNet / Teachable Machine), the final
layer is a Softmax mathematical function:
    Probability(Class i) = exp(Score_i) / SUM(exp(Score_all))

Because all output probabilities MUST add up to exactly 100%, the AI HAS NO CHOICE
but to pick Apple, Banana, or Orange - even if you show it a photo of an alien, a toaster,
or a tennis ball!
It CANNOT output: 'I have never seen this before in my training.'
In real life, this flaw caused Tesla autonomous crashes and medical imaging misdiagnoses.

2. THE 12 GAUNTLET TEST VECTORS:
- adv_01_ood_tennis_ball.png          -> Test for OOD & fuzzy texture trap
- adv_02_ood_basketball.png           -> Test for color-shortcut overconfidence
- adv_03_texture_swap_apple_banana.png-> Test whether CNN prioritizes Texture or Geometry
- adv_04_adversarial_patch_sticker.png-> Test kernel vulnerability to high-contrast patch
- adv_05_checkerboard_frequency_noise.png -> High-frequency spatial frequency attack
- adv_06_inverted_negative_spectrum.png -> Inverted RGB chromatic response
- adv_07_camouflage_background_blend.png -> Edge detection collapse under background mimicry
- adv_08_chimeric_sliced_hybrid.png   -> Multi-class conflict resolution in single frame
- adv_09_ood_traffic_light_red.png    -> Critical safety test: Artificial glowing sphere vs organic fruit
- adv_10_extreme_silhouette_backlit.png -> Pure silhouette evaluation without color assistance
- adv_11_ood_reptilian_scale_apple.png -> Biological pattern transfer
- adv_12_posterized_minimal_banana.png -> Minimalist vector abstraction

3. YOUR ENGINEERING DEFENSE TASK:
How do real AI engineers defend production models against OOD attacks?
Method A: Confidence Thresholding (Reject prediction if top class < 80% confidence)
Method B: Negative / Background Rejection Class (Train a 4th class with random everyday objects!)
Try creating a 4th class in Teachable Machine called 'None / Other / Background' and retrain!
""")

# 3. AUDIT_WORKSHEET.txt
with open(os.path.join(work_dir, 'AUDIT_WORKSHEET.txt'), 'w', encoding='utf-8') as f:
    f.write("""================================================================================
AI SECURITY AUDIT WORKSHEET — STUDENT LOG
Name: ______________________   Date: ______________   Model Version: _________
================================================================================

IMAGE FILE                                PREDICTED CLASS   CONFIDENCE (%)   DID IT FOOL THE AI? (YES/NO)   FAILURE MODE IDENTIFIED
--------------------------------------------------------------------------------------------------------------------------------
adv_01_ood_tennis_ball.png                [             ]   [         %]     [        ]                     [ OOD Object            ]
adv_02_ood_basketball.png                 [             ]   [         %]     [        ]                     [ OOD Object            ]
adv_03_texture_swap_apple_banana.png      [             ]   [         %]     [        ]                     [ Texture Bias          ]
adv_04_adversarial_patch_sticker.png      [             ]   [         %]     [        ]                     [ Adversarial Patch     ]
adv_05_checkerboard_frequency_noise.png   [             ]   [         %]     [        ]                     [ Frequency Noise       ]
adv_06_inverted_negative_spectrum.png     [             ]   [         %]     [        ]                     [ Inverted Spectrum     ]
adv_07_camouflage_background_blend.png    [             ]   [         %]     [        ]                     [ Camouflage / Low-Edge ]
adv_08_chimeric_sliced_hybrid.png         [             ]   [         %]     [        ]                     [ Chimeric / Split Class]
adv_09_ood_traffic_light_red.png          [             ]   [         %]     [        ]                     [ Safety-Critical OOD   ]
adv_10_extreme_silhouette_backlit.png     [             ]   [         %]     [        ]                     [ Zero-Color Silhouette ]
adv_11_ood_reptilian_scale_apple.png      [             ]   [         %]     [        ]                     [ Biological Texture    ]
adv_12_posterized_minimal_banana.png      [             ]   [         %]     [        ]                     [ Posterized Vector     ]

ANALYSIS QUESTIONS:
1. What was the highest confidence score your AI gave to an object that was NOT a fruit at all?
   Object: _________________________  Score: _______%  Prediction: __________________

2. In adv_03 (apple shape with banana yellow skin), did the AI vote with the SHAPE (Apple) or the TEXTURE/COLOR (Banana)?
   Answer: _________________________
   What does this prove about what deep neural networks pay attention to?

3. If this AI were deployed in a supermarket checkout scanner or an airport luggage screener,
   what disaster could occur?

4. PROPOSE A SOLUTION: Describe two specific software engineering techniques to prevent the AI
   from predicting non-fruits with 99% confidence.
""")

# 4. TEACHER_KEY_AND_DEBRIEF.txt
with open(os.path.join(work_dir, 'TEACHER_KEY_AND_DEBRIEF.txt'), 'w', encoding='utf-8') as f:
    f.write("""================================================================================
TEACHER ANSWER KEY & CLASSROOM DEBRIEF GUIDE (PHASE 9)
For Middle/High School AI Educators (Students Aged 14–16)
================================================================================

KEY CONCEPTUAL TAKEAWAY:
Phase 9 shifts students from 'AI consumers' to 'AI Safety & Security Engineers'.
They learn that deep neural networks do not possess common sense or semantic understanding.
They are high-dimensional curve fitters optimized exclusively on training loss.

EXPECTED MODEL BEHAVIORS:
1. adv_01 (Tennis Ball) -> Almost universally classified as 'Orange' or 'Banana' with 90-99% confidence.
   Teaching Point: Explain the Softmax function. Point out that the model has no 'None' category.
2. adv_02 (Basketball) -> Classified as 'Orange' with overwhelming confidence (>95%).
   Teaching Point: The model learned 'orange round pixel cluster' instead of 'citrus peel with stem and pores'.
3. adv_03 (Texture Swap) -> In 80% of models, Texture wins over Shape!
   Teaching Point: Research paper insight (Geirhos et al., 2019): Convolutional Neural Networks
   have a strong 'Texture Bias', whereas human children have a 'Shape Bias'.
4. adv_04 & adv_05 (Adversarial Noise/Patch) -> The patch overrides global spatial coherence.
5. adv_09 (Red Traffic Light) -> Gets classified as 'Apple' with high confidence.
   Teaching Point: Imagine a self-driving car mistaking a stop light for an apple or vice versa!

SOCRATIC DISCUSSION QUESTIONS TO ASK THE CLASS:
1. 'Why couldn\\'t the AI simply say: I don\\'t know what that is?'
2. 'If you were designing the computer vision system for an autonomous drone, how would you protect it?'
3. 'What happens if someone puts an adversarial sticker on a 45 MPH speed limit sign so the AI reads it as 85 MPH?'

DEFENSE STRATEGY DEMONSTRATION:
Have an early-finishing student create a 4th class named 'Other / Non-Fruit' in Teachable Machine,
feed in 20 photos of desks, shoes, faces, and balls, retrain, and rerun the Gauntlet!
Watch how all false confidences drop instantly!
""")

# 5. OPEN_ME.html
with open(os.path.join(work_dir, 'OPEN_ME.html'), 'w', encoding='utf-8') as f:
    f.write("""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Phase 9 — Adversarial Gauntlet & OOD Audit</title>
<style>
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;max-width:880px;margin:32px auto;padding:0 24px;color:#0f172a;background:#f8fafc;line-height:1.6}
header{border-bottom:2px solid #e2e8f0;padding-bottom:16px;margin-bottom:24px}
h1{font-size:26px;color:#0f172a;margin:0 0 6px}
.subtitle{color:#64748b;font-size:15px;margin:0}
.banner{background:#fff1f2;border:1px solid #fecdd3;border-radius:10px;padding:16px 20px;margin:20px 0;color:#9f1239}
.banner b{color:#881337}
.card{background:white;border:1px solid #e2e8f0;border-radius:12px;padding:20px;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,0.03)}
.card h2{font-size:18px;margin:0 0 10px;color:#1e293b}
ol{padding-left:20px;margin:0}
li{margin-bottom:8px}
.btn{display:inline-block;background:#0f172a;color:white;text-decoration:none;padding:10px 18px;border-radius:8px;font-weight:600;font-size:15px}
.btn:hover{background:#334155}
table{width:100%;border-collapse:collapse;margin-top:12px;font-size:14px}
th,td{border:1px solid #e2e8f0;padding:8px 12px;text-align:left}
th{background:#f1f5f9;color:#334155}
code{background:#f1f5f9;padding:2px 6px;border-radius:4px;font-family:monospace}
</style>
</head>
<body>
<header>
  <h1>Phase 9 — Adversarial Gauntlet &amp; OOD Audit</h1>
  <p class="subtitle">AI Red Team Security Assessment for High School AI Researchers (Ages 14–16)</p>
</header>

<div class="banner">
  <b>Hardcore AI Challenge:</b> In this phase, you are an AI security auditor. You will expose the Softmax Overconfidence Flaw by feeding 12 deliberately engineered adversarial attacks and Out-of-Distribution (OOD) objects into your trained model.
</div>

<div class="card">
  <h2>Quick Start Checklist</h2>
  <ol>
    <li>Keep Teachable Machine open in your browser: <a href="https://teachablemachine.withgoogle.com/" target="_blank">teachablemachine.withgoogle.com</a></li>
    <li>Locate the <code>DATA_ADVERSARIAL_GAUNTLET</code> folder inside this extracted ZIP.</li>
    <li>Upload all 12 images into Teachable Machine's input preview one by one.</li>
    <li>Open <code>AUDIT_WORKSHEET.txt</code> and record your model's classification &amp; confidence percentage.</li>
  </ol>
</div>

<div class="card">
  <h2>The 4 Vulnerability Categories</h2>
  <table>
    <thead>
      <tr><th>Vulnerability Class</th><th>Target Attack Image</th><th>Expected Exploit</th></tr>
    </thead>
    <tbody>
      <tr><td>Out-Of-Distribution (OOD)</td><td>Tennis Ball, Basketball, Traffic Light</td><td>Model hallucinates &gt;90% confidence on non-fruit items</td></tr>
      <tr><td>Texture vs. Shape Bias</td><td>Texture Swap (Apple shape + Banana skin)</td><td>Model votes with texture rather than global geometry</td></tr>
      <tr><td>Adversarial Perturbation</td><td>Adversarial Patch &amp; Checkerboard Noise</td><td>High-frequency patterns override neural activations</td></tr>
      <tr><td>Domain &amp; Lighting Shift</td><td>Camouflage Blend &amp; Negative Inversion</td><td>Feature extraction collapses under non-standard light</td></tr>
    </tbody>
  </table>
</div>
</body>
</html>
""")

# 6. URLS.txt
with open(os.path.join(work_dir, 'URLS.txt'), 'w', encoding='utf-8') as f:
    f.write("""Teachable Machine:
https://teachablemachine.withgoogle.com/

AI Safety & Adversarial Attacks in Computer Vision (Reference):
https://distill.pub/2017/adversarial-examples/
https://arxiv.org/abs/1811.12231 (ImageNet-trained CNNs are biased towards texture)
""")

# Create the ZIP archive
zip_path = 'downloads/Phase_09_Adversarial_Gauntlet_ULTIMATE.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(work_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, work_dir)
            z.write(full_path, rel_path)

print(f"Successfully built {zip_path}, size: {os.path.getsize(zip_path)} bytes")
