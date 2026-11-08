"""Keep the script hash in the page's Content-Security-Policy in step with its inline script.

Run after any edit to the script in index.html:
    python tools/update-csp.py
Check without changing the file (used by CI):
    python tools/update-csp.py --check
"""

import base64
import hashlib
import io
import re
import sys
from pathlib import Path

PagePath = Path(__file__).resolve().parent.parent / 'index.html'
ScriptPattern = re.compile(r'<script>(.*?)</script>', re.S)
HashPattern = re.compile(r"script-src 'sha256-[A-Za-z0-9+/=]+'")


def ScriptHash(Page):
    Scripts = ScriptPattern.findall(Page)
    if len(Scripts) != 1:
        sys.exit(f'Expected one inline script in index.html, found {len(Scripts)}.')
    # Browsers hash the script after turning CRLF and CR into LF
    Text = Scripts[0].replace('\r\n', '\n').replace('\r', '\n')
    return base64.b64encode(hashlib.sha256(Text.encode('utf-8')).digest()).decode('ascii')


def Main():
    CheckOnly = '--check' in sys.argv[1:]
    Page = io.open(PagePath, encoding='utf-8', newline='').read()
    Matches = HashPattern.findall(Page)
    if len(Matches) != 1:
        sys.exit(f"Expected one script-src hash in the CSP, found {len(Matches)}.")

    Expected = f"script-src 'sha256-{ScriptHash(Page)}'"
    if Matches[0] == Expected:
        print('CSP script hash is up to date.')
        return

    if CheckOnly:
        sys.exit('CSP script hash is out of date, so the page will not run. '
                 'Run "python tools/update-csp.py" and commit the result.')

    io.open(PagePath, 'w', encoding='utf-8', newline='').write(Page.replace(Matches[0], Expected))
    print('CSP script hash updated.')


if __name__ == '__main__':
    Main()
