import csv
from pathlib import Path
from collections import Counter

path = Path('dataset_streamlit_shell/data/current_filtered.csv')
with path.open('r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

stats = {}
for sex in ('female', 'male'):
    subset = [r for r in rows if r['Sex'].strip() == sex]
    survived = [r for r in subset if r['Survived'].strip() == '1']
    stats[sex] = (len(subset), len(survived), len(survived) / len(subset))

female = [r for r in rows if r['Sex'].strip() == 'female']
fs = [r for r in female if r['Survived'].strip() == '1']
fd = [r for r in female if r['Survived'].strip() == '0']
ms = [r for r in rows if r['Sex'].strip() == 'male' and r['Survived'].strip() == '1']

print('sex_stats', stats)
print('female_survivors_class', Counter(r['Pclass'] for r in fs))
print('female_non_survivors_class', Counter(r['Pclass'] for r in fd))
print('male_survivors_class', Counter(r['Pclass'] for r in ms))
