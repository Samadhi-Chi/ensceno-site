#!/usr/bin/env python3
"""Check page links, language parity, and the absence of third-party embeds."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.links, self.h1, self.lang = path, set(), [], 0, None
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate id: {self.path}: {attrs["id"]}'
            self.ids.add(attrs['id'])
        if tag == 'html': self.lang = attrs.get('lang')
        if tag == 'h1': self.h1 += 1
        assert tag not in ('script', 'iframe', 'form'), f'Unexpected script, embed or form: {self.path}'
        for attr in ('src', 'href'):
            if attr in attrs:
                url = urlsplit(attrs[attr])
                if tag in ('img', 'script', 'iframe') or (tag == 'link' and attrs.get('rel') == 'stylesheet'):
                    assert not url.netloc, f'External asset: {self.path}: {url.geturl()}'
                self.links.append(url)

pages = {p.resolve(): Page(p) for p in DIST.rglob('*.html')}
for path, page in pages.items():
    assert page.h1 == 1 and page.lang, f'Heading or language error: {path}'
    for url in page.links:
        if url.scheme or url.netloc: continue
        target_path = unquote(url.path)
        if target_path.startswith('/ensceno-site/'):
            target = DIST / target_path.removeprefix('/ensceno-site/')
        elif target_path:
            target = path.parent / target_path
        else:
            target = path
        if target.is_dir(): target /= 'index.html'
        target = target.resolve()
        assert target.is_relative_to(DIST.resolve()) and target.exists(), f'Broken link: {path}: {url.geturl()}'
        if url.fragment:
            assert target in pages and url.fragment in pages[target].ids, f'Broken anchor: {path}: {url.geturl()}'
copies = [json.loads((ROOT / 'content' / f'{lang}.json').read_text()) for lang in ('zh','en')]
for kind in ('help','privacy','open_source'):
    assert [s['id'] for s in copies[0][kind]['sections']] == [s['id'] for s in copies[1][kind]['sections']]
assert len(copies[0]['help']['sections'][-1]['faqs']) == len(copies[1]['help']['sections'][-1]['faqs'])
import hashlib
for manifest_path in (DIST / 'open-source' / 'releases').glob('*/manifest.json'):
    manifest = json.loads(manifest_path.read_text())
    archive = manifest_path.parent / manifest['file']
    assert archive.stat().st_size == manifest['bytes'], f'Archive size mismatch: {archive}'
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == manifest['sha256'], f'Archive hash mismatch: {archive}'
print(f'PASS: {len(pages)} pages; local links and anchors; bilingual section parity; no external embeds or scripts.')
