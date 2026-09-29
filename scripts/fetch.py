import urllib.request
import re
import html

req = urllib.request.Request('https://share.gemini.google/yEEZkGkvexTi', headers={'User-Agent': 'Mozilla/5.0'})
try:
    html_content = urllib.request.urlopen(req).read().decode('utf-8')
    strings = re.findall(r'"([^"]{50,})"', html_content)
    for s in strings:
        decoded = s.encode('utf-8').decode('unicode_escape')
        if 'Personal Trainer' in decoded or 'demo' in decoded or 'mobil' in decoded or 'HTML' in decoded or 'app' in decoded.lower():
            print(decoded)
            print("=" * 80)
except Exception as e:
    print(e)
