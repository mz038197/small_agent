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

new_field = '是否有船艙'
if new_field not in fields:
    out_fields = fields + [new_field]
    for row in rows:
        row[new_field] = '1' if row['船艙號'].strip() else '0'

    with src.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(rows)

    logobj = {
        'created_at': datetime.now().isoformat(timespec='seconds'),
        'actor': 'agent',
        'action': 'add_cabin_indicator',
        'columns': ['船艙號', new_field],
        'rows': len(rows),
        'note': '新增是否有船艙二元欄位以保留船艙資訊。'
    }
    with log.open('a', encoding='utf-8') as f:
        f.write(json.dumps(logobj, ensure_ascii=False) + '\n')

    print('done', len(rows))
else:
    print('exists')
