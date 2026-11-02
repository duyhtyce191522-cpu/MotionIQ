import os
import re

src_dir = "src"
print("Scanning for font issues in:", src_dir)

font_issues = []

for root, dirs, files in os.walk(src_dir):
    for f in files:
        if f.endswith((".tsx", ".ts", ".css", ".module.css")):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8", errors="ignore") as file:
                lines = file.readlines()
            for idx, line in enumerate(lines):
                # Check for font family overrides or odd fonts
                if "fontfamily" in line.lower() or "font-family" in line.lower():
                    font_issues.append((p, idx + 1, line.strip()))
                elif "font-serif" in line:
                    font_issues.append((p, idx + 1, line.strip()))
                elif "quicksand" in line.lower():
                    font_issues.append((p, idx + 1, line.strip()))
                elif "comic" in line.lower():
                    font_issues.append((p, idx + 1, line.strip()))

print(f"Total font issues / declarations found: {len(font_issues)}")
for p, line_no, content in font_issues:
    print(f"{p}:{line_no} -> {content[:100]}")

