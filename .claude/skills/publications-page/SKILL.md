---
name: publications-page
description: Add or update entries on publications.html - the ingestion workflow (Google Scholar is blocked, so OpenAlex/Crossref/arXiv stand in), how to fill PDF/DOI/arXiv links, entry HTML anatomy, PDF naming and compression, and how to pull a graphical abstract out of a paper. Use whenever publications are added, corrected, or audited.
---

# publications.html

Read `site-conventions` first. Entries are grouped newest-first in
`<section class="pub-year"><h2>YEAR</h2>`, one `<article class="pub-item">` each.

## 1. Find out what is missing

```bash
python3 scripts/pubs_sync.py        # exits non-zero if there are gaps
```

Reports per work: `MISSING` (not on the site), `DOI` / `ARXIV` (site entry lacks
a link the source knows), `VENUE` (site still says Submitted/Accepted but it is
published).

### Google Scholar is blocked - this matters

Ethan's profile is the intended source of truth:
<https://scholar.google.com/citations?user=q3KI3-0AAAAJ&hl=en&sortby=pubdate>

**Google blocks the `/citations` endpoint for every automated client.** Verified:
plain `curl` with a browser user-agent returns **HTTP 404**, and the agent's
`WebFetch` returns **404** too, while `scholar.google.com` itself returns 200. It
is deliberate anti-scraping - no key, header, or user-agent fixes it. Do not
burn time retrying, and do not claim to have read the profile.

So: **`pubs_sync.py` automates the check via OpenAlex; Scholar stays a manual
eyeball.** Ask Ethan to open the profile (or paste its contents) when you need
certainty that nothing is missing. OpenAlex indexes essentially the same works.

### The sources that do work

| Source | Use for | Endpoint |
|---|---|---|
| OpenAlex | full author work list, DOI, venue, year, arXiv id | `api.openalex.org/works?filter=author.id:A5061968827\|A5141073323` |
| Crossref | resolve a DOI from a title | `api.crossref.org/works?query.bibliographic=<title>` |
| arXiv | preprint metadata | `export.arxiv.org/api/query?id_list=<id>` |

OpenAlex has split Ethan across **two author entities** (`A5061968827`, 36 works;
`A5141073323`, 2) - always query both. It also returns Zenodo deposits, Research
Square mirrors, BAPS meeting abstracts, and arXiv duplicates of published papers;
`pubs_sync.py` filters those and folds preprints into their published record
(including when the preprint carries an extra subtitle, e.g.
`... Navier-Stokes equations. Part 1. Forced response`).

### Two metadata traps that have already bitten

- **bioRxiv DOIs are `10.64898/...`, not `10.1101/...`** for 2026 preprints.
  Both CASCADE and PEAgent links were constructed wrong as `10.1101` and would
  have been dead. **Read the DOI off the PDF's own page stamp** - never build one
  from the preprint id.
- **A journal PDF usually prints its DOI in the page margin.** `10.1111/tpj.71076`
  came off the Kontolati PDF's first page, not from any API.
- The CV and the site disagreed on arXiv `2203.04515`'s title. OpenAlex confirmed
  the site's "Structure and Distribution Metric..." - prefer the indexed record.

## 2. Entry anatomy

```html
  <article class="pub-item">
    <div class="pub-image">
      <img src="images/pubpic/<slug>.png" alt="<what the figure shows>" />
    </div>
    <div class="pub-meta">
      <h3>Title exactly as published</h3>
      <p class="pub-authors">A. Author, B. Author, E. Pickering</p>
      <p class="pub-venue">Journal, volume(issue), pages (YEAR)</p>
      <div class="pub-links">
        <a href="papers/<slug>.pdf" target="_blank" rel="noreferrer">PDF</a>
        <a href="papers/<slug>.txt" target="_blank" rel="noreferrer">BibTeX</a>
        <a href="https://doi.org/..." target="_blank" rel="noreferrer">DOI</a>
        <a href="https://arxiv.org/abs/..." target="_blank" rel="noreferrer">arXiv</a>
        <a href="https://github.com/..." target="_blank" rel="noreferrer">Code</a>
      </div>
      <details>
        <summary>Abstract</summary>
        <p>Verbatim abstract.</p>
      </details>
    </div>
  </article>
```

- Link order: **PDF, BibTeX, DOI, arXiv/bioRxiv, Code.** Include only what exists.
- Exactly **one** `.pub-links` block per entry, never empty (`check_site.py` enforces).
- Unpublished work: `<p class="pub-venue"><b>Submitted</b>, Venue (YEAR)</p>`,
  `<b>Accepted</b>`, or `<b>Preprint</b>, bioRxiv <id> (YEAR)`. Revisit these -
  "Accepted" entries for JASA 2021 and JFM 2025 were both stale for years.
- **No figure?** The article tag must be `class="pub-item pub-item-nofigure"`.
- **Never write an abstract you did not read.** Copy it from the PDF, or omit the
  `<details>` block entirely.

## 3. PDFs

Name `<firstauthor><year><shortslug>.pdf` (`kontolati2026binns.pdf`,
`farghadan2026cascade.pdf`). Incoming files land in `~/Downloads` with arbitrary
names - **verify identity by extracting page 1 before copying**:

```bash
python3 -c "from pypdf import PdfReader; print(PdfReader('x.pdf').pages[0].extract_text()[:400])"
```

Compress anything over ~10MB (`gs -dPDFSETTINGS=/printer` keeps sequence logos
and small multiples legible; `/ebook` at 150dpi smears them for ~1MB less).
Confirm the page count and page-1 text survive. Vector-heavy papers will not
shrink - leave them and rely on the DOI.

## 4. Graphical abstracts

Render, then **look at the figure before choosing it**:

```bash
gs -sDEVICE=png16m -r300 -dFirstPage=N -dLastPage=N -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=fig.png papers/<slug>.pdf
```

Then crop with pillow to the figure's fractional region, auto-trim white margins,
and resize to **760px wide** (the column is 180px; 760 covers retina).

**Figure 1 is not automatically the right figure.** Judge it:

- *Bucksch*: Figure 1 is a Scopus publication-count chart; **Figure 2**, the
  Phenomics wheel, carries the argument.
- *Yao*: Figure 1 is eight panels and turns to mush at thumbnail size; **panel A**
  alone is the framework overview.
- *Kontolati*, *Farghadan*: Figure 1 is already an overview schematic - use it whole.

Crop tight - caption text and neighbouring panel slivers both bleed in easily, so
re-render and re-check after adjusting bounds. Write a descriptive `alt`.

## 5. Known open items

- Five works OpenAlex lists that are **deliberately not on the site** pending
  Ethan's call: two 2024 AIAA conference papers (`10.2514/6.2024-3414`,
  `10.2514/6.2024-3199`), a 2020 *Advances in Building Energy Research* article
  (`10.1080/17512549.2020.1730239`), and two JASA meeting abstracts
  (`10.1121/1.5137546`, `10.1121/1.5067573`). Ask before adding.
- Six entries have no figure: four jet-noise papers with no local PDF, and the
  two building-energy papers.
