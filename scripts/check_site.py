#!/usr/bin/env python3
"""Structural checks for the CompAgLab static site.

Run from the repo root:  python3 scripts/check_site.py
Exits non-zero if anything fails, so it works as a pre-push gate.

Checks, in order:
  1. Every HTML page's tags balance (a stray </article> silently reflows a page).
  2. Every local src=/href= target exists on disk (catches PDFs linked but never copied).
  3. publications.html invariants: one links block per entry, no empty entries,
     every entry carries an abstract, figureless entries carry .pub-item-nofigure.
  4. people.html invariants: every person card has a photo that exists.
  5. Zoomable figures: any img[data-full] points at a file that exists, and
     every figure inside .pub-image / .pillar-media is zoomable.
"""
import os
import re
import sys
from html.parser import HTMLParser

PAGES = ["index.html", "research.html", "people.html", "publications.html"]
VOID = {"meta", "link", "img", "br", "hr", "input", "source", "area",
        "base", "col", "embed", "param", "track", "wbr"}

failures = []


def fail(msg):
    failures.append(msg)
    print(f"  FAIL {msg}")


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"stray </{tag}> at {self.getpos()}")
            return
        open_tag, pos = self.stack.pop()
        if open_tag != tag:
            self.errors.append(
                f"</{tag}> at {self.getpos()} closes <{open_tag}> opened at {pos}")


def check_balance_and_assets():
    for page in PAGES:
        print(f"{page}:")
        html = open(page, encoding="utf-8").read()
        parser = Balance()
        parser.feed(html)
        for err in parser.errors:
            fail(f"{page}: {err}")
        for tag, pos in parser.stack:
            fail(f"{page}: <{tag}> opened at {pos} never closed")
        for url in re.findall(r'(?:src|href|data-full)="([^"]+)"', html):
            if url.startswith(("http://", "https://", "#", "mailto:", "data:")):
                continue
            if not os.path.exists(url.split("#")[0]):
                fail(f"{page}: links missing local file {url}")
        if not parser.errors and not parser.stack:
            print("  tags balanced")


def articles(html, cls):
    pattern = r'<article class="' + cls + r'[^"]*">((?:(?!</article>).)*?)</article>'
    return re.findall(pattern, html, re.S)


def title_of(body, tag="h3"):
    m = re.search(rf"<{tag}>(.*?)</{tag}>", body, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else "(untitled)"


def check_publications():
    print("publications.html invariants:")
    html = open("publications.html", encoding="utf-8").read()
    entries = articles(html, "pub-item")
    print(f"  {len(entries)} entries, {sum('pub-image' in e for e in entries)} with a figure")
    for body in entries:
        name = title_of(body)[:60]
        n_links = body.count('<div class="pub-links">')
        if n_links != 1:
            fail(f"publications: {n_links} link blocks (expected 1) in {name!r}")
        elif not re.search(r'rel="noreferrer">[^<]+</a>', body):
            fail(f"publications: link block is empty in {name!r}")
        for field in ("pub-authors", "pub-venue"):
            if field not in body:
                fail(f"publications: missing .{field} in {name!r}")
        if "<summary>Abstract</summary>" not in body:
            fail(f"publications: no abstract in {name!r} "
                 f"(fetch one: python3 scripts/fetch_abstract.py <doi>)")
    # the 180px/1fr grid squeezes text into the image column without this class
    for m in re.finditer(r'<article class="(pub-item[^"]*)">((?:(?!</article>).)*?)</article>',
                         html, re.S):
        cls, body = m.group(1), m.group(2)
        has_fig = "pub-image" in body
        tagged = "pub-item-nofigure" in cls
        if has_fig and tagged:
            fail(f"publications: has a figure but is tagged nofigure: {title_of(body)[:60]!r}")
        if not has_fig and not tagged:
            fail(f"publications: no figure and not tagged nofigure: {title_of(body)[:60]!r}")


def check_zoomable():
    """Figures are only enlargeable if lightbox.js is loaded and they opt in."""
    print("zoomable figures:")
    for page in ("publications.html", "research.html"):
        html = open(page, encoding="utf-8").read()
        figures = re.findall(r'<div class="(?:pub-image|pillar-media)"[^>]*>\s*(<img [^>]*/>)', html)
        missing = [f for f in figures if "data-zoomable" not in f]
        for f in missing:
            src = re.search(r'src="([^"]+)"', f)
            fail(f"{page}: figure not zoomable: {src.group(1) if src else f[:60]}")
        if figures and "lightbox.js" not in html:
            fail(f"{page}: has zoomable figures but does not load lightbox.js")
        print(f"  {page}: {len(figures) - len(missing)}/{len(figures)} figures zoomable")


def check_people():
    print("people.html invariants:")
    html = open("people.html", encoding="utf-8").read()
    cards = articles(html, "person-card")
    print(f"  {len(cards)} person cards")
    for body in cards:
        name = title_of(body, "h3") if "<h3>" in body else title_of(body, "h2")
        if "person-role" not in body:
            fail(f"people: missing .person-role for {name!r}")
        img = re.search(r'<img src="([^"]+)"', body)
        if not img:
            fail(f"people: no photo for {name!r}")
        elif not os.path.exists(img.group(1)):
            fail(f"people: photo missing on disk for {name!r}: {img.group(1)}")


def main():
    if not os.path.exists("publications.html"):
        sys.exit("run this from the repo root")
    check_balance_and_assets()
    check_publications()
    check_zoomable()
    check_people()
    print()
    if failures:
        print(f"{len(failures)} problem(s) found")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
