import csv
from pathlib import Path
from datetime import datetime
import json

src = Path('dataset_streamlit_shell/data/current_filtered.csv')
log_path = Path('dataset_streamlit_shell/data/cleaning_log.jsonl')

mapping = {
    'PassengerId': '乘客編號',
    'Survived': '是否存活',
    'Pclass': '艙等',
    'Name': '姓名',
    'Sex': '性別',
    'Age': '年齡',
    'SibSp': '兄弟姐妹/配偶數',
    'Parch': '父母/子女數',
    'Ticket': '票號',
    'Fare': '票價',
    'Cabin': '船艙號',
    'Embarked': '登船港口',
}

with src.open('r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    old_fields = reader.fieldnames

new_fields = [mapping.get(c, c) for c in old_fields]

with src.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=new_fields)
    writer.writeheader()
    for row in rows:
        writer.writerow({mapping.get(k, k): v for k, v in row.items()})

log = {
    'timestamp': datetime.now().isoformat(timespec='seconds'),
    'action': 'rename_columns_to_traditional_chinese',
    'file': str(src).replace('\\', '/'),
    'affected_rows': len(rows),
    'affected_columns': old_fields,
    'new_columns': new_fields,
}
with log_path.open('a', encoding='utf-8') as f:
    f.write(json.dumps(log, ensure_ascii=False) + '\n')

print('renamed', len(old_fields), 'columns for', len(rows), 'rows')
print('new_fields', new_fields)
