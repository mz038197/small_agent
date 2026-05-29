import csv
from pathlib import Path
from collections import Counter

path = Path('dataset_streamlit_shell/data/current_filtered.csv')
with path.open('r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

vals = [r['登船港口'].strip() for r in rows]
print('count', len(vals))
print('missing', sum(1 for v in vals if v == ''))
print('counts', Counter(v if v != '' else '(空白)' for v in vals))
