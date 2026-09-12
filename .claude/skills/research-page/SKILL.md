---
name: research-page
description: Edit research.html, the CompAgLab research pillars page - pillar anatomy and the unfilled image placeholders each pillar still carries. Use when adding, reordering, or rewriting a research theme, or when supplying pillar artwork.
---

# research.html

Read `site-conventions` first.

## Pillar anatomy

```html
        <article class="pillar">
          <div class="pillar-text">
            <h2>Theme name</h2>
            <p>Two to four sentences.</p>
          </div>
          <div class="pillar-media" aria-hidden="true">
            <span>Image Placeholder</span>
          </div>
        </article>
```

Current pillars, in order: **LLMs for Editing**, **Mechanistic Ag AI**,
**Active Learning for Ag**, **Loss Functions for Ag**, **Agents for Ag Design**.

`.research-pillars` is a flex column with `gap: 22px` - pillars stack, so order in
the file is order on the page.

## Pillar artwork

Each pillar carries the figure that best represents it. Paper figures are reused
from `images/pubpic/` rather than duplicated; non-paper artwork lives in
`images/research/`:

| Pillar | Figure |
|---|---|
| LLMs for Editing | `farghadan2026cascade` (CASCADE, DNA language-model attributions) |
| Mechanistic Ag AI | `kontolati2026binns` (biology-informed neural networks) |
| Active Learning for Ag | `pickering2022discovery` (active learning in neural operators) |
| Agents for Ag Design | `images/research/vipr-ag-agents.jpg` (UGA Agentic AgCRADLE workflow) |

"Loss Functions for Ag" was removed on 2026-09-12 because no figure we had
actually illustrated it; the markup is preserved in `DEFERRED.md`.

**Do not use the PEAgent figure for the agents pillar.** Despite the name,
PEAgent is a sequence-model framework and web portal, not an agentic system -
Ethan flagged the name as a misnomer. That pillar leads with the UGA VIPR course
*AI Agents for a Sustainable Food Supply*, co-led with Scott Jackson.

The wrapper is `<div class="pillar-media">` with **no `aria-hidden`** once it holds
a real figure, and `.pillar-media:has(img)` drops the dashed placeholder chrome.
Figures are `data-zoomable` with a `data-full` master - see `site-conventions`.

To add artwork for a new pillar, use the Ghostscript-render-then-crop recipe in
`publications-page`, which produces a 760px thumbnail and an 1800px master.

## Writing a pillar

Match the existing voice: what the lab builds, then what it is for. Keep each to
one paragraph - the page is a scan, not a read. Each pillar should map to real
work; cross-check against `publications.html` so the themes and the papers agree.
