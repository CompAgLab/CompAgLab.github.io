# START HERE

Orientation for a new session on the **Computational Agriculture Lab** website.
Read this first, then load the skill for whatever page you're touching.

Live: <https://compaglab.github.io> · Repo: `CompAgLab/CompAgLab.github.io` (branch `main`)

---

## What this is

A four-page static site for Ethan Pickering's lab in Crop and Soil Sciences at
the University of Georgia. **Plain HTML and one stylesheet. No Jekyll, no build
step, no framework, no package.json.** What is committed is what ships; GitHub
Pages serves `main` about 60–80 seconds after a push.

| Page | Purpose | State |
|---|---|---|
| `index.html` | Hero, lab's guiding question, **active recruiting notice** | thin by design |
| `research.html` | 4 research pillars, each with a figure | recently rebuilt |
| `people.html` | PI + 7 members in 4 role sections | current |
| `publications.html` | 22 entries, 2016–2026 | complete and verified |

## Ground rules

1. **Never invent a fact.** Not a DOI, a degree, a start year, an abstract, or a
   figure pairing. Leave it out and say it's missing. Constructed DOIs have been
   wrong here before (bioRxiv uses `10.64898/…`, not `10.1101/…`).
2. **Run the validator before every push:** `python3 scripts/check_site.py`.
   It exits non-zero on broken tags, dead local links, and page invariants.
3. **Stage and stop** unless Ethan asks you to commit or push.
4. **Content pulled from the site goes in `DEFERRED.md`**, markup preserved, with
   a note on what would bring it back. Don't just delete.
5. The git remote **must be SSH** — HTTPS has no usable credential here.

## The map

```
.claude/skills/site-conventions/     ← load this first, always
.claude/skills/publications-page/    ← publication ingestion, figures, abstracts
.claude/skills/people-page/          ← member cards, roles, headshots
.claude/skills/research-page/        ← pillars and their artwork
.claude/skills/home-page/            ← hero and background video
scripts/check_site.py                ← validator (pre-push gate)
scripts/pubs_sync.py                 ← publications vs OpenAlex/Crossref
scripts/fetch_abstract.py            ← abstract by DOI, cleaned
DEFERRED.md                          ← what we pulled, and what would restore it
```

## What the site looks like

A model that cannot see the rendered page should know:

- **Type:** Georgia / Times New Roman **serif throughout**, 18px, line-height 1.6.
  Academic and traditional; no sans-serif anywhere, no web fonts loaded.
- **Colour:** almost none. Four tokens — `--ink #1a1a1a`, `--muted #5a5a5a`,
  `--border #e2e2e2`, `--wash #f7f7f7`. No brand colour, **no UGA red**, no accent.
  Light mode only (`color-scheme: light`); there is no dark-mode support.
- **Layout:** every page is one centred column, `max-width: 1320px`, content sitting
  in a translucent white `.content-panel` (85% opacity, 14px radius, soft shadow).
- **Backgrounds:** full-bleed and per-page. Home plays `soy-background.mp4`, People
  plays `corn-sunset.mp4`; Research and Publications use static photographs washed
  out behind a 72% white overlay. Sticky translucent header with four tab-style
  nav links.
- **Density:** publications and people are long single-column lists. Abstracts and
  biographies are collapsed behind `<details>`, so the pages scan short and expand
  deep. Figures are click-to-enlarge via `lightbox.js`.

## Where it stands

Verified as of **2026-09-12**:

- All 22 publications have authors, venue, at least one link, an **abstract**, and
  a **graphical abstract**. `check_site.py` enforces every one of those.
- `pubs_sync.py` exits clean: no missing DOI, arXiv link, or paper versus OpenAlex.
- Six works are deliberately off the site — see `DEFERRED.md`.

### Size — not urgent, but know the shape

| Limit | GitHub | Us |
|---|---|---|
| Single file (hard block) | 100 MiB | 31 MB max |
| **Published Pages site** | **1 GB hard** | ~240 MB |
| Pages source repo | 1 GB recommended | 477 MB on disk |

`papers/` is 188 MB — **78% of what we publish**. `.git` is 237 MB, bigger than
the working tree, because replaced and recompressed PDFs leave their old blobs in
history forever. Nothing is at risk; revisit past ~700 MB. Options then: stop
hosting PDFs that are one DOI click away, or rewrite history (disruptive, public
repo, only on an explicit ask).

---

## If you were asked for ideas to make this more appealing

Ethan may hand this file to a model and ask how to improve the site for visitors.
Useful context for that:

**Audience, roughly in priority order.** Prospective PhD students and postdocs —
the homepage says the lab is *actively recruiting* and that is the site's main job;
then collaborators and program officers checking credibility; then peers arriving
from a paper.

**Honest weaknesses, so suggestions aren't wasted on what's already fine:**

- **No entry point for a prospective student.** There is no "Join / Openings" page,
  no application guidance, no statement of what it's like to work here. The
  recruiting ask lives in one homepage paragraph and goes nowhere.
- **No contact route anywhere.** No email, no address, no form, no map. A visitor
  who wants in has nothing to click.
- **No news, dates, or signs of life.** Nothing tells a visitor the lab is active
  this month. The personal site has a `news.yml`; this one has no equivalent.
- **Research pillars are abstract.** Five sentences each about methods, with no
  crops named up front, no outcomes, no link from a pillar to the papers behind it.
- **Publications are an undifferentiated list.** No "selected work", no way to
  filter or jump by year, no topic grouping — the 2026 plant-genomics work sits in
  the same visual weight as 2016 building-energy work from a prior career.
- **People cards carry no contact or links** except the PI's, and no `.person-facts`
  for five of seven members (those facts were never supplied — see `people-page`).
- **Visually conservative and monochrome.** Serif, greyscale, no UGA identity, no
  dark mode. Defensible as understated; also indistinguishable from a 2009
  academic page.
- **The homepage is a single panel of prose.** No imagery of the actual work — and
  the lab has genuinely striking figures sitting in `images/pubpic/`.

**Constraints any suggestion must respect:** static HTML only, no build step, no
framework or CDN dependency, keep it fast and accessible (the current markup uses
real landmarks, `aria-current`, focusable figures), and mind the size budget above.
The four-page structure is not sacred; adding a page is cheap, and nav lives in
each page's `<header>` and must be updated in all of them together.
