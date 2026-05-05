from pathlib import Path
import re, html
s = Path('article.html').read_text(encoding='utf-8', errors='ignore')
keys = ['<title>', 'articleBody', 'entry-content', 'jeg_inner_content', 'content-inner', 'post-content', 'OpenClaw', 'Hermes', 'OAuth', 'OUath']
out=[]
out.append(f'len={len(s)}')
for key in keys:
    out.append(f'{key}: {s.find(key)}')
for pat in [r'<title>(.*?)</title>', r'<meta property="og:title" content="(.*?)"', r'<meta property="og:description" content="(.*?)"', r'<meta name="description" content="(.*?)"']:
    m=re.search(pat,s,re.S|re.I)
    out.append('META: '+(html.unescape(m.group(1).strip()) if m else 'NA'))
Path('article_report.txt').write_text('\n'.join(out), encoding='utf-8')
