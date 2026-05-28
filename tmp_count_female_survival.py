import csv
from pathlib import Path

path = Path('dataset_streamlit_shell/data/current_filtered.csv')
with path.open('r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

female = [r for r in rows if r['Sex'].strip() == 'female']
survived_female = [r for r in female if r['Survived'].strip() == '1']

print('total_rows', len(rows))
print('female_count', len(female))
print('survived_female_count', len(survived_female))
print('probability', len(survived_female) / len(female))
