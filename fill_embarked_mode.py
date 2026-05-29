import csv
import json
from pathlib import Path
from collections import Counter
from datetime import datetime

src = Path('dataset_streamlit_shell/data/current_filtered.csv')
log = Path('dataset_streamlit_shell/data/cleaning_log.jsonl')

with src.open('r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fields = reader.fieldnames

col = '登船港口'
values = [r[col].strip() for r in rows if r[col].strip()]
if not values:
    raise SystemExit('No non-missing values found')

mode = Counter(values).most_common(1)[0][0]
affected = 0
for row in rows:
    if row[col].strip() == '':
        row[col] = mode
        affected += 1

with src.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

logobj = {
    'created_at': datetime.now().isoformat(timespec='seconds'),
    'actor': 'agent',
    'action': 'fill_missing_embarked_mode',
    'columns': [col],
    'rows': affected,
    'note': f'以眾數 {mode} 補齊登船港口的空值。'
}
with log.open('a', encoding='utf-8') as f:
    f.write(json.dumps(logobj, ensure_ascii=False) + '\n')

print('mode', mode)
print('affected', affected)
