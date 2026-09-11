import os, sys

d = r'd:\node\games'
out = open(r'd:\node\corruption_report.txt', 'w', encoding='utf-8')
files = [f for f in sorted(os.listdir(d)) if f.endswith('.html') and f not in ('schulte_test.html', 'schulte_restored.html')]

for fname in files:
    path = os.path.join(d, fname)
    content = open(path, 'r', encoding='utf-8').read()
    idxs = [i for i, ch in enumerate(content) if ch == '\ufffd']
    if not idxs:
        continue
    out.write(f'=== {fname} ({len(idxs)} corrupted) ===\n')
    for i in idxs[:60]:
        before = content[max(0, i-12):i]
        after = content[i+1:i+13]
        out.write(f'  pos {i}: {repr(before)}|REPL|{repr(after)}\n')
    out.write('\n')

out.close()
print('Report written to d:\\node\\corruption_report.txt')