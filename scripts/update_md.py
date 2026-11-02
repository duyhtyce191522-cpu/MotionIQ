import os
import shutil

MD_PATH = "Final_MOTIONIQ.md"

with open("Final_MOTIONIQ.md", "r", encoding="utf-8") as f:
    content = f.read()

# Synchronize page numbers in markdown
page_replacements = [
    ("Table 1.1:** Founding Team Competency Profiles & RACI Governance Matrix (Page 7)", "Table 1.1:** Founding Team Competency Profiles & RACI Governance Matrix (Page 8)"),
    ("Table 2.1:** Quantitative Field Survey Findings & Statistical Breakdown (N = 50) (Page 9)", "Table 2.1:** Quantitative Field Survey Findings & Statistical Breakdown (N = 50) (Page 9)"),
    ("Table 2.2:** Competitive Landscape Analysis & Strategic Positioning Differentiation (Page 11)", "Table 2.2:** Competitive Landscape Analysis & Strategic Positioning Differentiation (Page 11)"),
    ("Table 3.1:** 9-Block Business Model Canvas (BMC) Framework (Page 12)", "Table 3.1:** 9-Block Business Model Canvas (BMC) Framework (Page 12)"),
    ("Table 3.2:** Profile of Model Files and Core Algorithms in Project Source Code (Page 13)", "Table 3.2:** Profile of Model Files and Core Algorithms in Project Source Code (Page 13)"),
    ("Table 3.2-Joints:** 22-Joint Standard UI-PRMD Anatomical Mapping & Forward Kinematics (Page 20)", "Table 3.2-Joints:** 22-Joint Standard UI-PRMD Anatomical Mapping & Forward Kinematics (Page 16)"),
    ("Table 3.2a:** Actual Parameters Extracted from Weights File uiprmdQualityModel.json (Page 23)", "Table 3.2a:** Actual Parameters Extracted from Weights File uiprmdQualityModel.json (Page 17)"),
    ("Table 3.3:** Summary Table of 4 Standardized Functional Exercises in MotionIQ (Page 28)", "Table 3.3:** Summary Table of 4 Standardized Functional Exercises in MotionIQ (Page 21)"),
    ("Table 3.4:** Results of 5 Actual MVP Prototype Testing Sessions (Page 30)", "Table 3.4:** Results of 5 Actual MVP Prototype Testing Sessions (Page 22)"),
    ("Table 4.1:** Communication Channels & Operational Implementation Methods (Page 31)", "Table 4.1:** Communication Channels & Operational Implementation Methods (Page 23)"),
    ("Table 4.2:** 4-Month Communication Implementation Roadmap (Page 32)", "Table 4.2:** 4-Month Communication Implementation Roadmap (Page 24)"),
    ("Table 4.3:** Proposed Pricing Structure of MotionIQ (Page 33)", "Table 4.3:** Proposed Pricing Structure of MotionIQ (Page 24)"),
    ("Table 4.4:** 4-Month Lean Student Media Budget Allocation (10,000,000 VND) (Page 33)", "Table 4.4:** 4-Month Lean Student Media Budget Allocation (10,000,000 VND) (Page 25)"),
    ("Table 4.5:** Target Customer Segments & 4-Month Conversion Funnel KPIs (Page 34)", "Table 4.5:** Target Customer Segments & 4-Month Conversion Funnel KPIs (Page 26)"),
    ("Table 4.6:** Early Access Tier Subscription Monthly Revenue Forecast (Page 35)", "Table 4.6:** Early Access Tier Subscription Monthly Revenue Forecast (Page 26)"),
    ("Table 4.7:** Operational Break-Even vs. Full Capital Recovery Analysis (Page 36)", "Table 4.7:** Operational Break-Even vs. Full Capital Recovery Analysis (Page 27)"),
    ("Table 5.1:** Identified Operational Risk Matrix & Concrete Mitigation Strategies (Page 37)", "Table 5.1:** Identified Operational Risk Matrix & Concrete Mitigation Strategies (Page 28)")
]

for old, new in page_replacements:
    content = content.replace(old, new)

with open("Final_MOTIONIQ.md", "w", encoding="utf-8") as f:
    f.write(content)

with open("MotionIQ_Final_Report_EXE101_EN.md", "w", encoding="utf-8") as f:
    f.write(content)

# Replicate to target paths
shutil.copyfile("Final_MOTIONIQ.md", "public/Final_MOTIONIQ.md")
shutil.copyfile("MotionIQ_Final_Report_EXE101_EN.md", "public/MotionIQ_Final_Report_EXE101_EN.md")
shutil.copyfile("Final_MOTIONIQ.md", r"C:\Users\PC\Downloads\Final_MOTIONIQ.md")
shutil.copyfile("MotionIQ_Final_Report_EXE101_EN.md", r"C:\Users\PC\Downloads\MotionIQ_Final_Report_EXE101_EN.md")
shutil.copyfile("Final_MOTIONIQ.md", r"C:\Users\PC\.gemini\antigravity\brain\2528946a-763d-44fc-b905-a9488a80b69a\Final_MOTIONIQ.md")
shutil.copyfile("MotionIQ_Final_Report_EXE101_EN.md", r"C:\Users\PC\.gemini\antigravity\brain\2528946a-763d-44fc-b905-a9488a80b69a\MotionIQ_Final_Report_EXE101_EN.md")

print("All Markdown files updated and synchronized successfully!")

