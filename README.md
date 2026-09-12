# CompAgLab.github.io

The Computational Agriculture Lab's website — <https://compaglab.github.io>

Plain static HTML served by GitHub Pages from `main`. **No Jekyll, no build
step.** Edit the `.html` files directly; what is committed is what ships.

```
index.html  research.html  people.html  publications.html
styles.css              one stylesheet for all four pages
images/  videos/  papers/  files/
scripts/                maintenance tooling
.claude/skills/         how to edit each page (see below)
```

## Before you push

```bash
python3 scripts/check_site.py     # tag balance, dead local links, page invariants
```

Non-zero exit means something is broken. The most common defect is a PDF linked
but never copied in, which the validator catches.

```bash
python3 scripts/pubs_sync.py      # publications.html vs OpenAlex/Crossref
```

Reports publications that are missing, or that lack a DOI/arXiv link the public
record knows about. Google Scholar blocks automated access to its profile pages,
so this uses OpenAlex as the automated stand-in — the Scholar profile itself
stays a manual check.

## Editing guides

Each page has a skill under `.claude/skills/` documenting its structure and the
traps found while building it. They are written for Claude Code but read fine as
plain documentation.

| Skill | Covers |
|---|---|
| `site-conventions` | repo layout, CSS grid traps, local tooling, deploy loop — **start here** |
| `publications-page` | publication ingestion, DOI/arXiv sourcing, PDFs, graphical abstracts |
| `people-page` | member cards, sections, roles and affiliates, headshots |
| `home-page` | hero and background-video pattern |
| `research-page` | research pillars and their placeholder artwork |

The remote must be SSH (`git@github.com:CompAgLab/CompAgLab.github.io.git`);
HTTPS has no usable credential. Pages takes roughly 60–80 seconds to serve a push.
