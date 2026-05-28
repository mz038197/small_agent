import csv
from pathlib import Path

in_path = Path('dataset_streamlit_shell/data/current_filtered.csv')
out_path = Path('dataset_streamlit_shell/data/current_filtered.csv')

rows = []
with in_path.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for r in reader:
        cabin = (r.get('Cabin') or '').strip()
        if cabin == '' or cabin.lower() == 'nan':
            r['Cabin'] = 'Unknown'
        rows.append(r)

with out_path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print('updated rows=', len(rows))
print('unknown_count=', sum(1 for r in rows if r['Cabin'] == 'Unknown'))
