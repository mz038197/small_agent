from pathlib import Path
import re, html, json
s = Path('article.html').read_text(encoding='utf-8', errors='ignore')

# 1) Try JSON-LD articleBody
bodies=[]
for m in re.finditer(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', s, re.S|re.I):
    raw = html.unescape(m.group(1)).strip()
    try:
        data = json.loads(raw)
    except Exception:
        continue
    stack=[data]
    while stack:
        x=stack.pop()
        if isinstance(x, dict):
            if 'articleBody' in x:
                bodies.append(x.get('articleBody') or '')
            stack.extend(x.values())
        elif isinstance(x, list):
            stack.extend(x)

# 2) fallback: entry-content div rough strip
text='\n\n'.join(bodies)
if not text:
    m = re.search(r'<div[^>]+class=["\'][^"\']*(?:entry-content|content-inner)[^"\']*["\'][^>]*>(.*?)</div>\s*</div>', s, re.S|re.I)
    if m:
        frag=m.group(1)
        frag=re.sub(r'<script.*?</script>|<style.*?</style>', '', frag, flags=re.S|re.I)
        frag=re.sub(r'<[^>]+>', '\n', frag)
        text=html.unescape(frag)

text = re.sub(r'\r', '', text)
text = re.sub(r'\n{3,}', '\n\n', text)
text = re.sub(r'[ \t]{2,}', ' ', text).strip()
Path('koc_text.txt').write_text(text[:20000], encoding='utf-8')
print('bodies', len(bodies), 'chars', len(text))
