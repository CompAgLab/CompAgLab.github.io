---
name: site-conventions
description: Shared conventions for the CompAgLab static site - repo layout, the CSS grid traps, the validator, available local tooling, and the push/verify deploy loop. Load this before editing any page; the per-page skills (publications-page, people-page, home-page, research-page) assume it.
---

# CompAgLab site conventions

`~/Documents/git/CompAgLab.github.io` serves <https://compaglab.github.io> from
GitHub Pages on `main`. **Plain static HTML. No Jekyll, no build step, no
package.json.** What is in the repo is what ships, byte for byte.

```
index.html  research.html  people.html  publications.html
styles.css              one stylesheet for all four pages
images/people/          headshots         images/pubpic/   publication figures
images/hero/            video posters     images/backgrounds/
videos/                 background loops  papers/          PDFs + .txt BibTeX
files/                  CV
scripts/check_site.py   structural validator (run before every push)
scripts/pubs_sync.py    publication cross-check against OpenAlex/Crossref
```

## Always run the validator before pushing

```bash
python3 scripts/check_site.py     # exits non-zero on any problem
```

It checks tag balance, that every local `src=`/`href=` target exists, and the
per-page invariants described in the page skills. It has a self-test history:
injected faults (stray `</article>`, dead asset, empty link block, missing
`.person-role`) are all caught. A silent 404 on a linked PDF is the single most
common defect here, because PDFs are copied in by hand.

## Two CSS grid traps

`styles.css` uses fixed two-column grids with a 180px media column:

```css
.person-card { grid-template-columns: 180px 1fr; }
.pub-item    { grid-template-columns: 180px 1fr; }
```

1. **A `.pub-item` with no `.pub-image` puts its text in the 180px column.**
   It does not gracefully span. Figureless entries must carry
   `class="pub-item pub-item-nofigure"`; a `:has(.pub-image)` rule backs this up
   for entries added later without the class. `check_site.py` enforces it.
2. **`.person-photo img` is `height: auto`**, so headshot aspect ratios are
   whatever the source file is - a landscape photo renders short and wide beside
   square ones. Either crop headshots square before adding them, or add
   `aspect-ratio: 1; object-fit: cover` (not yet done; Roth Conrad's card shows
   the effect).

Theme tokens are `--ink --muted --border --wash` on `:root`, `color-scheme: light`.
One breakpoint, `@media (max-width: 700px)`, collapses both grids to one column.

## Local tooling (this Mac, verified)

| Need | Use | Not available |
|---|---|---|
| PDF text | `python3` + `pypdf` (`pip install pypdf`) | `pdftotext`, poppler |
| PDF page -> PNG | `gs` (Ghostscript, `/usr/local/bin/gs`) | `pdftoppm`, so `Read` cannot render PDFs |
| PDF compress | `gs -dPDFSETTINGS=/printer` | `qpdf`, `cpdf` |
| Image crop/resize | `python3` + `pillow` | ImageMagick (`convert`/`magick`) |
| GitHub API | plain `git` over SSH | `gh` CLI |

Ghostscript only shrinks PDFs whose bulk is **raster images**. A vector-figure
paper (most fluid-mechanics journals) barely moves - `towne2022efficient.pdf`
went 17MB to 16MB. Don't rasterize to force it; keep the DOI link instead.

## Deploy loop

The remote **must be SSH**. HTTPS has no usable credential in this environment
and fails with `could not read Username`:

```bash
git remote set-url origin git@github.com:CompAgLab/CompAgLab.github.io.git
```

```bash
python3 scripts/check_site.py && git add -A && git commit && git push origin main
```

GitHub Pages takes **roughly 60-80 seconds** to serve a push. Verify against the
live site rather than assuming - poll for a string you just added:

```bash
for i in $(seq 1 10); do
  n=$(curl -s https://compaglab.github.io/people.html | grep -c 'SOMETHING_NEW')
  [ "$n" -ge 1 ] && echo LIVE && break; sleep 20
done
```

Check new binaries actually serve: `curl -s -o /dev/null -w '%{http_code} %{size_download}' <url>`.

## House rules

- Kebab-case every asset filename (`olatunde-akanbi.webp`, not `Olatunde-Akanbi.webp`).
- Copied files sometimes arrive mode 600; `chmod 644` them or they 404 for visitors.
- Never invent a fact - a DOI, a degree, a start year, an abstract. Leave the
  field out and say it is missing. Constructed DOIs have already been wrong once
  (see publications-page, bioRxiv prefix).
- Stage changes and stop unless the user asks to commit or push.
