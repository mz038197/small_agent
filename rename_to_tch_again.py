import csv
import json
from pathlib import Path
from datetime import datetime

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
if old_fields == new_fields:
    print('already_traditional')
else:
    with src.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=new_fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({mapping.get(k, k): v for k, v in row.items()})

    log = {
        'created_at': datetime.now().isoformat(timespec='seconds'),
        'actor': 'agent',
        'action': 'rename_columns_traditional_chinese',
        'columns': old_fields,
        'rows': len(rows),
        'note': '將欄位名稱轉為繁體中文。'
    }
    with log_path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(log, ensure_ascii=False) + '\n')
    print('renamed', len(old_fields), 'columns')
    print(new_fields)
