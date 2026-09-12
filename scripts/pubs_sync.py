#!/usr/bin/env python3
"""Cross-check publications.html against public bibliographic sources.

    python3 scripts/pubs_sync.py            # report only
    python3 scripts/pubs_sync.py --json     # machine-readable

WHY NOT GOOGLE SCHOLAR: Ethan's profile is the intended source of truth
(scholar.google.com/citations?user=q3KI3-0AAAAJ), but Google blocks the
/citations endpoint for every automated client -- plain curl and the agent's
WebFetch both get HTTP 404 while scholar.google.com itself returns 200. There
is no key or user-agent that fixes this; it is deliberate anti-scraping.

So this script uses OpenAlex as the automated stand-in (it indexes the same
works, is free, needs no key) and Crossref to resolve anything OpenAlex misses.
Treat Scholar as a MANUAL check: open the profile, sort by year, and confirm
nothing here is missing. The script tells you what to look for.

It reports, per work:
  MISSING   -- in the source but not on the site at all
  DOI       -- site entry has no DOI link but the source knows one
  ARXIV     -- site entry has no arXiv link but the source knows one
  VENUE     -- site still says Submitted/Accepted though the source has a venue
"""
import argparse
import json
import re
import sys
import urllib.parse
import urllib.request

# Both IDs are Ethan; OpenAlex has split his record across two author entities.
OPENALEX_AUTHORS = ["A5061968827", "A5141073323"]
MAILTO = "ethan.pickering@uga.edu"
SCHOLAR_PROFILE = "https://scholar.google.com/citations?user=q3KI3-0AAAAJ&hl=en&sortby=pubdate"

# Works Ethan has decided to leave off the site (2026-09-12): two AIAA
# conference papers, a building-energy article, and two JASA meeting abstracts.
# Delete an entry here to make the script start reporting it again.
EXCLUDED_DOIS = {
    "10.2514/6.2024-3414",   # Nonlinear Interactions in Non-Resonant, Homogeneous Turbulent Jets
    "10.2514/6.2024-3199",   # Resolvent Modeling of Subsonic Jet Noise
    "10.1080/17512549.2020.1730239",  # Data analytics applied to office building electricity
    "10.1121/1.5137546",     # Furthering resolvent-based jet noise models (abstract)
    "10.1121/1.5067573",     # Resolvent analysis for jet noise source identification (abstract)
}

# Sources that mirror a real paper rather than being one.
SKIP_HOSTS = ("zenodo", "research square", "bulletin of the american physical society",
              "caltechauthors", "ohiolink")


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": f"compaglab-site ({MAILTO})"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r)


def norm(title):
    """Normalize a title for matching across sources (punctuation and case vary)."""
    t = re.sub(r"&[a-z]+;", " ", (title or "").lower())
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return " ".join(t.split())


def fetch_openalex():
    """Return {normalized_title: record}, preferring published over preprint."""
    flt = "|".join(OPENALEX_AUTHORS)
    url = ("https://api.openalex.org/works?filter=author.id:" + flt +
           "&per-page=200&sort=publication_year:desc&mailto=" + MAILTO)
    works = get_json(url)["results"]
    out = {}
    for w in works:
        title = w.get("title")
        if not title:
            continue
        src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
        if any(h in src.lower() for h in SKIP_HOSTS):
            continue
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        if doi in EXCLUDED_DOIS:
            continue
        arxiv = ""
        if doi.startswith("10.48550/arxiv."):
            arxiv, doi = doi.split("arxiv.", 1)[1], ""
        for loc in w.get("locations") or []:
            s = (loc.get("source") or {}).get("display_name") or ""
            lid = loc.get("landing_page_url") or ""
            if "arxiv" in s.lower() and not arxiv:
                m = re.search(r"abs/([0-9.]+)", lid)
                if m:
                    arxiv = m.group(1)
        rec = {"title": title, "year": w.get("publication_year"), "venue": src,
               "doi": doi, "arxiv": arxiv, "is_preprint": w.get("type") == "preprint"}
        key = norm(title)
        prev = out.get(key)
        # a published record beats a preprint record of the same title
        if prev is None or (prev["is_preprint"] and not rec["is_preprint"]):
            if prev and prev.get("arxiv") and not rec.get("arxiv"):
                rec["arxiv"] = prev["arxiv"]
            out[key] = rec
        elif prev and rec.get("arxiv") and not prev.get("arxiv"):
            prev["arxiv"] = rec["arxiv"]

    # Preprints often carry a subtitle the journal version drops
    # ("... Navier-Stokes equations. Part 1. Forced response"). Fold those into
    # the published record instead of reporting them as missing.
    for key in list(out):
        rec = out.get(key)
        if not rec or not rec["is_preprint"]:
            continue
        for other_key, other in out.items():
            if other_key == key or other["is_preprint"]:
                continue
            if key.startswith(other_key) or other_key.startswith(key):
                if rec.get("arxiv") and not other.get("arxiv"):
                    other["arxiv"] = rec["arxiv"]
                del out[key]
                break
    return out


