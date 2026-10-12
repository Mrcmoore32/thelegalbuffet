#!/usr/bin/env python3
"""Monthly link health check for The Legal Buffet.
Opens every external link on the site, flags dead/moved/hijacked ones.
Usage: check-links.py [--report PATH]
Writes a report; exit 0 = all good, exit 1 = problems found.
"""
import re, sys, glob, subprocess, json, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMEOUT = 20
WORKERS = 25

def extract_links():
    links = set()
    for page in glob.glob(os.path.join(SITE, '**', '*.html'), recursive=True):
        txt = open(page, errors='ignore').read()
        for m in re.finditer(r'href="(https?://[^"]+)"', txt):
            url = m.group(1)
            # skip anchors-only weirdness
            links.add(url)
    return sorted(links)

def check(url):
    """Returns (url, status, detail)."""
    try:
        r = subprocess.run(
            ['curl', '-sS', '-o', '/dev/null', '-w', '%{http_code} %{url_effective} %{time_total}',
             '-L', '--max-time', str(TIMEOUT), '--max-redirs', '5',
             '-A', 'Mozilla/5.0 (compatible; LegalBuffet-linkcheck/1.0)',
             url],
            capture_output=True, text=True, timeout=TIMEOUT + 10)
        parts = r.stdout.strip().split()
        if not parts:
            return (url, 'ERROR', (r.stderr.strip() or 'no response')[:120])
        code = parts[0]
        final = parts[1] if len(parts) > 1 else url
        if code.startswith('2') or code.startswith('3'):
            note = ''
            if urlparse(final).netloc != urlparse(url).netloc:
                note = f' -> redirects to {final}'
            return (url, 'OK', note)
        return (url, 'DEAD', f'HTTP {code}')
    except subprocess.TimeoutExpired:
        return (url, 'ERROR', 'timed out')
    except Exception as e:
        return (url, 'ERROR', str(e)[:120])

def main():
    links = extract_links()
    print(f'Checking {len(links)} unique external links...', flush=True)
    dead, errors, moved = [], [], []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(check, u): u for u in links}
        for f in as_completed(futs):
            url, status, detail = f.result()
            if status == 'DEAD':
                dead.append((url, detail))
            elif status == 'ERROR':
                errors.append((url, detail))
            elif detail:
                moved.append((url, detail))
    report = {
        'total': len(links),
        'dead': [{'url': u, 'detail': d} for u, d in sorted(dead)],
        'errors': [{'url': u, 'detail': d} for u, d in sorted(errors)],
        'moved_domains': [{'url': u, 'detail': d} for u, d in sorted(moved)],
    }
    out = sys.argv[sys.argv.index('--report') + 1] if '--report' in sys.argv else None
    text = [f"Link check: {len(links)} links, {len(dead)} dead, {len(errors)} errors, {len(moved)} domain-changes."]
    for u, d in sorted(dead):
        text.append(f'DEAD: {u} ({d})')
    for u, d in sorted(errors):
        text.append(f'ERROR: {u} ({d})')
    for u, d in sorted(moved):
        text.append(f'MOVED: {u}{d}')
    report_text = '\n'.join(text)
    if out:
        open(out, 'w').write(report_text)
        open(out + '.json', 'w').write(json.dumps(report, indent=1))
    print(report_text, flush=True)
    return 1 if (dead or errors) else 0

if __name__ == '__main__':
    sys.exit(main())
