MINISTRY OF EDUCATION AND TRAINING
FPT UNIVERSITY CAN THO

STARTUP PROJECT FINAL REPORT (FINAL REPORT) COURSE: EXE101 — EXPERIENTIAL ENTREPRENEURSHIP

MOTIONIQ — AI ASSISTANT PLATFORM SUPPORTING HOME EXERCISE TRACKING FOR THE ELDERLY (100% ON-DEVICE AI)

"MotionIQ – Home exercise, movement tracking made easier."

MotionIQ — AI Assistant Platform Supporting Home Exercise Tracking for the Elderly. Smartphone camera-based motion tracking, posture verification, repetition counting, and real-time audio guidance.

Instructor: Mr. Tran Ngoc Son
Student Group Name: MOTIONIQ — Group K19
Website Demo MVP: https://motion-iq-five.vercel.app

CAN THO CITY, NOVEMBER 2026

ACKNOWLEDGEMENTS

The MotionIQ project team would like to express our deepest gratitude and most sincere thanks to Mr. Tran Ngoc Son, who has dedicatedly imparted knowledge on innovative startup thinking, business model methodologies, and patiently guided us, providing invaluable professional feedback through each milestone: Checkpoint 1, Checkpoint 2, and Checkpoint 3 of the EXE101 course (Startup Experience).

The team also wants to sincerely thank the elderly individuals and relatives who enthusiastically participated in 50 survey responses as well as 5 direct prototype testing sessions of the application. Practical feedback from actual users is the guiding light that helps the team perfect the MotionIQ product to be the most useful and humane.

EXECUTIVE SUMMARY

MotionIQ is a technology solution applying Artificial Intelligence and computer vision running directly on mobile devices (100% On-Device AI), supporting the elderly to track their workout progress and balance training at home via a smartphone or laptop camera without investing in expensive additional hardware sensor equipment.

By flexibly combining the virtual assistant character "Be Nam" with Vietnamese voice count reminders, a pose recognition model based on published benchmark motion datasets (UI-PRMD, KIMORE, EHE) and the One-Euro Filter noise reduction filter, MotionIQ helps seniors maintain proper workout habits, count repetitions, and provide basic feedback. Actual survey results on 50 subjects show that more than 68% of children face difficulties when directly observing their parents working out, and 82.4% are ready to let their relatives try the application. Practical testing through 5 sessions achieved a range of motion (ROM) angle measurement index of 94.6% compared to the reference measurement angle and a SUS system usability score of 84.5/100 (Excellent level).

Regarding business and financial strategy, the team applies a value-based pricing method and competitor comparison with an Early Access trial package of 49,000 VND / month (~1,600 VND/day), combined with a concise 4-month communication plan with a student budget of 10,000,000 VND. Break-even analysis shows that with 26 paying customers for the Early Access package or 15 customers for the Standard package (79,000 VND/month), the project will self-cover its fixed monthly operating costs (1,000,000 VND/month), achieving operational self-sufficiency without requiring founder out-of-pocket subsidies.

LIST OF ABBREVIATIONS

LIST OF TABLES

List of tables summarizing experimental data, source code algorithms, financials, and operational plans in the report:

Table 1.1: Founding Team Competency Profiles & RACI Governance Matrix	Page 8

Table 2.1: Quantitative Field Survey Findings & Statistical Breakdown (N = 50)	Page 9

Table 2.2: Competitive Landscape Analysis & Strategic Positioning Differentiation	Page 11

Table 3.1: 9-Block Business Model Canvas (BMC) Framework	Page 12

Table 3.2: Profile of Model Files and Core Algorithms in Project Source Code	Page 13

Table 3.2-Joints: 22-Joint Standard UI-PRMD Anatomical Mapping & Forward Kinematics	Page 16

Table 3.2a: Actual Parameters Extracted from Weights File uiprmdQualityModel.json	Page 17

Table 3.3: Summary Table of 4 Standardized Functional Exercises in MotionIQ	Page 21

Table 3.4: Results of 5 Actual MVP Prototype Testing Sessions	Page 22

Table 4.1: Communication Channels & Operational Implementation Methods	Page 23

Table 4.2: 4-Month Communication Implementation Roadmap	Page 24

Table 4.3: Proposed Pricing Structure of MotionIQ	Page 24

