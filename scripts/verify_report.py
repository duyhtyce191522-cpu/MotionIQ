import docx, sys
sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document('Final_MOTIONIQ.docx')

# 1. Check cantSplit and tblHeader
missing_cantsplit = 0
missing_tblheader = 0
for t_idx, tbl in enumerate(doc.tables):
    for r_idx, row in enumerate(tbl.rows):
        trPr = row._tr.get_or_add_trPr()
        if not any(el.tag.endswith('cantSplit') for el in trPr):
            missing_cantsplit += 1
        if r_idx == 0 and len(tbl.rows) > 1:
            if not any(el.tag.endswith('tblHeader') for el in trPr):
                missing_tblheader += 1

print(f'Missing cantSplit: {missing_cantsplit}')
print(f'Missing tblHeader: {missing_tblheader}')

# 2. Check full document text for defects
full_text = []
for p in doc.paragraphs:
    full_text.append(p.text)
for tbl in doc.tables:
    for row in tbl.rows:
        for cell in row.cells:
            full_text.append(cell.text)
doc_str = '\n'.join(full_text)

checks = [
    'MedTech Pioneers',
    'Kết quả phân tích',
    'Phân tích đối thủ',
    'KIẾN TRÚC GIẢI PHÁP',
    'với visibility_i',
    '10^-6 và',
    'Hông trái',
    '20 Đ',
    '1.000.000đ',
    'Rủi ro nhận diện',
    '0Inference',
    '\\%',
    'peoples',
    'CONCLUDE'
]

for c in checks:
    count = doc_str.count(c)
    print(f'Check "{c}": {count}')
