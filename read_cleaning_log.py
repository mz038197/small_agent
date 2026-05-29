from pathlib import Path
path = Path('dataset_streamlit_shell/data/cleaning_log.jsonl')
print(path.read_text(encoding='utf-8'))