Table 4.4: 4-Month Lean Student Media Budget Allocation (10,000,000 VND)	Page 25

Table 4.5: Target Customer Segments & 4-Month Conversion Funnel KPIs	Page 26

Table 4.6: Early Access Tier Subscription Monthly Revenue Forecast	Page 26

Table 4.7: Operational Break-Even vs. Full Capital Recovery Analysis	Page 27

Table 5.1: Identified Operational Risk Matrix & Concrete Mitigation Strategies	Page 28

TABLE OF CONTENTS

(Hierarchical Table of Contents with Standard Academic Chapter Structure)

ACKNOWLEDGEMENTS	2

EXECUTIVE SUMMARY	2

LIST OF ABBREVIATIONS	4

LIST OF TABLES	5

CHAPTER 1: PROJECT SETUP & FOUNDING TEAM CAPABILITY	7

1.1. Context of MotionIQ Idea Formation	7

1.2. Mission, Vision, and Core Values	7

1.3. Founding Team Capability Profiles & RACI Governance Matrix	8

CHAPTER 2: MARKET RESEARCH & FIELD SURVEY ANALYSIS	9

2.1. Methodology and Field Survey Scale (N = 50)	9

2.2. Quantitative Field Survey Findings & Data Analysis from Google Sheets (N = 50)	9

2.3. Target Customer Persona & Empathy Mapping	10

2.4. Competitive Landscape Analysis & Strategic Positioning Differentiation	10

CHAPTER 3: BUSINESS MODEL & TECHNICAL MVP PROTOTYPE	12

3.1. 9-Block Business Model Canvas (BMC) Framework	12

3.2. Profile of Model Files and Algorithms in Project Source Code	12

3.2.1. Technical Solution Architecture & 100% On-Device AI Pipeline	13

3.2.2. Real-Time Browser-Based Computer Vision Layer (Edge AI Vision Pipeline)	14

3.2.3. Automated Environment, Lighting & Standing Distance Calibration Layer	14

3.2.4. 3D Kinematics Mathematical Layer, Signal Noise Filtering & Repetition State Machine	15

3.2.5. Machine Learning Model for Assessing Movement Quality from UI-PRMD Dataset	16

3.3. 4 Standardized Functional Exercise Movements	18

3.3.1. Principles of Exercise Standardization Based on 3 International Datasets	18

3.3.2. In-Depth Analysis of 4 Standardized Functional Exercises	18

3.3.3. Summary Table of 4 Standardized Functional Exercises in MotionIQ	21

3.4. Results of 5 Actual MVP Prototype Testing Sessions	21

CHAPTER 4: MEDIA PLAN & REVENUE DEVELOPMENT	23

4.1. 04-Month Media Objectives	23

4.2. Target Customers & Key Message	23

4.3. Communication Channels & Methods	23

4.4. 04-Month Media Implementation Roadmap	23

4.5. Value-Based & Competitive Parity Pricing Strategy	24

4.6. Budget Estimation and Operating Costs	25

4.7. Revenue Development Plan & KPI Targets after 04 Months	25

4.8. Revenue Forecast and Break-Even Analysis	26

CHAPTER 5: RISK MANAGEMENT & SUSTAINABILITY	28

5.1. Identification of Practical Risks & Mitigation Measures	28

5.2. Development and Sustainability Plan by Phase	28

5.3. Project Limitations and Future Technological Roadmap	29

CONCLUSION	30

CHAPTER 1: PROJECT SETUP & FOUNDING TEAM CAPABILITY (CHECKPOINT 1)

1.1. Context of MotionIQ Idea Formation

Vietnam is currently one of the fastest aging populations in the world. According to the General Statistics Office (GSO), the number of people aged 60 and above has exceeded 13.5 million (accounting for 13.5% of the total population). Along with the natural aging process, the elderly often face musculoskeletal degeneration, sarcopenia (age-related muscle loss), knee and spinal osteoarthritis, and decreased balance capability, dramatically elevating the risk of falls and severe daily activity limitations.

Maintaining gentle, regular physical activity habits at home plays a vital role in slowing functional decline and sustaining independent physical mobility. However, in reality, most seniors exercise spontaneously based on unverified habits without knowing whether their joint angles and spinal alignments are anatomically correct. Meanwhile, busy working adult children cannot constantly supervise or remind their parents in person. Stemming from the urgent need to care for our own families, the founding team developed the MotionIQ project — an AI-powered home exercise tracking platform utilizing standard smartphone and laptop cameras to provide real-time repetition counting, posture verification, and gentle audio encouragement right in the living room.

