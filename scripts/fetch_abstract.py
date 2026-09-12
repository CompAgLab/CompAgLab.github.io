#!/usr/bin/env python3
"""Fetch a publication abstract, cleaned and wrapped for publications.html.

    python3 scripts/fetch_abstract.py 10.1017/jfm.2024.525
    python3 scripts/fetch_abstract.py --html 10.1017/jfm.2024.525   # ready to paste

Source is OpenAlex, which stores abstracts as an inverted index and has had one
for every paper on this site so far -- including papers with no local PDF, which
is why it beats extracting from the PDF. Crossref is the fallback.

Publisher abstracts arrive with artefacts this cleans up:
  - LaTeX math delimiters ($Re = 450\\,000$ -> Re = 450,000)
  - AIAA's "View Video Presentation: <url>" prefix
  - stray backslash commands and doubled whitespace

Always eyeball the result before pasting. If no source has an abstract, copy it
from the PDF by hand -- never write one yourself.
"""
import argparse
import html
import json
import re
import sys
import textwrap
import urllib.parse
import urllib.request

MAILTO = "ethan.pickering@uga.edu"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": f"compaglab-site ({MAILTO})"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r)


def clean(text):
    text = re.sub(r"^View Video Presentation:\s*\S+\s*", "", text)
    text = re.sub(r"\$([^$]*)\$", lambda m: m.group(1), text)
    text = text.replace("\\,", ",").replace("\\%", "%").replace("\\times", " x ")
    text = re.sub(r"\\[a-zA-Z]+\{?|\}", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([.,;:)])", r"\1", text).replace("( ", "(")
    return html.escape(text, quote=False)


def from_openalex(doi):
    work = get("https://api.openalex.org/works/https://doi.org/" + doi)
    inverted = work.get("abstract_inverted_index")
    if not inverted:
        return None
    pos = {}
    for word, idxs in inverted.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def from_crossref(doi):
    msg = get("https://api.crossref.org/works/" + urllib.parse.quote(doi) +
              "?mailto=" + MAILTO)["message"]
    raw = msg.get("abstract")
    if not raw:
        return None
    return re.sub(r"<[^>]+>", " ", raw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doi")
    ap.add_argument("--html", action="store_true", help="emit a <details> block")
    args = ap.parse_args()
    doi = args.doi.replace("https://doi.org/", "").strip()

    text = None
    for name, fn in (("OpenAlex", from_openalex), ("Crossref", from_crossref)):
        try:
            text = fn(doi)
        except Exception as e:
            print(f"# {name}: {e}", file=sys.stderr)
            continue
        if text:
            print(f"# source: {name} ({len(text.split())} words)", file=sys.stderr)
            break
    if not text:
        sys.exit(f"no abstract for {doi} in OpenAlex or Crossref -- copy it from the PDF")

    text = clean(text)
    body = "\n".join("          " + ln for ln in textwrap.wrap(text, 96))
    if args.html:
        print("      <details>\n        <summary>Abstract</summary>\n        <p>")
        print(body)
        print("        </p>\n      </details>")
    else:
        print(text)


if __name__ == "__main__":
    sys.exit(main())
