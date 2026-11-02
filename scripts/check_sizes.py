import re

with open("src/app/page.tsx", "r", encoding="utf-8") as f:
    text = f.read()

sizes = set(re.findall(r"fontSize:\s*['\"].*?['\"]", text))
print("Font sizes in page.tsx:")
for s in sorted(sizes):
    print(s)
