import csv
from pathlib import Path
from collections import Counter

path = Path('dataset_streamlit_shell/data/current_filtered.csv')
with path.open('r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

missing = sum(1 for r in rows if not r['Cabin'].strip())
non_missing = [r['Cabin'].strip() for r in rows if r['Cabin'].strip()]
print('rows', len(rows))
print('missing', missing)
print('missing_rate', missing / len(rows))
print('top_cabins', Counter(non_missing).most_common(10))
print('by_pclass_missing_rates')
for p in ['1', '2', '3']:
    subset = [r for r in rows if r['Pclass'].strip() == p]
    m = sum(1 for r in subset if not r['Cabin'].strip())
    print(p, len(subset), m, m / len(subset))