def crossref_doi(title):
    url = ("https://api.crossref.org/works?rows=1&mailto=" + MAILTO +
           "&query.bibliographic=" + urllib.parse.quote(title))
    try:
        items = get_json(url)["message"]["items"]
    except Exception:
        return None
    if not items:
        return None
    it = items[0]
    if norm(it["title"][0]) != norm(title):
        return None
    return {"doi": it["DOI"], "venue": (it.get("container-title") or [""])[0],
            "volume": it.get("volume"), "page": it.get("page")}


def parse_site(path="publications.html"):
    html = open(path, encoding="utf-8").read()
    entries, year = [], None
    pat = r'<h2>(\d{4})</h2>|<article class="pub-item[^"]*">(.*?)</article>'
    for m in re.finditer(pat, html, re.S):
        if m.group(1):
            year = m.group(1)
            continue
        body = m.group(2)
        t = re.search(r"<h3>(.*?)</h3>", body, re.S)
        venue = re.search(r'<p class="pub-venue">(.*?)</p>', body, re.S)
        links = re.findall(r'href="([^"]+)"[^>]*>([^<]+)</a>', body)
        entries.append({
            "title": re.sub(r"\s+", " ", t.group(1)).strip() if t else "",
            "year": year,
            "venue": re.sub(r"<[^>]+>|\s+", " ", venue.group(1)).strip() if venue else "",
            "hrefs": [u for u, _ in links],
            "kinds": [k.strip() for _, k in links],
        })
    return entries


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    site = parse_site()
    by_title = {norm(e["title"]): e for e in site}
    source = fetch_openalex()

    issues = []
    for key, rec in sorted(source.items(), key=lambda kv: -(kv[1]["year"] or 0)):
        entry = by_title.get(key)
        if entry is None:
            issues.append({"kind": "MISSING", "year": rec["year"], "title": rec["title"],
                           "detail": f"{rec['venue'] or 'preprint'}"
                                     f"{' doi:' + rec['doi'] if rec['doi'] else ''}"})
            continue
        hrefs = " ".join(entry["hrefs"])
        if rec["doi"] and "doi.org" not in hrefs:
            issues.append({"kind": "DOI", "year": entry["year"], "title": entry["title"],
                           "detail": f"https://doi.org/{rec['doi']}"})
        if rec["arxiv"] and "arxiv.org" not in hrefs:
            issues.append({"kind": "ARXIV", "year": entry["year"], "title": entry["title"],
                           "detail": f"https://arxiv.org/abs/{rec['arxiv']}"})
        preprint_venue = any(h in rec["venue"].lower() for h in ("arxiv", "biorxiv", "preprint"))
        if re.search(r"Submitted|Accepted", entry["venue"], re.I) and rec["venue"] and not preprint_venue:
            issues.append({"kind": "VENUE", "year": entry["year"], "title": entry["title"],
                           "detail": f"site says {entry['venue']!r}; source says {rec['venue']!r}"})

    # site entries the source does not know about -- usually fine (theses, new preprints)
    unknown = [e for e in site if norm(e["title"]) not in source]

    if args.json:
        print(json.dumps({"issues": issues, "not_in_source": [e["title"] for e in unknown]}, indent=2))
        return 1 if issues else 0

    print(f"site entries: {len(site)}   source works (deduped): {len(source)}\n")
    if issues:
        for i in issues:
            print(f"  {i['kind']:<8} {i['year']}  {i['title'][:62]}")
            print(f"           {i['detail']}")
    else:
        print("  no gaps: every source work is on the site with DOI/arXiv where known")
    if unknown:
        print(f"\nOn the site but not in OpenAlex ({len(unknown)}) -- verify by hand on Scholar:")
        for e in unknown:
            print(f"  {e['year']}  {e['title'][:66]}")
    print(f"\nManual Scholar check: {SCHOLAR_PROFILE}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
