import csv
from pathlib import Path
from statistics import median

path = Path('dataset_streamlit_shell/data/current_filtered.csv')
with path.open('r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

ages = []
missing = 0
for r in rows:
    v = r['年齡'].strip()
    if v == '':
        missing += 1
    else:
        try:
            ages.append(float(v))
        except ValueError:
            pass

print('rows', len(rows))
print('missing', missing)
print('missing_rate', missing / len(rows))
print('median', median(ages))
print('mean', sum(ages)/len(ages))
print('by_sex')
for sex in ['male', 'female']:
    subset = [r for r in rows if r['性別'].strip() == sex]
    miss = sum(1 for r in subset if r['年齡'].strip() == '')
    print(sex, len(subset), miss, miss/len(subset))
