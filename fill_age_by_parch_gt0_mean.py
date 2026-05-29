import csv
import json
from pathlib import Path
from datetime import datetime

src = Path('dataset_streamlit_shell/data/current_filtered.csv')
log = Path('dataset_streamlit_shell/data/cleaning_log.jsonl')

with src.open('r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fields = reader.fieldnames

# Use current Chinese column names.
age_col = '年齡'
parch_col = '父母/子女數'

# Compute mean age among rows with parch > 0 and non-missing age.
ages = []
for row in rows:
    parch = row[parch_col].strip()
    age = row[age_col].strip()
    if parch != '' and float(parch) > 0 and age != '':
        ages.append(float(age))

if not ages:
    raise SystemExit('No valid ages found for parch > 0')

mean_age = sum(ages) / len(ages)
mean_age_str = f'{mean_age:.2f}'

affected = 0
for row in rows:
    parch = row[parch_col].strip()
    age = row[age_col].strip()
    if parch != '' and float(parch) > 0 and age == '':
        row[age_col] = mean_age_str
        affected += 1

with src.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

logobj = {
    'created_at': datetime.now().isoformat(timespec='seconds'),
    'actor': 'agent',
    'action': 'fill_missing_age_by_parch_gt0_mean',
    'columns': [age_col, parch_col],
    'rows': affected,
    'note': '以父母/子女數大於 0 的年齡平均值補齊符合條件的年齡空值。'
}
with log.open('a', encoding='utf-8') as f:
    f.write(json.dumps(logobj, ensure_ascii=False) + '\n')

print('mean_age', mean_age_str)
print('affected', affected)
