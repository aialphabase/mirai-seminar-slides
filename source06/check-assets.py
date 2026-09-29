"""Read-only checks for session 06 visual replacement. Run after build.py."""
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
page = ROOT / 'sessions/06/index.html'
current = page.read_text()
original = subprocess.check_output(['git', 'show', 'f6c9145:sessions/06/index.html'], cwd=ROOT, text=True)

class SlideContent(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_section = False
        self.text = []
        self.count = 0
    def handle_starttag(self, tag, attrs):
        if tag == 'section':
            self.in_section = True
            self.count += 1
    def handle_endtag(self, tag):
        if tag == 'section':
            self.in_section = False
    def handle_data(self, data):
        if self.in_section and data.strip():
            self.text.append(data.strip())

before, after = SlideContent(), SlideContent()
before.feed(original)
after.feed(current)
assert before.count == after.count == 22
assert before.text == after.text, 'Slide text changed'
assert re.search(r'<script>(.*?)</script>', original, re.S).group(1) == re.search(r'<script>(.*?)</script>', current, re.S).group(1), 'Interaction code changed'
assets = set(re.findall(r"url\(['\"]?(assets/[^)'\"]+)", current))
new = [a for a in assets if '/news06/' in a]
for asset in new:
    assert (page.parent / asset).is_file(), asset
assert len(new) == 7, new
assert len(re.findall(r'background-image:url\(\'assets/news06/', current)) == 8
assert 'steps next-stage' in current
print('PASS: 22 slides; text and interaction script unchanged; 7 new assets / 9 placements; all new referenced assets exist.')