1.2. Mission, Vision, and Core Values

• Mission: "Democratizing quality, evidence-based physical exercise support for every Vietnamese household" — safeguarding autonomous mobility, minimizing fall risks among the elderly, and providing working children complete peace of mind.

• Vision: Establishing MotionIQ as Vietnam's premier, widely adopted digital motion-tracking platform for elderly home wellness by 2027.

• Core Values:
1. Safety & Evidence-Based: All movement protocols are grounded in validated geriatric biomechanics and benchmarked against prestigious public datasets (UI-PRMD, KIMORE, EHE).
2. Privacy by Design: 100% On-Device AI processing directly in browser RAM, strictly saying NO to recording or transmitting video streams to external cloud servers.
3. Geriatric Empathy: High-contrast interface, extra-large touch targets (≥ 56px), and warm Vietnamese voice coaching through the "Bé Nấm" companion.

1.3. Founding Team Capability Profiles & RACI Governance Matrix

The MotionIQ founding team (Group K19) represents an interdisciplinary synergy combining Information Security, Graphic Design / UI-UX, Multimedia Communication, Foreign Languages, and Service Management from FPT University Can Tho Campus:

Table 1.1: Founding Team Competency Profiles & RACI Governance Matrix:

CHAPTER 2: MARKET RESEARCH & FIELD SURVEY ANALYSIS (CHECKPOINT 2)

2.1. Methodology and Field Survey Scale (N = 50)

