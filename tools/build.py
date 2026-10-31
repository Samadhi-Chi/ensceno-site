#!/usr/bin/env python3
"""Build a portable, dependency-free bilingual GitHub Pages site."""
import argparse
import html
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist"
parser = argparse.ArgumentParser()
parser.add_argument("--release", action="store_true", help="Require verified public contact details")
args = parser.parse_args()
config = json.loads((ROOT / "site.json").read_text())
ready = all(config.get(k) for k in ("owner", "support_email", "email_registered", "email_receiving_verified", "email_sending_verified"))
if args.release and not ready:
    parser.error("Public release requires a confirmed owner and registered mailbox with send/receive verification.")
preview = not args.release
escape = html.escape
OUT.mkdir(exist_ok=True)
shutil.copytree(ROOT / "assets", OUT / "assets", dirs_exist_ok=True)
shutil.copytree(ROOT / "open-source", OUT / "open-source", dirs_exist_ok=True)
(OUT / ".nojekyll").write_text("")

def page(lang, kind, copy):
    other = "en" if lang == "zh" else "zh"
    filename = {"help": "index.html", "privacy": "privacy.html", "open_source": "open-source.html"}[kind]
    info = copy[kind]
    title = f'{copy[kind + "_label"]} · {copy["brand"]}'
    sections = []
    for section in info["sections"]:
        body = section.get("html", "")
        for faq in section.get("faqs", []):
            body += f'<details><summary>{escape(faq["q"])}</summary><div class="answer">{faq["a"]}</div></details>'
        sections.append(f'<section class="article-section" id="{section["id"]}"><h2>{escape(section["title"])}</h2>{body}</section>')
    toc = ''.join(f'<a href="#{section["id"]}">{escape(section["title"])}</a>' for section in info["sections"])
    draft = f'<div class="preview-note" role="note">{escape(copy["draft"])}</div>' if preview else ''
    if kind == "help":
        intro_extra = f'''<div class="source-links"><a class="source-link" href="#jellyfin"><span class="source-icon" aria-hidden="true">J</span><span><strong>{copy["help"]["jellyfin"]}</strong><small>{copy["help"]["jellyfin_note"]}</small></span><span aria-hidden="true">↗</span></a><a class="source-link" href="#smb"><span class="source-icon" aria-hidden="true">S</span><span><strong>{copy["help"]["smb"]}</strong><small>{copy["help"]["smb_note"]}</small></span><span aria-hidden="true">↗</span></a></div><p class="scope">{copy["help"]["scope"]}</p>'''
    elif kind == "privacy":
        intro_extra = f'<p class="date">{copy["privacy"]["date_label"]} <time datetime="{config["policy_date"]}">{config["policy_date"]}</time></p><p class="privacy-summary">{copy["privacy"]["summary"]}</p>'
    else:
        intro_extra = f'<p class="scope">{info["scope"]}</p>'
    contact = (f'<a class="contact-button" href="mailto:{escape(config["support_email"], quote=True)}">{escape(copy["contact_button"])} <span aria-hidden="true">↗</span></a><p class="email-address">{escape(config["support_email"])}</p>' if ready else f'<p class="contact-pending">{escape(copy["contact_pending"])}</p>')
    base = config["base_url"].rstrip('/')
    canonical = f'{base}/{lang}/{"" if kind == "help" else filename}'
    head_links = '' if preview else f'<link rel="canonical" href="{canonical}">'
    help_current = ' aria-current="page"' if kind == 'help' else ''
    privacy_current = ' aria-current="page"' if kind == 'privacy' else ''
    return f'''<!doctype html>
<html lang="{copy["lang"]}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="dark"><meta name="referrer" content="no-referrer"><meta name="description" content="{escape(info["intro"], quote=True)}">{'<meta name="robots" content="noindex,nofollow">' if preview else ''}<title>{escape(title)}</title>{head_links}<link rel="alternate" hreflang="zh-Hans" href="../zh/{filename}"><link rel="alternate" hreflang="en" href="../en/{filename}"><link rel="icon" href="../assets/app-icon.png"><link rel="stylesheet" href="../assets/site.css"></head>
<body><a class="skip-link" href="#main">{copy["skip"]}</a>{draft}
<header class="site-header"><div class="header-inner"><a class="brand" href="index.html"><img src="../assets/app-icon.png" alt="" width="40" height="40"><span>{copy["brand"]}</span></a><span class="header-caption">{copy["support_label"]}</span><nav aria-label="{'主导航' if lang == 'zh' else 'Main navigation'}"><a href="index.html"{help_current}>{copy["help_label"]}</a><a href="privacy.html"{privacy_current}>{copy["privacy_label"]}</a><a class="language-link" href="../{other}/{filename}" lang="{'en' if other == 'en' else 'zh-Hans'}" hreflang="{'en' if other == 'en' else 'zh-Hans'}">{copy["switch_label"]}</a></nav></div></header>
<main id="main" tabindex="-1"><div class="hero"><p class="eyebrow">{info["eyebrow"]}</p><h1>{'<br>'.join(escape(line) for line in info["title"].splitlines())}</h1><p class="intro">{info["intro"]}</p>{intro_extra}</div><div class="reading-layout"><aside class="toc"><p>{copy["contents"]}</p><nav aria-label="{copy["contents"]}">{toc}<a href="#contact">{copy["contact_title"]}</a></nav></aside><article>{''.join(sections)}<section class="contact-panel" id="contact"><p class="eyebrow">{'联系开发者' if lang == 'zh' else 'Contact the developer'}</p><h2>{copy["contact_title"]}</h2><p>{copy["contact_intro"]}</p>{contact}<p class="contact-details">{copy["contact_checklist"]}</p><p class="owner">{'开发者' if lang == 'zh' else 'Developer'} · {escape(config["owner"])}</p></section></article></div></main>
<footer><p><a href="open-source.html">{copy["open_source_label"]}</a></p><p>{copy["footer"]}</p><p>© 2026 {escape(config["owner"])}</p></footer></body></html>'''

for lang in ("zh", "en"):
    copy = json.loads((ROOT / "content" / f"{lang}.json").read_text())
    (OUT / lang).mkdir(exist_ok=True)
    for kind, filename in (("help", "index.html"), ("privacy", "privacy.html"), ("open_source", "open-source.html")):
        (OUT / lang / filename).write_text(page(lang, kind, copy), encoding="utf-8")

(OUT / "index.html").write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><meta name="description" content="Ensceno support and privacy information in English and Chinese."><title>Ensceno · 入境</title><link rel="icon" href="assets/app-icon.png"><link rel="stylesheet" href="assets/site.css"></head><body class="language-home"><main><img class="welcome-icon" src="assets/app-icon.png" alt="" width="88" height="88"><p class="eyebrow">APPLE VISION PRO</p><h1>Ensceno <span lang="zh-Hans">· 入境</span></h1><p class="intro">Help & privacy <span lang="zh-Hans">／ 帮助与隐私</span></p><div class="language-options"><a href="zh/" lang="zh-Hans">中文 <span aria-hidden="true">↗</span></a><a href="en/" lang="en">English <span aria-hidden="true">↗</span></a></div></main></body></html>''', encoding="utf-8")
(OUT / "404.html").write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found · Ensceno</title></head><body><main><h1>Page not found / 页面不存在</h1><p><a href="/ensceno-site/">Ensceno support / 入境支持中心</a></p></main></body></html>''', encoding="utf-8")
(OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n" if preview else "User-agent: *\nAllow: /\n")
print(f'Built {"preview" if preview else "release"} site: {OUT}')
