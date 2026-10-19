#!/usr/bin/env python3
"""Render with Quarto when available, or the bundled Pandoc/Reveal.js fallback.

The fallback is an HTML preview renderer, not an implementation of Quarto.
It supports this package's static Markdown and embeds its existing Reveal.js
runtime. It does not execute code or reproduce arbitrary Quarto extensions.
"""
from pathlib import Path
import argparse
import html
import re
import shutil
import subprocess
import base64

ROOT = Path(__file__).resolve().parents[1]


def markdown(path, slide=False):
    args = ['pandoc', str(path), '--from=markdown',
            '--to=revealjs' if slide else '--to=html5']
    if slide:
        args.append('--slide-level=2')
    result = subprocess.run(args, capture_output=True, text=True, check=True).stdout
    result = re.sub(r'(href="[^"#?]+)\.qmd(["#?])', r'\1.html\2', result)
    if slide:
        def embed_image(match):
            src = match.group(1)
            if src.startswith(('https:', 'http:', 'data:')):
                return match.group(0)
            image_path = (path.parent / src).resolve()
            mime = 'image/png' if image_path.suffix.lower() == '.png' else 'image/svg+xml'
            encoded = base64.b64encode(image_path.read_bytes()).decode('ascii')
            return 'src="data:' + mime + ';base64,' + encoded + '"'
        result = re.sub(r'src="([^"]+)"', embed_image, result)
    return result


def title(path):
    match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$',
                      path.read_text(), re.M)
    return match.group(1) if match else path.stem


def website_page(name):
    path = ROOT / name
    label = html.escape(title(path))
    navigation = [('index.html', 'Week 6'), ('slides/day6.html', 'Slides'),
                  ('reflection.html', 'Final reflection'),
                  ('resources.html', 'Sources and further reading')]
    nav = ''.join(f'<a href="{url}">{text}</a>' for url, text in navigation)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{label} | DS 115</title>'
            '<link rel="stylesheet" href="assets/site.css"></head><body>'
            f'<nav class="course-nav" aria-label="Course navigation">{nav}</nav>'
            f'<main class="course-main"><h1>{label}</h1>{markdown(path)}</main>'
            '<footer class="course-foot">DS 115: Exploring Data Science</footer>'
            '</body></html>')


def slide_page():
    assets = ROOT / 'assets' / 'vendor'
    css = (assets / 'course-preview.css').read_text()
    css += '\n' + (ROOT / 'slides' / 'day6.css').read_text()
    js = (assets / 'reveal.js').read_text()
    notes = (assets / 'notes.js').read_text()
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>DS 115 Week 6: Where Can Data Science Take Me?</title>'
            f'<style>{css}</style></head><body>'
            '<div class="reveal"><div class="slides">'
            f'{markdown(ROOT / "slides/day6.qmd", slide=True)}</div></div>'
            f'<script>{js}</script><script>{notes}</script>'
            '<script>Reveal.initialize({width:1600,height:900,margin:0.06,'
            'minScale:0.2,maxScale:2,center:false,controls:true,progress:true,'
            'slideNumber:"c/t",transition:"fade",hash:true,plugins:[RevealNotes]});'
            '</script></body></html>')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fallback', action='store_true',
                        help='Use Pandoc even when Quarto is installed')
    args = parser.parse_args()
    if shutil.which('quarto') and not args.fallback:
        subprocess.run(['quarto', 'render'], cwd=ROOT, check=True)
        (ROOT / 'docs' / '.nojekyll').touch()
        return
    if not shutil.which('pandoc'):
        raise SystemExit('Install Quarto, or install Pandoc for the fallback renderer.')
    docs = ROOT / 'docs'
    (docs / 'slides').mkdir(parents=True, exist_ok=True)
    (docs / 'assets').mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / 'assets/site.css', docs / 'assets/site.css')
    shutil.copy2(ROOT / 'assets/survey-qr.png', docs / 'assets/survey-qr.png')
    for name in ['index.qmd', 'reflection.qmd', 'resources.qmd']:
        (docs / Path(name).with_suffix('.html')).write_text(website_page(name))
    (docs / 'slides/day6.html').write_text(slide_page())
    (docs / '.nojekyll').touch()
    print('Rendered static HTML preview into docs using Pandoc and bundled Reveal.js.')
    print('Quarto source is included. Run quarto render for a native Quarto build.')


if __name__ == '__main__':
    main()

