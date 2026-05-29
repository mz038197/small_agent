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

remove_field = '船艙號'
if remove_field in fields:
    out_fields = [c for c in fields if c != remove_field]
    for row in rows:
        row.pop(remove_field, None)

    with src.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(rows)

    logobj = {
        'created_at': datetime.now().isoformat(timespec='seconds'),
        'actor': 'agent',
        'action': 'drop_cabin_column',
        'columns': [remove_field],
        'rows': len(rows),
        'note': '刪除缺失率過高的船艙號欄位。'
    }
    with log.open('a', encoding='utf-8') as f:
        f.write(json.dumps(logobj, ensure_ascii=False) + '\n')

    print('dropped', remove_field, 'rows', len(rows))
else:
    print('not_found')