To rigorously validate problem hypotheses and quantify market demand during Checkpoint 2, the team administered a comprehensive field survey across 50 independent respondents via Google Forms (publicly auditable dataset: https://docs.google.com/spreadsheets/d/1NJpJjXDwdHJxuo02m3jhKDx7krYWp0I2cv6WzW1sUJM):
• Respondent Demographics: 81.6% aged 18–23 and 18.4% aged 23–30, representing working children and grandchildren directly responsible for elderly family care.
• Elder Care Experience: 65.3% reported actively assisting elderly parents or grandparents with daily functional mobility over the past 12 months.
• Target Age Cohort of Relatives: 28.6% aged 60–69, 24.5% aged 70–79, and 10.2% aged 80+ (totaling 63.3% aged 60 and above; 24.5% aged 50–59; 12.2% under 50).

2.2. Quantitative Field Survey Findings & Data Analysis from Google Sheets (N = 50)

Table 2.1: Quantitative Field Survey Findings & Statistical Breakdown (N = 50):

When investigating primary user apprehensions regarding camera-based AI tools (Question 14):
1. Image Privacy & Security: 45% expressed privacy concerns regarding living room camera feeds.
2. Technological Intimidation: 50% noted that elderly parents struggle with complicated mobile software.
3. AI Accuracy on Tremors: 40% questioned whether AI can accurately assess slow, shaky geriatric movements.

These empirical survey findings directly established MotionIQ's core architectural pillars: 100% On-Device RAM processing to eliminate privacy fears, Geriatric UI with one-touch navigation and Vietnamese voice coaching to eliminate friction, and the One-Euro Filter to eradicate joint tremor noise.

2.3. Target Customer Persona & Empathy Mapping

MotionIQ serves a dual-customer profile comprising the Direct User (Elderly) and the Primary Payer (Adult Children):
• Persona 1 — Direct User: Mr. Nguyen Van An, 68 years old, retired civil servant living in Can Tho City. Suffers from early-stage knee osteoarthritis and mild balance loss. Desires daily gentle mobility routines to walk steadily and play with grandchildren. Struggles with small touchscreens, fears burdening his busy children, and feels unmotivated when practicing alone without feedback.
• Persona 2 — Primary Payer: Ms. Thu Hang, 36 years old, corporate office worker in Can Tho. Deeply loves her father but works 9–10 hours daily, feeling persistent guilt and anxiety over his sedentary isolation. Willing to pay 50,000 – 100,000 VND/month for a dependable wellness application that tracks her father's exercise safely and provides structured progress transparency.

2.4. Competitive Landscape Analysis & Strategic Positioning Differentiation

Table 2.2: Competitive Landscape Analysis & Strategic Positioning Differentiation:

CHAPTER 3: BUSINESS MODEL & TECHNICAL MVP PROTOTYPE (CHECKPOINT 3)

3.1. 9-Block Business Model Canvas (BMC) Framework

Table 3.1: 9-Block Business Model Canvas (BMC) Framework:

3.2. Profile of Model Files and Core Algorithms in Project Source Code

All technical architecture details presented below are directly extracted from the live MotionIQ production codebase (src/features/pose/ and scripts/uiprmd/):

Table 3.2: Profile of Model Files and Core Algorithms in Project Source Code:

3.2.1. Technical Solution Architecture & 100% On-Device AI Pipeline

To eliminate user privacy apprehensions and guarantee real-time latency without expensive GPU servers, MotionIQ operates a 100% On-Device AI architecture executed entirely within the client's web browser across four closed-loop layers:
1. Computer Vision Layer: MediaPipe Pose Landmarker Lite running via WASM/WebGL extracts 33 body landmarks at 25–30 FPS.
2. Environmental Calibration Layer: Continuously monitors room lighting, standing distance, and landmark visibility before allowing workouts to start.
3. Mathematical Kinematics Layer: Computes 3D joint angles, filters noise via One-Euro Filter, and drives a 7-state repetition state machine.
4. Machine Learning Movement Quality Layer: Normalizes skeletal coordinates and applies Logistic Regression trained on UI-PRMD to detect compensatory errors.

3.2.2. Real-Time Browser-Based Computer Vision Layer (Edge AI Vision Pipeline)

The computer vision engine (poseService.ts) integrates @mediapipe/tasks-vision (version 0.10.18):
• 33-Landmark Skeleton Tracking: Employs pose_landmarker_lite.task (16-bit Float16 quantization) in continuous video stream mode. Simultaneously outputs normalized 2D/3D screen coordinates and metric 3D world coordinates centered at the pelvis origin.
• Background Prewarming: In the static method PoseService.prewarm(), the application pre-initializes the WASM FilesetResolver as soon as the user opens the web app, ensuring the camera starts instantly without loading delay.
• Hardware Fallback: Defaults to GPU WebGL delegate. If WebGL context creation fails on older devices, it automatically falls back to CPU WASM.
• Adaptive Frame Skipping: Monitors FPS over 1,000ms intervals. If frame rate drops below 18 FPS for 2 consecutive cycles, it processes only alternate frames (even frames), prioritizing audio coaching responsiveness until FPS recovers to ≥ 26.
• Absolute Image Privacy (Privacy by Design): Video frames are read from HTMLVideoElement strictly into volatile local RAM to compute coordinates, then immediately garbage-collected. No image or video stream is ever saved or transmitted externally.

3.2.3. Automated Environment, Lighting & Standing Distance Calibration Layer

To ensure reliable tracking before rep counting begins, landmarkValidator.ts evaluates three conditions on every video frame:

• Step 1 — Ambient Lighting Measurement: Draws video frames to an OffscreenCanvas (32×24 pixels) and computes perceived luminance (Y) using standard ITU-R BT.601 coefficients:

• Step 2 — Standing Distance Estimation: Evaluates the bounding ratio of visible landmarks (visibility > 0.35) relative to frame height:

• Step 3 — Anatomical Region Visibility: Verifies visibility across 5 key body segments: Head (0, 7, 8), Hands (15, 16), Hips (23, 24), Knees (25, 26), and Feet (27–30). Tracking begins only when all regions exceed visibility ≥ 0.40 and overall confidence > 0.30.

3.2.4. 3D Kinematics Mathematical Layer, Signal Noise Filtering & Repetition State Machine

• 3D Spatial Joint Angle Calculation Formula (calculateAngle): Given adjacent anatomical landmarks A, B (vertex), and C, bone vectors BA = A - B and BC = C - B are formed. To prevent zero-division on degenerate points, vector lengths are bounded (|BA| ≥ 10^-6 and |BC| ≥ 10^-6), and cosine values are clamped to [-1.0, 1.0]:

• One-Euro Filter & Exponential Moving Average with Jump Gate: Addresses age-related physiological tremors. Along with the velocity-adaptive One-Euro filter, signalSmoother.ts incorporates an Exponential Moving Average (EMA) and 45° Jump Gate:

• Repetition State Machine with Hysteresis: Strict 7-state transitions govern repetition counting: IDLE → READY → DESCENDING → BOTTOM → ASCENDING → TOP → COMPLETE. A hysteresis angle threshold (hysteresisDeg) and minimum holding frames (minHoldFrames) prevent phantom rep counts from camera shake.

3.2.5. Machine Learning Model for Assessing Movement Quality from UI-PRMD Dataset

A distinguishing innovation of MotionIQ is supplementing heuristic angle thresholds with an empirical Machine Learning movement quality model trained on the international UI-PRMD dataset (University of Idaho - Physical Rehabilitation Movement Dataset, DOI: 10.5281/zenodo.23104965). The pipeline spans four algorithmic stages:

• Stage 1: Forward Kinematics Reconstruction & Joint Mapping: Maps 33 MediaPipe landmarks to 22 standard UI-PRMD Kinect joints:

Table 3.2-Joints: 22-Joint Standard UI-PRMD Anatomical Mapping & Forward Kinematics:

• Stage 2: Torso-Length Spatial Normalization: Translates all joints to Waist origin and normalizes by 3D Torso Length (Euclidean distance from Waist to Chest, requiring torsoLength ≥ 0.05), yielding a scale-invariant 66-dimensional vector per frame (22 joints × [X, Y, Z]):

• Stage 3: Kinematic Time-Series Pooling into 132-Dimensional Feature Vector: For repetition length T ≥ 5 frames, summarizeFrames() compresses the sequence into a fixed 132-dimensional vector combining Mean (µ) and Standard Deviation (σ) across all 66 joint coordinates:

• Stage 4: L2-Regularized Logistic Regression Training & 3-Threshold Classification Inference: Evaluates movement quality using Ridge Logistic Regression trained on 200 real motion sequences per exercise from UI-PRMD (100 correct, 100 compensatory). Validation enforces strict Subject-Separated splitting (train on Subjects 1–8; evaluate on unseen Subjects 9 & 10):

Table 3.2a: Actual Parameters Extracted from Weights File uiprmdQualityModel.json:

3.3. 4 Standardized Functional Exercise Movements

3.3.1. Principles of Exercise Standardization Based on 3 International Datasets

To ensure scientific rigor, safety, and physical appropriateness for Vietnamese seniors, MotionIQ strictly restricts its exercise library to functional movements verified across three established public motion research corpora (excluding unsuitable high-impact exercises):
1. UI-PRMD Dataset (University of Idaho, DOI: 10.5281/zenodo.23104965): Provides 3D skeletal data across 10 subjects with clinical annotation of correct and compensatory movement executions. Used directly to train uiprmdQualityModel.json.
2. KIMORE Dataset (Kinematic Assessment of Movement and Clinical Scores for Remote Monitoring): Comprises kinematic recordings from 78 subjects (healthy and motor-impaired), serving as the empirical baseline for target Range of Motion (Target ROM) boundaries in KinematicsLineChart.tsx.
3. EHE Dataset (Elderly Home Exercise Dataset): Encompasses 869 repetitions from 25 elderly individuals via home Kinect sensors, providing empirical calibration for repetition pacing, holding delays (minHoldFrames), and geriatric velocity thresholds.

3.3.2. In-Depth Analysis of 4 Standardized Functional Exercises

1. Exercise 1: Sit-to-Stand (System Code: sit-to-stand)

• Dataset Mapping Code: UI-PRMD: m05 (Sit-to-stand) | KIMORE: Es4 (Pelvis rotation / Sit-to-stand).

• Physical Activity Benefits for Older Adults: Transitioning from sitting to standing is one of the most critical functional activities for maintaining independence in daily living for older adults. The exercise directly targets the quadriceps, gluteus maximus, and trains the ability to control the body's center of gravity vertically.

• Anatomical Landmarks & Tracked Kinematic Angles: The system measures bilateral knee flexion angles via 3 landmarks: Hip (LEFT_HIP 23 / RIGHT_HIP 24) – Knee (LEFT_KNEE 25 / RIGHT_KNEE 26, vertex) – Ankle (LEFT_ANKLE 27 / RIGHT_ANKLE 28), while tracking hip flexion angle (Shoulder 11/12 – Hip 23/24 – Knee 25/26). Target Range of Motion (Target ROM): Transitioning from a seated position on a backed chair (knee angle 90°–125°) to a fully upright standing posture (knee angle reaching 165°–180°).

• Model Parameter Analysis from Model File (m05 in uiprmdQualityModel.json): The model has a bias coefficient = -0.9520. In the mean (µ) and standard deviation (σ) vectors, variation is strongly concentrated in the vertical Y-axis coordinate of the left/right knee joint (mean σ_Y reaching 0.7586 and 0.7287 times the torso length), along with anterior-posterior Z-axis displacement of the chest and head regions (mean µ_Z of chest = 0.3265, head = 0.3966) as the practitioner leans slightly forward to gain momentum to stand up. The model effectively detects compensatory errors such as: excessive forward trunk leaning, standing up without full knee extension, or shifting weight to one leg. Validation accuracy on Subjects 9 & 10 reached 95.0% (38/40 correct samples).

2. Exercise 2: Controlled Functional Squat (System Code: squat)

• Dataset Mapping Code: UI-PRMD: m01 (Deep squat) | KIMORE: Es5 (Squatting) | EHE Dataset: Squatting.

• Physical Activity Benefits for Older Adults: Comprehensive strengthening for the lower limb muscle group (quadriceps, hamstrings, glutes) and enhancing knee-ankle ligament stability, helping elderly people walk firmly and reducing the risk of knee buckling when climbing stairs.

• Anatomical Landmarks & Tracked Kinematic Angles: Simultaneously measures knee flexion angle (Hip 23/24 – Knee 25/26 – Ankle 27/28) and trunk inclination angle (Shoulder 11/12 – Hip 23/24 – Knee 25/26). Target Range of Motion (Target ROM): Lowering the center of gravity under control so that knee flexion stays within the safe zone of 90°–125° (avoiding deep squats that put stress on elderly knee cartilage), maintaining a straight spine, then pushing back up to a standing posture.

• Model Parameter Analysis from Model File (m01 in uiprmdQualityModel.json): The model has a bias coefficient = -0.3258. Weights with large magnitudes are located in the lower limb joint chain (knee joint displacement weights reach +0.7587 on the left and +0.7320 on the right; Y-axis standard deviation of knee and ankle reach 0.6962–0.7441). The model helps identify common technical errors such as: knee valgus (knees caving inward), shallow squat depth failing to reach muscle activation thresholds, or leaning the head and back too far forward. Validation accuracy on Subjects 9 & 10 reached 72.5% (29/40 correct samples).

3. Exercise 3: Standing Shoulder Abduction (System Code: shoulder-raise)

• Dataset Mapping Code: UI-PRMD: m07 (Standing shoulder abduction) | KIMORE: Es1 (Lifting of the arms) | EHE Dataset: LA (Lifting of arms).

• Physical Activity Benefits for Older Adults: Improves shoulder joint Range of Motion (Shoulder ROM), prevents frozen shoulder in old age, expands the ribcage to support respiratory function, and maintains upper limb flexibility for daily tasks (such as dressing, combing hair, reaching for items on shelves).

• Anatomical Landmarks & Tracked Kinematic Angles: Tracks shoulder abduction angle via 3 landmarks: Hip (23/24) – Shoulder (LEFT_SHOULDER 11 / RIGHT_SHOULDER 12, vertex) – Elbow (LEFT_ELBOW 13 / RIGHT_ELBOW 14), combined with checking elbow extension (Shoulder 11/12 – Elbow 13/14 – Wrist 15/16). Target Range of Motion (Target ROM): Raising arms laterally from a resting position alongside the body (0°–20°) to the target angle zone of 90°–150° (maximum 180° depending on individual flexibility) and then lowering them slowly.

• Model Parameter Analysis from Model File (m07 in uiprmdQualityModel.json): The model has a bias coefficient = -0.8338. Statistical data in the model clearly reflects the kinematic features of upper-limb exercises: standard deviations across all lower-limb joints (hip, knee, ankle) are near zero (mean σ ranging from 0.002 to 0.044 - indicating the legs remain stationary as a base), while standard deviations are highly concentrated at the wrist and hand joints (mean σ_Y reaching 0.3458–0.6225; weights at the wrist and hand reach +0.6867 to +0.8700). The model accurately detects errors such as shoulder shrugging/neck retraction, elbow flexing, or tilting the spine to the opposite side to compensate when the shoulder joint is stiff. Validation accuracy on Subjects 9 & 10 reached 97.5% (39/40 correct samples).

4. Exercise 4: Standing Side Leg Raise (System Code: side-leg-raise)

• Dataset Mapping Code: UI-PRMD: m06 (Standing active straight leg raise / Hip abduction).

• Physical Activity Benefits for Older Adults: Directly strengthens the gluteus medius and tensor fasciae latae - muscle groups responsible for maintaining lateral pelvic balance during single-leg stance. This is a key exercise helping elderly individuals correct a wobbly gait, prevent staggering, and minimize the risk of sideways falls.

• Anatomical Landmarks & Tracked Kinematic Angles: Measures hip abduction angle via 3 landmarks: Ipsilateral Shoulder (11/12) or Contralateral Hip – Exercising Hip (23/24, vertex) – Knee (25/26) / Ankle (27/28), while monitoring the knee angle of the lifting leg (Hip 23/24 – Knee 25/26 – Ankle 27/28) to ensure it stays straight (≥ 165°). Target Range of Motion (Target ROM): Lightly holding onto a secure support, lifting the leg straight out to the side to achieve a hip opening angle of 30°–45° while keeping the torso upright.

• Model Parameter Analysis from Model File (m06 in uiprmdQualityModel.json): The model has a bias coefficient = -0.9935. Prominent features in the model are the sharp contrast in amplitude between the stance leg (low standard deviation σ ≈ 0.05–0.12) and the active leg performing the movement (very high standard deviation at the knee, ankle, and foot: mean σ_X reaching 0.3987–0.4336, mean σ_Y reaching 0.7249–0.7970; weights along the active leg joint chain reach +0.4774 to +0.6137). The model keenly detects two common compensatory errors in elderly individuals with weak hip abductors: (1) Knee flexion when lifting the leg, and (2) Leaning the entire upper body toward the stance leg to create the illusion of lifting the leg higher. Validation accuracy on Subjects 9 & 10 reached 97.5% (39/40 correct samples).

3.3.3. Summary Table of 4 Standardized Functional Exercises in MotionIQ

Table 3.3: Summary Table of 4 Standardized Functional Exercises in MotionIQ:

Safety Limit Notice: MotionIQ is strictly a supportive tool for monitoring home functional movement via standard mobile/laptop cameras. Joint angle metrics and movement quality assessment scores serve as physical activity tracking references and do not replace medical diagnosis, clinical evaluation, or direct care from licensed physical therapists.

3.4. Results of 5 Actual MVP Prototype Testing Sessions

The MotionIQ team deployed the live MVP prototype across five comprehensive physical testing sessions in Can Tho City with elderly citizens and wellness trainers:

Table 3.4: Results of 5 Actual MVP Prototype Testing Sessions:

CHAPTER 4: MEDIA PLAN & REVENUE DEVELOPMENT (CHECKPOINT 3)

4.1. 04-Month Media Objectives

Throughout the 4-month initial launch period, MotionIQ focuses on establishing localized brand awareness, driving targeted organic trials, and converting active trial users into recurring subscribers within a disciplined student budget:
1. Brand Awareness: Establish the "Bé Nấm" companion image as a warm, reliable exercise supporter for Vietnamese seniors across TikTok and Facebook.
2. Targeted Reach: Connect with 150–180 working adult children seeking autonomous mobility solutions for their parents.
3. User Activation: Guide 40–50 households to register and complete trial sessions, capturing empirical usability feedback.
4. Paying Conversion: Convert 15–20 households into paying subscribers, generating initial recurring operational revenue.

4.2. Target Customers & Key Message

• Primary Payer: Adult children aged 25–40 who work long hours away from home but hold deep concern for their elderly parents' physical health.
• Direct User: Seniors aged 60+ requiring simple, gentle, guided movements with clear Vietnamese voice prompts.
• Core Slogan: "MotionIQ – Home exercise, movement tracking made easier."

4.3. Communication Channels & Methods

Table 4.1: Communication Channels & Operational Implementation Methods:

4.4. 04-Month Media Implementation Roadmap

Table 4.2: 4-Month Communication Implementation Roadmap:

4.5. Value-Based & Competitive Parity Pricing Strategy

MotionIQ applies a Value-Based Pricing strategy benchmarked against prevailing alternatives in Vietnam:
• In-home personal training costs 200,000 – 400,000 VND per session (2–4M VND/month), making it unaffordable for average families.
• YouTube fitness videos are free but offer zero posture validation, creating safety risks for elderly practitioners.
• Survey data shows 64.7% of surveyed families readily accept 50,000 – 149,000 VND/month. MotionIQ introduces a highly competitive tier structure:

Table 4.3: Proposed Pricing Structure of MotionIQ:

4.6. Budget Estimation and Operating Costs

To execute the 4-month launch plan, the team established a lean student marketing budget of 10,000,000 VND:

Table 4.4: 4-Month Lean Student Media Budget Allocation (10,000,000 VND):

In addition to the media budget, baseline operating costs are maintained lean:
• Fixed Costs (FC): 1,000,000 VND / month (lightweight cloud database, domain registration, software licenses).
• Variable Costs (VC): 10,000 VND / subscriber / month (payment gateway processing fees via PayOS/MoMo and cloud notification messaging).

4.7. Revenue Development Plan & KPI Targets after 04 Months

MotionIQ deploys a 5-stage conversion funnel (Reach → Interest → Trial → Conversion → Retention):

Table 4.5: Target Customer Segments & 4-Month Conversion Funnel KPIs:

4.8. Revenue Forecast and Break-Even Analysis

Monthly recurring revenue projections across customer adoption levels on the Early Access plan (49,000 VND/month):

Table 4.6: Early Access Tier Subscription Monthly Revenue Forecast:

Break-Even Analysis is computed using standard entrepreneurial unit economics formulas:
Break-Even Volume: Q_BE = FC / (P - VC)

Table 4.7: Operational Break-Even vs. Full Capital Recovery Analysis:

CHAPTER 5: RISK MANAGEMENT & SUSTAINABILITY (CHECKPOINT 3)

5.1. Identification of Practical Risks & Mitigation Measures

To ensure safe, sustainable, and legally compliant operation, the team identified seven operational risks and designed targeted mitigations:

Table 5.1: Identified Operational Risk Matrix & Concrete Mitigation Strategies:

5.2. Development and Sustainability Plan by Phase

The project follows a disciplined three-phase growth trajectory:
• Phase 1 — Validation & Launch (Months 1–4): Finalize MVP web prototype, onboard 40–50 trial households, convert 15–20 paying subscribers, validate 49k pricing.
• Phase 2 — Stabilization & Optimization (Months 5–6): Optimize AI inference speed, measure 3-month subscriber retention rate, introduce 79k Standard tier, reach operational break-even (26 subscribers).
• Phase 3 — Expansion & Community Scaling (Months 7–12): Expand exercise catalog with wrist/ankle routines, deploy Zalo Mini App for zero-install access, pilot B2B partnerships with senior day-care centers in the Mekong Delta.

5.3. Project Limitations and Future Technological Roadmap

While achieving high accuracy and usability, the team candidly recognizes current MVP constraints and outlines future engineering upgrades:
• Lighting & Clothing Sensitivity: Extreme backlight or loose, flowing clothing can occasionally impair landmark visibility. Future work will integrate adaptive contrast auto-tuning and multi-frame silhouette estimation.
• Single-Angle Monocular Tracking: Relying on a single smartphone camera limits full 360° rotational depth. The roadmap includes multi-view synchronization when users possess both a phone and laptop.
• Expanded Exercise Library: Current ML weights cover 4 core functional movements. The team plans to incorporate sitting balance drills, gentle neck stretches, and ankle mobility routines trained on specialized geriatric datasets.

CONCLUSION

The MotionIQ project addresses a pressing, heartfelt societal challenge in contemporary Vietnam: assisting elderly parents in maintaining regular physical activity and preserving independent mobility while granting busy working children peace of mind.

Through an authentic, disciplined, and evidence-based approach — supported by an empirical survey of 50 families, 100% On-Device AI biomechanical tracking, published international datasets (UI-PRMD, KIMORE, EHE), and a balanced 4-month media and financial strategy with a 10,000,000 VND budget — MotionIQ proves that student-led innovation can create meaningful, accessible, and compassionate healthcare technology for the community.

The founding team expresses deep gratitude to the course instructors, academic advisors, and family participants whose mentorship and candid feedback brought MotionIQ from an initial concept to a validated, working prototype ready for real-world impact.